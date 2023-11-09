from api.models import ChangedLog

import pandas as pd
import seaborn as sns

def set_changed_log_charts():
    changed_logs = ChangedLog.objects.all().values("model", "action")
    df = pd.DataFrame(changed_logs)
    _render_changed_log_charts(df)

def _render_changed_log_charts(df):
    custom_palette = ["#1976d2", "#c2614e", "#d4cf3f"]
    g = sns.catplot(x="action", data=df, hue="model", kind="count", palette=custom_palette, aspect=2, legend_out=False)
    g.set_axis_labels("Action", "Count")
    g.ax.set_title("Count of Actions by Models", fontdict={"fontsize": 16, "fontweight": "bold"})
    g.savefig("./api/static/chart_log.png")