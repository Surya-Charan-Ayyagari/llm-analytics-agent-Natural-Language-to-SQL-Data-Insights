import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

def pick_chart(df: pd.DataFrame):
    dt_cols = [c for c in df.columns if 'date' in c.lower() or 'month' in c.lower()]
    num_cols = df.select_dtypes('number').columns.tolist()
    if dt_cols and num_cols:
        return ("line", dt_cols[0], num_cols[0])
    if num_cols:
        return ("bar", df.columns[0], num_cols[0])
    return (None, None, None)


def render_chart(df: pd.DataFrame):
    chart, x, y = pick_chart(df)
    if chart is None:
        return None
    fig = plt.figure()
    if chart == 'line':
        d = df.sort_values(x)
        plt.plot(d[x], d[y])
        plt.xlabel(x); plt.ylabel(y); plt.title(f"{y} over {x}")
    else:
        top = df if y not in df.columns else df.nlargest(10, y)
        plt.bar(top[x].astype(str), top[y])
        plt.xticks(rotation=45, ha='right')
        plt.xlabel(x); plt.ylabel(y); plt.title(f"Top by {y}")
    plt.tight_layout()
    return fig