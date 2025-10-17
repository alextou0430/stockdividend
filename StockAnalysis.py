import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, date, timedelta

header = st.container()

with header:
    st.title('Welcome to Alex\'s Stock Analysis !!!')

def display_stock_chart(ticker, start_date, end_date, start_amount):
    try:
        print("BEGIN function display_stock_chart ----------------------------------------------------------------")
        company = yf.Ticker(ticker)
        print("AFTER")
        print("Company:", company)
        print("company info: ", company.info)
        company_long_name = company.info['longName']
        st.write("Description for ", company_long_name)
        st.write(company.info['longBusinessSummary'])
        df = company.history(start="1900-01-01")
        company_found_date = str(df.iloc[0].name)[0:10]
        st.write("For", company_long_name, "we have data dating back to ", company_found_date)
        price_data = yf.download(tickers=ticker, start=start_date, end=end_date)
        start_price = round(price_data.head(1)['Close'].values[0][0], 2)
        st.write("Stock closing price for start input date is: ", start_price)
        end_price = round(price_data.tail(1)['Close'].values[0][0], 2)
        st.write("Stock closing price for your end date is: ", end_price)
        st.write("input amount(USD): ", start_amount)
        number_of_original_share = start_amount // start_price
        total_cost_without_dividend = round(((start_amount // start_price) * end_price) - (start_price * int(number_of_original_share)), 2)
        # subtracted the start price * number of shares you have because we want to calculate the cost increase from our original price
        st.write("The final total share cost increase from start without dividend reinvestment is: ", total_cost_without_dividend, "dollars.")
        st.write("the number of shares of this value is: ", int(number_of_original_share))
        st.write("However, including the dividend reinvestment accumulated over time,")
        dividendCalculation(ticker, start_amount, price_data, end_price, total_cost_without_dividend)
        st.write("Stock chart from input date range: ", start_date, " to ", end_date)

        close_price_data_dict = price_data['Close'].to_dict()
        st.line_chart(close_price_data_dict[ticker])

        st.write("Dividend payout throughout the history of the company:")
        dividend_data = yf.Ticker(ticker).dividends
        orig_dividends_dict = dividend_data.to_dict()
        st.line_chart(dividend_data)
    except Exception as e:
        print(f"We caught exception at: {e}")
        st.write("You inputted an invalid symbol: ", ticker)
        print("----------------- END EXCEPTION ------------------------------------------------------------")

def dividendCalculation(ticker, start_amount, data, end_price, grand_total_without_dividend):
    company = yf.Ticker(ticker)
    dividend_data = yf.Ticker(ticker).dividends
    orig_dividends_dict = dividend_data.to_dict()
    left_over_cost = 0
    closing_price_on_start_date = data.iloc[0]["Close"].squeeze()
    dividends_dict = {}
    starting_number_shares = round(start_amount // closing_price_on_start_date, 2)
    starting_shares_leftover_money =start_amount - (starting_number_shares * closing_price_on_start_date)
    left_over_cost += starting_shares_leftover_money
    for key, value in orig_dividends_dict.items():
        new_key = str(key)[:10]
        dividends_dict[new_key] = value

    number_of_current_shares = starting_number_shares
    for date, dividendCost in dividends_dict.items():
        if date in data.index:
            current_record = data.loc[date]
            current_stock_price = current_record["Close"].squeeze()
            current_share_value = starting_number_shares * current_stock_price
            dividend_amount = dividendCost * number_of_current_shares

            # we would get the dividend amount for the current date by multiplying
            #the dividend cost by the current number of shares. if the dividend amount
            #is greater than the current closing price for the stock, we buy as much as we can
            #if it is not greater than stock we store it in leftover_cost
            if dividend_amount >= current_stock_price:
            # print("dividend amount is: ", dividend_amount)
                num_shares_bought_with_dividend = dividend_amount // current_stock_price
                number_of_current_shares = number_of_current_shares + num_shares_bought_with_dividend
                # left_over_cost = left_over_cost + ((dividend_amount / current_stock_price) - (dividend_amount // current_stock_price))
                left_over_cost += dividend_amount - (num_shares_bought_with_dividend * current_stock_price)
            else:
                left_over_cost += dividend_amount
        else:
            continue

    #*****************dividendsCalculationWrite**************************
    # st.write("Your stock price per share for your start date was: ", closing_price_on_start_date)
    # st.write("Your final stock price when you cashed out was: ", current_stock_price)
    st.write("The number of shares you own after applying dividend reinvestment is:", number_of_current_shares)
    st.write("Your total leftover cost money after reinvesting dividends is: ", left_over_cost)
    st.write("Since it is not ideal to reinvest left over cost every time you have more money than 1 share price, our calculation collects all leftovers and adds it to the grand total at the end.")
    st.write("Therefore, your final grand total amount of USD including the starting amount is: ", number_of_current_shares * end_price + left_over_cost)
    st.write("and the pure profit from your starting price would be: ", (number_of_current_shares * end_price + left_over_cost) - start_amount)

    #*****************dividendsCalculationWrite**************************

    # print("dividends_dict:", dividends_dict)

    # for key, value in dividends_dict.items():
    #     print(key, value)

    # print("----------------- begin check --------------")
    # print(data)
    # # print(type(data))
    # print("------------------------------------------")
    # # print(data.info())
    # print("------------------------------------------")
    # # print(data.index)
    # # print(type(data.index))
    # # print("here", data.iloc[0])
    # print("-------------------------------------------")
    # print("there", current_record)
    # print("----------------- end check --------------")








def main():

    #sidebar inputs
    st.sidebar.header("Enter your stock information")
    ticker= st.sidebar.text_input("Enter stock ticker (e.g. AAPL):","MPWR")
    amount = st.sidebar.number_input(
        'Initial Investment',
        min_value=1,  # Optional: minimum value allowed
        max_value=100000000,  # Optional: maximum value allowed
        value=10000,  # Optional: default value
        step=100,  # Optional: increment/decrement step
        help="Enter your investment amount from between 1 to 100,000,000"  # Optional: tooltip
    )

    start_date = st.sidebar.text_input("Start Date", "2005-02-01")
    today = date.today()
    # end_date = st.sidebar.text_input("End Date", "2025-10-10")
    end_date = st.sidebar.text_input("End Date", str(today))
    display_stock_chart(ticker, start_date, end_date, amount)
main()
