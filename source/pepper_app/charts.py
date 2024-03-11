import plotly.express as px
import pandas as pd


def article_price_history_chart(discount_price_list, date_added_list, article_name_list, article):
    """The function is responsible for drawing a graph of the history of price changes of an item."""
    data = {"Date": pd.to_datetime(date_added_list),
            "Price [zł]": discount_price_list,
            "Name": article_name_list}
    
    df = pd.DataFrame(data)

    fig = px.scatter(df, 
                     x="Date", 
                     y="Price [zł]", 
                     title=f"Searched article: {''.join(article)}",
                     hover_data="Name",
                     trendline="ols", 
                     template="plotly_dark")

    return fig