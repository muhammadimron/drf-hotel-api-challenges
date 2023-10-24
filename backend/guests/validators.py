from rest_framework.validators import UniqueValidator
from .models import Guest

unique_name_validator = UniqueValidator(queryset=Guest.objects.all(), lookup='iexact')