from collections import Counter

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def article_price_history_chart(discount_price_list, date_added_list, article_name_list):
    """To fix"""

    data = {"Date": pd.to_datetime(date_added_list),
            "Price": discount_price_list,
            "Name": article_name_list}
    
    df = pd.DataFrame(data)

    fig = px.scatter(df, 
                     x="Date", 
                     y="Price", 
                     title=f"{' '.join(list)}",
                     hover_data="Name",
                     trendline="ols", 
                     template="plotly_dark")

    return fig