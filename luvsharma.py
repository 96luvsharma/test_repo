#Luv Sharma
#M.Sc. Finance
#University of Siena, Italy.

import yahoo_fin.stock_info as si
import fscore_opt as fs
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import datetime as dt
import numpy as np
import time


prog = 0

st.set_page_config(page_title="Luv Sharma",page_icon="chart_with_upwards_trend",layout="wide",)


sp500 = fs.sp500()
nasdaq = si.tickers_nasdaq()
dax40 = fs.tickers_dax()
markets = ["Select a market to get the stock tickers","S&P500","NASDAQ", "DAX40"]

nav = option_menu(menu_title = 'Navigation',
    options=['Efficient Frontier','Multiple Firm F-Score', 'Single Firm F-Score','Portfolio Dashboard', 'About Me' ],
    icons=['pie-chart-fill','cash-coin','file-bar-graph-fill','file-binary-fill','file-person'],
    menu_icon= "list",
    default_index=0,
    orientation= 'horizontal',
    styles={
    "container": {"padding": "0!important"},
    "icon": {"color": "white", "font-size": "20px"}, 
    }
    )




if nav == 'Multiple Firm F-Score':
#     sel = st.selectbox("Markets", options=markets)
#     if sel == 'S&P500':
    selection = st.multiselect('Please select multiple stocks to analyze.',sp500)
#     elif sel == "NASDAQ":
#         selection = st.multiselect('Please select multiple stocks to analyze.',nasdaq)
#     elif sel == 'DAX40':
#         selection = st.multiselect('Please select multiple stocks to analyze.',dax40)
#     else:
#         b=0
    
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

if nav == 'Efficient Frontier':
    st.title("Historical Effecient Frontier Calculation.")


    X = st.selectbox('Markets', options=['Please select a market from this dropdown menu.','S&P500 (^GSPC)', 'DOW30 (^DJI)','NASDAQ-100 (^NSC)','DAX40 (^GDAXI)' ,'FTSE100 (^FTSE)' ],index=0)

    btn = st.button(' Calculate Efficient Frontier ')
    if btn:
        
        
        tickers = []
        if len(X) > 1: 
            if X == 'S&P500 (^GSPC)':
                tickers = si.tickers_sp500()
            elif X == 'DOW30 (^DJI)':
                tickers = si.tickers_dow()
            elif X == 'NASDAQ-100 (^NSC)':
                tickers = fs.tickers_nasdaq100()
            elif X =='FTSE100 (^FTSE)':
                tickers = fs.tickers_ftse100()
            # elif X == 'FTSE250 (^FTMC)':
                # tickers = fs.tickers_ftse250()
            # elif X == 'IBOVESPA (^BVSP)':
                # tickers = fs.tickers_ibovespa()
            elif X == 'DAX40 (^GDAXI)':
                tickers = fs.tickers_dax()
            # elif X == 'NIFTYBANK':
            #     tickers = si.tickers_niftybank()
            else :
                b = 1 #Random place holder.


        if 1 < len(X) < 40 :
#             my_bar = st.progress(0)
            st.text("Please wait a few minutes and scroll down for details once the process is completed. ")
            st.text("It may take 1-15 minutes depending on the market selected.")
            with st.spinner(f"Collecting live data upto today for {X}"):
                time.sleep(5)
                weight = []

                # if tickers == 'FTSE100':
                #     tickers +'.L'
                # if tickers == 'FTSE250':
                #     tickers +'.L'

                # for i in range(len(tickers)):
                #     x = len(tickers)
                #     y = 1/x
                #     weight.append(y)
                for i in range(len(tickers)):
                    weight.append(1/len(tickers))
    #             my_bar.progress(10)
                weights = np.array(weight)
    #             my_bar.progress(15)
#                 """Calculating..."""
                Returns, Std, mWeights, ResultGraph, SR, RET = fs.eff_front(tickers,weights, graph= True)
            st.success("Done!")
#             my_bar.progress(75)

            # l=[]
            # newWeights= []
            # newList=[]
            # for i in range(len(mWeights)):
            #     if mWeights[i] < 0.001:
            #         l.append(i)

            #     else:
            #         newWeights.append(mWeights[i])
            #         newList.append(tickers[i])

            # newWeights = np.array(newWeights)

            # my_bar.progress(65)

            # Returns, Std, Weights, NewGraph, NSR, NRET = fs.eff_front(newList,newWeights, graph=True)

            Frame = pd.DataFrame()
            Frame['Stocks'] = tickers
            Frame['Weights'] = mWeights
            Frame['Weights'] = round(Frame['Weights']*100,2)




            st.plotly_chart(ResultGraph, use_container_width=True)
            Frame1 = Frame[Frame.Weights > 0 ]


            ind = []
            for i in range(len(Frame1['Weights'])):
                i = i+1
                ind.append(i)

            # Frame1.reindex(ind)
            # Frame1.reset_index(drop=True)
            Frame1.set_index([pd.Index(ind)],inplace=True)
            # Frame1.drop('index',axis=1,inplace=True)
            t = len(Frame1['Weights'])
            st.table(Frame1)
#             my_bar.progress(90)
            st.text(f'Total Number of Assets invested in = {t}')
            st.text("Calculated over the period of 5 years or 1260 days in total.")
            st.text(f"Max Returns = {RET}")
            st.text(f"Max Volatility = {SR}")
#             my_bar.progress(100)
            
        else:
            st.text("Please select a market from the select box above.")

