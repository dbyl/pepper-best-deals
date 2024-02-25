from collections import Counter

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def article_price_history_chart(discount_price_list, date_added_list, article_name_list):
    """To fix"""

    #data_x = [c for c in discount_price_list]
    #data_y = [c for c in date_added_list]


    fig = go.Figure()
    df = pd.DataFrame({'x':date_added_list, 'y':discount_price_list})
    fig = px.scatter(template="plotly_dark")
    fig2 = px.scatter(df, x="x", y="y")
    fig.add_trace(fig2.data[0])


    return fig