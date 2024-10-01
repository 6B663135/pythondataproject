import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
#q1   
tesla=yf.Ticker("TSLA")
tesla_data=tesla.history(period="max")
tesla_data.reset_index(inplace=True)
url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
#q2
html_data=requests.get(url).content
soup=BeautifulSoup(html_data,"html.parser")
tesla_revenue=pd.DataFrame(columns=["Date","Revenue"])
for row in soup.find("table").find("tbody").find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    rev = col[1].text   
    tesla_revenue=pd.concat([tesla_revenue,pd.DataFrame({"Date":[date],"Revenue":[rev]})], ignore_index=True)
    tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"", regex=True)
    tesla_revenue.dropna(inplace=True)
    tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
print(tesla_revenue.tail())

#q3 GME

gme=yf.Ticker("GME")
gme_data=gme.history(period="max")
gme_data.reset_index(inplace=True)
print(gme_data.head())
#q4 code
url2="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"

html_data2=requests.get(url2).content
soup2=BeautifulSoup(html_data2,"html.parser")
gme_revenue=pd.DataFrame(columns=["Date","Revenue"])
for row in soup2.find("table").find("tbody").find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    rev = col[1].text
    gme_revenue=pd.concat([gme_revenue,pd.DataFrame({"Date":[date],"Revenue":[rev]})], ignore_index=True)
    gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"", regex=True)
    gme_revenue.dropna(inplace=True)
    gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
print(gme_revenue.tail())
#q5
make_graph(tesla_data,tesla_revenue,'Tesla Stock Price & Revenue')
#q6
make_graph(gme_data,gme_revenue,'GME Stock Price & Revenue')
