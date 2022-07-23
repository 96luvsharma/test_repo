from ast import Index
from operator import index
import yahoo_fin.stock_info as si
import fscore_opt as fs
import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_option_menu import option_menu
import time

st.set_page_config(layout="wide")


sp500 = fs.sp500()

nav = option_menu(menu_title = 'Navigation',
    options=['Portfolio Dashboard','Multiple Firm F-Score', 'Single Firm F-Score', 'About Me' ],
    icons=['cash-coin','file-bar-graph-fill','file-binary-fill','file-person'],
    menu_icon= "list",
    default_index=0,
    orientation= 'horizontal',
    styles={
    "container": {"padding": "0!important"},
    "icon": {"color": "white", "font-size": "20px"}, 
    }
    )




if nav == 'Multiple Firm F-Score':
    selection = st.multiselect('Select the stock tickers', sp500)
    btn = st.button('Calculate')

    if btn:
        a = 1
        name = list(selection)
        df = pd.DataFrame()
        for i in selection:
            statements = fs.get_statements(i)  
            total, profit, lev, op = fs.total_score()
            #company = [i]
            score = [total]
            # fscore = pd.DataFrame()
            # fscore = pd.DataFrame(list(zip(company, score)),columns=cols)
            df = df.append(score)
            a += 1

        df.set_index([selection], inplace=True)
        df.columns = ['F-Score']
        st.subheader('Total score of the selected firms is as follows out of 9.')
        st.bar_chart(df,height=400)
            

    
if nav == 'Single Firm F-Score':
    
    selection = st.selectbox('Select the stock ticker', sp500)
    btn = st.button('Calculate')

    if btn:
        statements = fs.get_statements(selection)
        total, profit, lev, op = fs.total_score()
        st.header(f'The F-Score for {selection} is {total}/9.')    
        st.subheader(f'1. The Profitability score for {selection} is {profit}.')
        st.subheader(f'2. The Leverage score for {selection} is {lev}.')
        st.subheader(f'3. The Operating Effeciency Score for {selection} is {op}')

if nav == 'Portfolio Dashboard':
    st.title('Portfolio Dashboard')

    dropdown = st.multiselect('Pick your assets- (please select more than one.)', sp500)

    start = st.date_input('Start', value = pd.to_datetime('2021-01-01'))
    end = st.date_input('End', value = pd.to_datetime('today'))

    def relativeret(df):
        rel = df.pct_change()
        cumret = (1+rel).cumprod()-1
        cumret = cumret.fillna(0)
        return cumret

    btn = st.button('Show Portfolio')

    if btn:
        df = relativeret(yf.download(dropdown, start, end)['Adj Close'])
        df['Portfolio'] = df.mean(axis = 1)
        st.header(f'Returns of {dropdown}')
        st.line_chart(df)
        port_ret = df['Portfolio'].iloc[-1]
        tot_ret = port_ret*100
        st.subheader(f'Total return of the portfolio was {tot_ret:.2f}%.')
        



if nav =='About Me':
    st.title('About Me!')
    st.subheader('Created by: Luv Sharma')
    st.subheader('Reach me at: 96.luvsharma@gmail.com')
    st.subheader('Profession: Student (M.Sc Finance)')
    st.subheader('Where: University of Siena, Italy')
    st.write("**Please select an option from the sidebar to know about how each section of the web app works, Thank you for checking it out!**")

    options = ['About Portfolio Dashboard','About F-Score' ,'']
    st.sidebar.title('Sidebar')
    sidebar = st.sidebar.selectbox('Menu', options,index= 2)
    
    
    if sidebar == 'About F-Score':
        st.header('About the F-Score')
        st.subheader("What is the Piotroski F-Score? ")
        st.write("The Piotroski score is a discrete score between 0-9 that reflects nine criteria used to determine the strength of a firm's financial position. It was originally developed to give investors an idea as to which companies are the strongest when grouped with value stocks. This is done to help highlight the best and worst performers before adding these stocks to a portfolio. The financial strength of the companies is determined by applying these nine accounting-based restrictions and awarding one point for each restriction that a stock passes:")
        st.subheader("A. Profitability")
        st.write("1. Net Income: Give 1 point if Net income  in the current period is positive; otherwise give 0 points.")
        st.write("2. Operating cash flow: Give 1 point if Cash flow from operations in the current period is positive; otherwise give 0 points.")
        st.write("3. Return on assets: Give 1 point if the current period's Return on assets (ROA) is higher when compared to the ROA of the previous period; otherwise give 0 points.")
        st.write("4. Quality of earnings: Give 1 point if the Cash flow from operations exceeds Net income before Extraordinary items; otherwise give 0 points.")
        st.subheader("B. Leverage, Liquidity, and Sources of Funds")
        st.write("1. Decrease in Leverage: Give 1 point if there is a lower ratio of Long term debt in the current period compared to the value in the previous period; otherwise give 0 points.")
        st.write("2. Increase in Liquidity: Give 1 point if the current period's Current ratio is higher when compared to the Current ratio of the previous period; otherwise give 0 points.")
        st.write("3. Absence of Dilution: Give 1 point if the firm did not issue new shares / equity in the preceding period; otherwise give 0 points.")
        st.subheader("C. Operating efficiency")
        st.write("1. Give 1 point if the current period's Gross margin is higher compared to the Gross margin of the previous period; otherwise give 0 points.")
        st.write("2. Asset turnover: Give 1 point if there is a higher Asset turnover ratio period on period (as a measure of productivity); otherwise give 0 points.")
        st.subheader("Meaning")
        st.write("If a company has a score of 8 or 9, it is considered a good value. If the score adds up to between 0-2 points, the stock is considered weak.")

    if sidebar == 'About Portfolio Dashboard':
        st.header('About Portfolio Dashboard')
        st.write("**The Portfolio is made by calculating the relative return of each stock at first and then converting it to cumulative return, the graph shows the return of each stock in percentages while the overall portfolio return is the average of the total return combined.**")