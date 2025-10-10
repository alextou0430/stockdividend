import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

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


def display_stock_chart(ticker, start_date, end_date, start_amount):
    company = yf.Ticker(ticker)

    for key, value in company.info.items():
        print(key, value)
    st.write(company.info['longBusinessSummary'])
    df = company.history(start="1900-01-01")
    company_long_name = company.info['longName']
    v = str(df.iloc[0].name)[0:10]
    st.write("For", company_long_name, "we have data dating back to ", v)
    print("user input:", ticker, start_date, end_date)
    price_data = yf.download(tickers=ticker, start=start_date, end=end_date)
    print(price_data)
    print("===============================================")
    print(price_data.info)
    print("This is the type for price data", type(price_data))
    print("This is the type for price data info", type(price_data.info))
    # print(price_data.head(1))
    print(price_data.head(1)['Close'], "here")
    # print(type(price_data.head(1)['Close']))
    print(price_data.head(1)['Close'].values[0][0], "here 2")
    # print(type(price_data.head(1)['Close'].values[0][0]))
    start_price = round(price_data.head(1)['Close'].values[0][0], 2)
    print(start_price)
    st.write("Stock price for start input date is: ", start_price)
    end_price = round(price_data.tail(1)['Close'].values[0][0], 2)
    print(end_price)
    st.write("Stock price for your end date is: ", end_price)
    st.write("input amount(USD): ", start_amount)
    number_of_share = start_amount // start_price
    total_cost_without_dividend = (start_amount / start_price) * end_price
    print(total_cost_without_dividend)
    total_cost_without_dividend = round(total_cost_without_dividend, 2)
    # st.write("The final total share cost increase without dividend reinvestment is: $", f"{total_cost_without_dividend:,.2f}")
    st.write("The final total share cost increase without dividend reinvestment is: ", total_cost_without_dividend)

    st.write("the number of shares of this value is: ", int(number_of_share))
    st.write("However, including the dividend reinvestment accumulated over time,")
    dividendCalculation(ticker, start_date, end_date, start_amount, price_data, end_price, total_cost_without_dividend)


    st.write("Stock chart from input date range: ", start_date, " to ", end_date)
    st.line_chart(price_data['Close'])

    st.write("Dividend payout in $ in between range", start_date, " to ", end_date)
    dividend_data = yf.Ticker(ticker).dividends
    orig_dividends_dict = dividend_data.to_dict()
    print(orig_dividends_dict)
    dividends_dict = {str(k)[:10]: v for k, v in orig_dividends_dict.items()}
    for key, value in dividends_dict.items():
        print("DIVIDEND PAID", key, value)
    st.line_chart(dividend_data)

def dividendCalculation(ticker, start_date, end_date, start_amount, data, end_price, grand_total_without_dividend):
    company = yf.Ticker(ticker)
    dividend_data = yf.Ticker(ticker).dividends
    orig_dividends_dict = dividend_data.to_dict()
    total_current_dividend_cost = 0
    closing_price_start_date = 0
    num_shares_start = 0
    total_cost_without_dividend = 0
    dividend_cost_current_date = 0
    dividends_dict = {str(k)[:10]: v for k, v in orig_dividends_dict.items()}
    closing_price_start_date = data.loc[start_date][0]
    num_shares_start = start_amount // closing_price_start_date
    # total_share_count = 0
    mike_current_share = num_shares_start
    mike_carry_over = 0
    print("START NUM SHARE =", mike_current_share)
    for date, dividendCost in dividends_dict.items():
    #     for i, j in data['Close']:
    #
    #         print(data['Close'].values[i][j])
    # print(data['Close'].values)
        print(date, dividendCost)
        # print(data.loc[date])
        # closing_price_start_date = data.loc[start_date][0]
        # num_shares_start = start_amount // closing_price_start_date
        total_cost_without_dividend = num_shares_start * data.loc[date][0]
        dividend_cost_current_date = total_cost_without_dividend * dividendCost

        total_current_dividend_cost = (dividend_cost_current_date + total_current_dividend_cost)
        print(total_cost_without_dividend, " ", dividend_cost_current_date, " ", total_current_dividend_cost)

        print("currently, I have", mike_current_share,"(shares) and carry over", mike_carry_over, "$")
        mike_dividend_amount = mike_current_share * dividendCost
        print("this dividend payout", date, "I receive: $", mike_dividend_amount)
        mike_current_close = data.loc[date]["Close"].squeeze()
        print("current closing stock price of this date:", mike_current_close)
        mike_drip_shares = mike_dividend_amount // mike_current_close
        print("which turn out to be ", mike_drip_shares, "shares")
        mike_current_share += mike_drip_shares
        mike_carry_over += mike_dividend_amount - (mike_drip_shares * mike_current_close)
        print("the carry over amounts (left over that couldn't drip a share):", mike_carry_over)
        carry_over_share_num = mike_carry_over // mike_current_close
        print("currently I can buy: ", carry_over_share_num, " number of shares with the carry over.")
        print("BEFORE: ", mike_current_share)
        #if the carry over amount is bigger than the closing price for 1 share then I will add the number of shares I can
    #   buy with the carry over money and also update the carry over so the amount of shares we bought * closing price is
    #   deducted from the carry over

        print("Is: ", mike_carry_over, ">=", mike_current_close, "?")

        if mike_carry_over >= mike_current_close:
            print("YES.", mike_carry_over, ">=", mike_current_close)
            num_of_bought_shares_with_carryover = mike_carry_over // mike_current_close
            print("I can buy: ", num_of_bought_shares_with_carryover, "shares")
            # total_share_count = mike_current_share + carry_over_share_num
            mike_current_share = mike_current_share + carry_over_share_num

            mike_carry_over = mike_carry_over - (carry_over_share_num * mike_current_close)
            print("THE CARRY OVER PRICE NOW IS: ", mike_carry_over)
        else:
            print("NO. THE CARRY OVER PRICE DOES NOT EXCEED THE CLOSE PRICE.")
            mike_current_share = mike_current_share + carry_over_share_num
            print("THE CARRY OVER PRICE NOW IS: ", mike_carry_over)

        mike_current_total_value = mike_current_close * mike_current_share + mike_carry_over
        print("Currently including the shares I have bought with the leftover money I have: ", mike_current_share, " number of shares")
        print("At this point, the total current value for this stock position is:", mike_current_total_value)

    grandTotal = end_price * mike_current_share
    print(mike_current_total_value)
    print(mike_current_share)
    print(grandTotal)
    st.write("the total final value would be: ", grandTotal, " dollars(USD) with a total amount of: ", mike_current_share, "shares.")

    st.write("So, comparing Total investment return with and without dividend, which is ", grandTotal, " and ", grand_total_without_dividend, "you would earn an additional ", round(grandTotal - grand_total_without_dividend, 2), "dollars.")
# streamlit run StockAnalysis.py
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
