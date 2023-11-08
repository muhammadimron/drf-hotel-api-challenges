import pandas as pd
from io import BytesIO
from django.utils.timezone import now
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from rest_framework import authentication, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.authentication import BearerAuthentication
from api.models import Booking, Guest, Room
from api.serializers import BookingSerializer
from api.utils import get_bookings_row, get_bookings_list, set_chart_bookings

from xhtml2pdf import pisa
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak, Spacer, Image
from reportlab.lib import styles, colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.doctemplate import Frame, PageTemplate

class BookingViewSets(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, BearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def shared_logic(self, validated_data=None, method=None):
        room_id = validated_data.get('room_id')
        guest_id = validated_data.get('guest_id')
        if room_id:
            duplicate_room_id = Booking.objects.filter(room_id=room_id)
            if duplicate_room_id:
                raise ValidationError("You cannot bookings the ordered room")
        if guest_id:
            duplicate_guest_id = Booking.objects.filter(guest_id=guest_id)
            if duplicate_guest_id:
                raise ValidationError("You cannot ordered more than one room")
        return validated_data

    def perform_create(self, serializer):
        validated_data = self.shared_logic(validated_data=serializer.validated_data)
        serializer.save(**validated_data)
    
    def perform_update(self, serializer):
        validated_data = self.shared_logic(validated_data=serializer.validated_data, method='PUT')
        serializer.save(**validated_data)

    def perform_destroy(self, instance):
        hard = self.request.query_params.get('hard')
        instance.delete(hard)

    @action(methods=["GET"], detail=False)
    def add(self, request, *args, **kwargs):
        Booking.objects.all().delete()
        for i in range(1, 6):
            room = Room.objects.filter(floor=1, number=i).first()
            guest = Guest.objects.filter(name=f"People number {i}").first()
            serializer = BookingSerializer(data={
                "room_id": room.id,
                "guest_id": guest.id
            })
            serializer.is_valid()
            serializer.save()
        return Response({
            "success": "please hit http://127.0.0.1:8000/bookings/ to see the result."
        }, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="export-excel")
    def export_excel(self, request, *args, **kwargs):
        rows = get_bookings_row()
        df = pd.DataFrame(rows)
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            status=status.HTTP_200_OK
            )
        response["Content-Disposition"] = 'attachment; filename="bookings_list.xlsx"'
        df.to_excel(response, index=False),
        return response

    @action(methods=["GET"], detail=False)
    def template(self, request, *args, **kwargs):
        rows = get_bookings_row()
        return render(request, "booking_template.html", {"rows": rows})

    @action(methods=["GET"], detail=False, url_path="export-pdf")
    def export_pdf(self, request, *args, **kwargs):
        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)
        elements = []

        title_text = "Bookings List - Hotel API"
        title_style = styles.getSampleStyleSheet()["Title"]
        title = Paragraph(title_text, title_style)
        
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        img = Image("./api/static/download.png")
        elements.append(img)
        elements.append(Spacer(1, 0.3*inch))

        body_text = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quidem atque vel placeat consequatur, nam ducimus minima, enim nemo soluta eveniet natus dolore repudiandae porro mollitia obcaecati. Debitis nisi magnam ab."
        body_style = styles.getSampleStyleSheet()["BodyText"]
        body_style.alignment = 4
        body = Paragraph(body_text, body_style)
        elements.append(body)
        elements.append(Spacer(1, 0.5*inch))

        set_chart_bookings()
        chart = Image("./api/static/chart.png", width=400, height=300)
        elements.append(chart)
        elements.append(Spacer(1, 0.3*inch))

        rows = get_bookings_list()
        table = Table(rows)
        style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), (0.098, 0.462, 0.823)),
            ("TEXTCOLOR", (0, 0), (-1, 0), (1, 1, 1)),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("TOPPADDING", (0, 0), (-1, 0), 12),
            ("GRID", (0, 0), (-1, -1), 1, (0, 0, 0)),
        ])
        table.setStyle(style)
        
        elements.append(table)

        elements.append(Spacer(1, 0.5*inch))
        elements.append(body)
        elements.append(Spacer(1, 0.2*inch))
        elements.append(body)

        # elements.append(PageBreak())
        # elements.append(title)
        # elements.append(Spacer(1, 0.5*inch))
        # elements.append(img)
        # elements.append(Spacer(1, 0.3*inch))
        # elements.append(body)
        # elements.append(Spacer(1, 0.5*inch))
        # elements.append(table)

        # elements.append(PageBreak())
        # elements.append(title)
        # elements.append(Spacer(1, 0.3*inch))
        # elements.append(chart)
        # elements.append(Spacer(1, 0.5*inch))
        # elements.append(body)
        # elements.append(Spacer(1, 0.5*inch))
        # elements.append(table)
        
        doc.build(elements, onFirstPage=_create_header_footer, onLaterPages=_create_header_footer)

        buf.seek(0)

        response = FileResponse(buf, content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=bookings_list.pdf"
        return response

class BookingUserViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, BearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(is_deleted=False)

def _create_header_footer(canvas, doc):
    canvas.saveState()
    width, _ = letter
    header_text = "Report Booking List - Hotel API"
    header_style = styles.getSampleStyleSheet()["BodyText"]
    header_style.fontName = "Helvetica-Bold"
    header_style.fontSize = 12
    header_style.textColor = colors.white
    canvas.setFillColorRGB(0.098, 0.462, 0.823)
    canvas.rect(0, 749, 620, 60, fill=True)
    canvas.setLineWidth(1)
    canvas.setStrokeColorRGB(0.098, 0.462, 0.823)
    canvas.line(0, letter[1] - 0.6 * inch, letter[0], letter[1] - 0.6 *inch)
    header = Paragraph(header_text, header_style)
    header.wrap(width, 1*inch)
    header.drawOn(canvas, 0.5 * inch, 10.65 * inch)
    footer_text = f"Page {doc.page}"
    footer_style = styles.getSampleStyleSheet()["BodyText"]
    footer_style.textColor = colors.white
    canvas.rect(0, 0, 620, 36, fill=True)
    canvas.setLineWidth(1)
    canvas.setStrokeColorRGB(0.098, 0.462, 0.823)
    canvas.line(0.3 * inch, letter[1] - 10.5 *inch, letter[0] - 0.3 * inch, letter[1] - 10.5 *inch)
    footer = Paragraph(footer_text, footer_style)
    footer.wrap(width, 0.5*inch)
    footer.drawOn(canvas, letter[0] - inch, 0.2 * inch)
    canvas.drawImage("./api/static/pandas.png", 0.5 * inch, 10, width=60, height=20, mask="auto")
    canvas.restoreState()