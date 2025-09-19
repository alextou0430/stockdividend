import streamlit as st
import yfinance as yf
import pandas as pd
header = st.container()

with header:
    st.title('Welcome to Alex Stock Analysis !!!')


# # stock symbol, start amount, start and end date (input)
# ticker = "AAPL"
#
# start_date = "2005-01-01"
# end_date = "2025-09-11"
#
# price_data = yf.download(tickers=ticker, start=start_date, end=end_date)
# pd.set_option("display.max_rows", None)      # Show all rows
# pd.set_option("display.max_columns", None)   # Show all columns
# print(price_data)
# pd.set_option("display.max_rows", None)      # Show all rows
# pd.set_option("display.max_columns", None)   # Show all columns
#
# dividend_data = yf.Ticker(ticker).dividends
# # put all dividend info in my dictionary
# orig_dividends_dict = dividend_data.to_dict()
# # print(orig_dividends_dict)
# dividends_dict = {str(k)[:10]: v for k, v in orig_dividends_dict.items()}
# for key, value in dividends_dict.items():
#     print("DIVIDEND PAID", key, value)


def display_stock_chart(ticker, start_date, end_date):
    print("user input:", ticker, start_date, end_date)
    price_data = yf.download(tickers=ticker, start=start_date, end=end_date)
    # print(price_data)

    company = yf.Ticker(ticker)
    df = company.history(start="1900-01-01")
    company_long_name = company.info['longName']
    v = str(df.iloc[0].name)[0:10]
    st.write("For", company_long_name, "we have data dating back to ", v)
    for key, value in company.info.items():
        print(key, value)
    st.write(company.info['longBusinessSummary'])


    st.write("Stock chart per your input range date")
    st.line_chart(price_data['Close'])

    st.write("Dividend payout in $")
    dividend_data = yf.Ticker(ticker).dividends
    # orig_dividends_dict = dividend_data.to_dict()
    # print(orig_dividends_dict)
    # dividends_dict = {str(k)[:10]: v for k, v in orig_dividends_dict.items()}
    # for key, value in dividends_dict.items():
    #     print("DIVIDEND PAID", key, value)
    st.line_chart(dividend_data)

# streamlit run StockAnalysis.py
def main():
    #sidebar inputs
    st.sidebar.header("Enter your stock information")
    ticker= st.sidebar.text_input("Enter stock ticker (e.g. AAPL):","AAPL")
    # amount = st.sidebar.number_input("Initial Investment", min_value=0.0, value=0.0)
    start_date = st.sidebar.text_input("Start Date", "2012-02-01")
    end_date = st.sidebar.text_input("End Date", "2025-06-02")
    display_stock_chart(ticker, start_date, end_date)

main()
