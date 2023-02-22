#Luv Sharma
#University of Siena, Italy.


import re
import json
import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import yahoo_fin.stock_info as si
import numpy as np
from scipy import optimize as sc
import datetime as dt
from plotly import graph_objects as go
import yfinance as yf
from yahooquery import Ticker

def scraper(stock):
    try:
        company = Ticker(stock)
        BS = company.balance_sheet()
        IS = company.income_statement()
        CF = company.cash_flow()

    except:
        Exception
        IndexError
        try:
            company = yf.Ticker(stock)
            BS = company.balance_sheet()
            IS = company.income_statement()
            CF = company.cash_flow()
        except:
            return ValueError('Scraper not working!')
    
    return BS.T, IS.T, CF.T


def convert_csv(df):

    return df.to_csv().encode('utf-8')

def dow():
    dow = si.tickers_dow()
    return dow

def ftse100():
    ftse100 = si.tickers_ftse100()
    return ftse100
    
def ftse250():
    ftse250 = si.tickers_ftse250()
    return ftse250
    
def ibovespa():
    ibovespa = si.tickers_ibovespa()
    return ibovespa
    
def nasdaq():
    nasdaq = si.tickers_nasdaq()
    return nasdaq
    
def nifty50():
    nifty50 = si.tickers_nifty50()
    return nifty50
    
def niftybank():
    niftybank = si.tickers_niftybank
    return niftybank
    #index = [dow, ftse100, ftse250, ibovespa, nasdaq, nifty50, niftybank, sp500]

def sp500():
    sp500 = si.tickers_sp500()
    return sp500

def company_info(firm):
    
    analysis = si.get_analysts_info(firm)
    company = si.get_stats_valuation(firm)
    stats = si.get_stats(firm)
    liveprice = si.get_live_price(firm)
    earningdate = si.get_next_earnings_date(firm)

    return analysis, company, stats, earningdate, liveprice

def t_sp500(): #Longer method to Fetch Ticker Symbols.
    global company_list
    #Scraping the list of companies in S&P500 from wikipedia.

    wiki = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    response_1 = requests.get(wiki) #fetching the data

    wiki_page = BeautifulSoup(response_1.text, 'html.parser' )

    #Storing the table with company info in company_table variable
    table_id = 'constituents'

    company_table = wiki_page.find('table', attrs={'id': table_id})

    #Creating dataframe with company info and storing it in csv format

    df = pd.read_html(str(company_table))
    df[0].to_csv('S&P500 Companies Info.csv')

    #Creating Dataframe from csv

    csv_df = pd.read_csv('S&P500 Companies Info.csv')
    company_list = csv_df['Symbol'].to_list()
    return company_list
    
global stock 

def income_st(stock): #Fetching Income Statement
    tick = yf.Ticker(stock)
    IS = tick.get_income_stmt()
    return IS

def bal_sht(stock): #Fetching Balance Sheet
    tick = yf.Ticker(stock)
    BS = tick.get_balance_sheet()
    return BS

def cash_flw(stock): #Fetching Cash Flow
    tick = yf.Ticker(stock)
    CF = tick.get_cash_flow()
    return CF


def get_statements(stocks):
    BS, IS, CF = scraper(stocks)
    balance_sheet = BS.T
    income_statement = IS.T
    cash_flow = CF.T
    return balance_sheet, income_statement, cash_flow



def save_statements(stocks):
    balance_sheet, income_statement, cash_flow = get_statements(stocks)
    i = 0
    while i <1:
        balance_sheet.to_csv(f'{stocks}_Balance_Sheet.csv')
        income_statement.to_csv(f'{stocks}_Income_Statement.csv')
        cash_flow.to_csv(f'{stocks}_Cash_Flows.csv')
        i =+1

#Calculating Profitability Score.

def profitability(balance_sheet, income_statement, cash_flow):
    profit_score = 0
    totalassets = balance_sheet.loc['TotalAssets']
    netincome = income_statement.loc['NetIncome']
    operatingcash = cash_flow.loc['CashFlowFromContinuingOperatingActivities']
    netincome_cy = netincome[-1]
    operatingcash_cy = operatingcash[-1]
    operatingcash_py = operatingcash[-2]
    ROA_cy = netincome[-1]/totalassets[-1]
    ROA_py = netincome[-2]/totalassets[-2]
    Qualityofearnings = operatingcash_cy - netincome_cy
    
    #Taking netincome into consideration.
    if netincome_cy > 0:
        profit_score += 1
    else :
        profit_score += 0
        
    #Taking Operating Cash into consideration.
    if operatingcash_cy >0:
        profit_score += 1
    else:
        profit_score += 0
    
    #Taking Change in ROA into consideration.    
    if (ROA_cy - ROA_py)>0:
        profit_score += 1
    else:
        profit_score += 0
        
    #Taking diff. between Operating Cash and Net Income for the current year.
    if (operatingcash_cy - netincome_cy) > 0 :
        profit_score += 1
    else:
        profit_score += 0
    
    return profit_score
        


def leverage(balance_sheet, income_statement, cash_flow):

    leverage_score = 0

    #LongTermDebt
    long_debt = balance_sheet.loc['LongTermDebt']
    long_debt_cy = long_debt[-1]
    long_debt_py = long_debt[-2]

    #Total Current Assets
    current_assets = balance_sheet.loc['CurrentAssets']
    current_assets_cy = current_assets[-1]
    current_assets_py = current_assets[-2]

    #Total Current Liabilities
    current_liab = balance_sheet.loc['CurrentLiabilities']
    current_liab_cy = current_liab[-1]
    current_liab_py = current_liab[-2]

    #Curretn Ratio for CY and PY
    Currentratio_cy = (current_assets_cy/current_liab_cy)
    Currentratio_py = (current_assets_py/current_liab_py)

    #Absence of Dilution (New shares issued or not)
    shares = balance_sheet.loc['StockholdersEquity']
    shares_cy = shares[-1]
    shares_py = shares[-2]

    #Scoring Parameters
    if long_debt_py - long_debt_cy > 0:
        leverage_score += 1
    else:
        leverage_score += 0

    if Currentratio_cy > Currentratio_py :
        leverage_score += 1
    else:
        leverage_score += 0

    if shares_py > shares_cy:
        leverage_score += 1
    else:
        leverage_score += 0

    return leverage_score



def op_eff(balance_sheet, income_statement, cash_flow):
    operation = 0
    grossprofit = income_statement.loc['GrossProfit']
    grossprofit_cy = grossprofit[-1]
    grossprofit_py = grossprofit[-2]
    
    #Asset Turnover Ratio
    totalassets = balance_sheet.loc['TotalAssets']
    totalassets_cy = totalassets[-1]
    totalassets_py = totalassets[-2]
    
    totalrevenue = income_statement.loc['TotalRevenue']
    totalrevenue_cy = totalrevenue[-1]
    totalrevenue_py = totalrevenue[-2]
    
    assetturn_cy = (totalassets_cy/totalrevenue_cy)
    assetturn_py = (totalassets_py/totalrevenue_py)
    
    grossmargin_cy = grossprofit_cy/totalrevenue_cy
    grossmargin_py = grossprofit_py/totalrevenue_py
    
    
    if grossmargin_cy > grossmargin_py:
        operation += 1
    else:
        operation += 0
    
    if assetturn_cy > assetturn_py:
        operation += 1
    else:
        operation += 0
        
    return operation
    

def total_score(stock):
    BS, IS, CF = get_statements(stocks=stock)
    balance_sheet, income_statement, cash_flow = BS.T, IS.T, CF.T
    profit = profitability(balance_sheet, income_statement, cash_flow)
    lev = leverage(balance_sheet, income_statement, cash_flow)
    op = op_eff(balance_sheet, income_statement, cash_flow)
    total_score = (profit + lev + op)
    return total_score, profit, lev, op

def get_info(stocks):
    info = si.get_company_info(stocks)
    return info


def get_data(stock):
    data = pd.DataFrame()
    for i in range(len(stock)):
        # inter += 1
        s = stock[i]
        a = yf.Ticker(s).history(period='5y',interval='1d')['Close']
        data[stock[i]] = a
    # stockData = pdr.get_data_yahoo(stock, start = start, end = end)
    # stockData = stockData['Adj Close']
    returns = data.pct_change()
    meanReturns = returns.mean()
    covMatrix = returns.cov()
    
    # stockData = si.get_data(stock, start = start, end = end)
    # stockData = stockData['adjclose']
    # returns = stockData.pct_change()
    # meanReturns = returns.mean()
    # covMatrix = returns.cov()
    
    return meanReturns, covMatrix


def pfolio_perf(weights, meanReturns, covMatrix):
    rets = np.sum(meanReturns*weights)*252
    std = np.sqrt(np.dot(weights.T, np.dot(covMatrix, weights))*np.sqrt(252))
    return rets, std


def negSR(weights, meanReturns, covMatrix, riskFreerate = 0.02):
    pReturns, pStd = pfolio_perf(weights, meanReturns, covMatrix)
    return -(pReturns - riskFreerate)/pStd


def maxSR(meanReturns, covMatrix, riskfreeRate = 0.02, constraintSet=(0.00,1)):
    'Minimize the negative Sharpe Ratio by altering the weights of the porfolio'
    numAssets = len(meanReturns)
    args = (meanReturns, covMatrix, riskfreeRate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = constraintSet
    bounds = tuple(bound for asset in range (numAssets))
    result = sc.minimize(negSR, numAssets*[1/numAssets], args = args, method='SLSQP', bounds = bounds, constraints= constraints)

    return result


def pfolio_var(weights, meanReturns, covMatrix):
    return pfolio_perf(weights, meanReturns, covMatrix)[1]


def minVar(meanReturns, covMatrix, constraintSet=(0.00,1)):
    "Minimize the porfolio variance by altering the weights/allocation of assets"
    numAssets = len(meanReturns)
    args = (meanReturns, covMatrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = constraintSet
    bounds = tuple(bound for asset in range (numAssets))
    result = sc.minimize(pfolio_var, numAssets*[1/numAssets], args = args, method='SLSQP', bounds = bounds, constraints= constraints)

    return result


def calculatedResults(meanReturns, covMatrix, riskfreerate=0.02, constraintSet =(0.00,1)):
    "Read in mean, cov matrix, and other financial  information Output"
    
    #Max SR Portfolio
    maxSR_portfolio = maxSR(meanReturns, covMatrix)
    maxSR_returns, maxSR_std = pfolio_perf(maxSR_portfolio['x'], meanReturns, covMatrix)
    maxSR_allocation = pd.DataFrame(maxSR_portfolio['x'], index =meanReturns.index, columns=['allocation'])
    maxSR_allocation.allocation = [round(i*100,0) for i in maxSR_allocation.allocation]
    
    #Min Volatility portfolio
    minVol_portfolio = minVar(meanReturns, covMatrix)
    minVol_returns, minVol_std = pfolio_perf(minVol_portfolio['x'], meanReturns, covMatrix)
    minVol_allocation = pd.DataFrame(minVol_portfolio['x'], index =meanReturns.index, columns=['allocation'])
    minVol_allocation.allocation = [round(i*100,0) for i in minVol_allocation.allocation]
    
    # Efficient Frontier
    efficientList = []
    targetReturns = np.linspace(minVol_returns, maxSR_returns, 20)
    for target in targetReturns:
        efficientList.append(efficientOpt(meanReturns, covMatrix, target)['fun'])
    
    maxSR_returns, maxSR_std = round(maxSR_returns*100,2), round(maxSR_std*100, 2)
    minVol_returns, minVol_std = round(minVol_returns*100,2), round(minVol_std*100,2)


    return maxSR_returns, maxSR_std, maxSR_allocation, minVol_returns, minVol_std, minVol_allocation, efficientList, targetReturns


def portfolioReturn(weights, meanReturns, covMatrix):
        return pfolio_perf(weights, meanReturns, covMatrix)[0]


def efficientOpt(meanReturns, covMatrix, returnTarget,constraintSet=(0.00,1)):
    "For each return target we want to optimize the porfolio for min variance."
    numAssets = len(meanReturns)
    args = (meanReturns, covMatrix)
    

    #"defining what the portfolio range is."
    constraints= ({'type':'eq', 'fun': lambda x: portfolioReturn(x, meanReturns, covMatrix) - returnTarget},
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = constraintSet
    bounds = tuple(bound for asset in range(numAssets))
    effopt = sc.minimize(pfolio_var , numAssets*[1/numAssets], args = args, method='SLSQP', bounds = bounds, constraints = constraints)#, options={'maxiter':5})

    return effopt


def EF_graph(meanReturns, covMatrix, riskFreeRate=0.02, constraintSet=(0.00,1)):
    """Return a graph ploting the min vol, max sr and efficient frontier"""
    maxSR_returns, maxSR_std, maxSR_allocation, minVol_returns, minVol_std, minVol_allocation, efficientList, targetReturns = calculatedResults(meanReturns, covMatrix, riskFreeRate, constraintSet)
    FINALSR = maxSR_std
    FINALRET = maxSR_returns
    #Max SR
    MaxSharpeRatio = go.Scatter(
        name='Maximium Sharpe Ratio',
        mode='markers',
        x=[maxSR_std],
        y=[maxSR_returns],
        marker=dict(color='red',size=14,line=dict(width=3, color='white'))
    )

    #Min Vol
    MinVol = go.Scatter(
        name='Mininium Volatility',
        mode='markers',
        x=[minVol_std],
        y=[minVol_returns],
        marker=dict(color='green',size=14,line=dict(width=3, color='white'))
    )

    #Efficient Frontier
    EF_curve = go.Scatter(
        name='Efficient Frontier',
        mode='lines',
        x=[round(ef_std*100, 2) for ef_std in efficientList],
        y=[round(target*100, 2) for target in targetReturns],
        line=dict(color='white', width=4, dash='dashdot')
    )

    data = [MaxSharpeRatio, MinVol, EF_curve]

    layout = go.Layout(
        title = 'Portfolio Optimisation with the Efficient Frontier',
        yaxis = dict(title='Annualised Return (%)'),
        xaxis = dict(title='Annualised Volatility (%)'),
        showlegend = True,
        legend = dict(
            x = 0.75, y = 0, traceorder='normal',
            bgcolor='black',
            bordercolor='white',
            borderwidth=2),
        width=800,
        height=600)
    
    fig = go.Figure(data=data, layout=layout)
    return fig, FINALSR, FINALRET


def eff_front(stockList,weights, graph = bool):
    
    n = len(stockList)

    # for i in range(n):
    #     b = 1/n
    #     weight.append(b)

    # weights = np.array(weight)

    endDate = dt.datetime.now()
    startDate = endDate - dt.timedelta(days=1260)
    data = pd.DataFrame()

    meanReturns, covMatrix = get_data(stockList)

    returns, std = pfolio_perf(weights, meanReturns, covMatrix)

    result = maxSR(meanReturns, covMatrix)
    maxRatio, maxWeight = result['fun'], result['x']


    minvarResult = minVar(meanReturns, covMatrix)
    minVariance, minWeights = minvarResult['fun'], minvarResult['x']

    returns, std = pfolio_perf(minWeights, meanReturns, covMatrix)
    
    if graph == True:
        ResultGraph, FSR, FRET = EF_graph(meanReturns,covMatrix)
    else :
        ResultGraph = None
    
    return returns, std , minWeights, ResultGraph, FSR, FRET

def tickers_dax(details = False):
    site = "https://en.wikipedia.org/wiki/DAX#Components"

    table = pd.read_html(site, attrs = {"id":"constituents"})[0]

    if details:
        return table
    dax_tickers = sorted(table['Ticker'].tolist())

    return dax_tickers

def tickers_nasdaq100(details = False):
    site = "https://en.wikipedia.org/wiki/Nasdaq-100#Components"

    table = pd.read_html(site, attrs = {"id":"constituents"})[0]

    if details:
        return table
    nas100_tickers = sorted(table['Ticker'].tolist())

    return nas100_tickers

def tickers_ftse100(details = False):
    ftse100_tickers = list()
    site = "https://en.wikipedia.org/wiki/FTSE_100_Index#Constituents"

    table = pd.read_html(site, attrs = {"id":"constituents"})[0]

    if details:
        return table
    ticks = sorted(table['Ticker'].tolist())
    for i in range(len(ticks)):
        ftse100_tickers.append(ticks[i]+'.L')

    return ftse100_tickers

def tickers_ftse250(details = False):
    ftse250_tickers = list()
    site = "https://en.wikipedia.org/wiki/FTSE_250_Index#Constituents"

    table = pd.read_html(site, attrs = {"id":"constituents"})[0]

    if details:
        return table
    ticks = sorted(table['Ticker[4]'].tolist())
    for i in range(len(ticks)):
        ftse250_tickers.append(ticks[i]+'.L')

    return ftse250_tickers

def tickers_ibovespa(details = False):
    ibovespa_tickers = list()
    site = "https://en.wikipedia.org/wiki/List_of_companies_listed_on_B3"

    table = pd.read_html(site, attrs = {"id":"constituents"})[0]

    if details:
        return table
    ticks = sorted(table['Ticker'].tolist())
    for i in range(len(ticks)):
        ibovespa_tickers.append(ticks[i]+'.SA')

    return ibovespa_tickers


def tickers_cac40(details = False):
    #CAC40(^FCHI) french index.
    cac40_tickers = list()
    site = "https://en.wikipedia.org/wiki/CAC_40#Composition"

    table = pd.read_html(site, attrs = {"id":"constituents"})[0]

    if details:
        return table
    ticks = sorted(table['Ticker'].tolist())
    cac40_tickers = ticks
    # for i in range(len(ticks)):
    #     cac40_tickers.append(ticks[i]+'.PA')

    return cac40_tickers

def tickers_mib(details = False):
    #FTSE-MIB(FTSEMIB.MI) italian index-milan.
    mib_tickers = list()
    site = "https://en.wikipedia.org/wiki/FTSE_MIB#Components"

    table = pd.read_html(site, attrs = {"id":"constituents"})[0]

    if details:
        return table
    ticks = sorted(table['Ticker'].tolist())
    mib_tickers = ticks
    # for i in range(len(ticks)):
    #     cac40_tickers.append(ticks[i]+'.PA')

    return mib_tickers

def _parse_json(url, headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}):
    html = requests.get(url=url, headers = headers).text

    json_str = html.split('root.App.main =')[1].split(
        '(this)')[0].split(';\n}')[0].strip()
    
    try:
        data = json.loads(json_str)[
            'context']['dispatcher']['stores']['QuoteSummaryStore']
    except:
        return '{}'
    else:
        # return data
        new_data = json.dumps(data).replace('{}', 'null')
        new_data = re.sub(r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)

        json_info = json.loads(new_data)

        return json_info

def get_company_name(ticker):
    '''Scrape the company information and return a table of the officers

       @param: ticker
    '''
    site = f"https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}"
    json_info = _parse_json(site)
    json_info = json_info["price"]["longName"]
   #  info_frame = pd.DataFrame.from_dict(json_info)
   #  info_frame = info_frame.set_index("name")
    return json_info

def _parse_table(json_info):

    df = pd.DataFrame(json_info)
    
    if df.empty:
        return df
    
    del df["maxAge"]

    df.set_index("endDate", inplace=True)
    df.index = pd.to_datetime(df.index, unit="s")
 
    df = df.transpose()
    df.index.name = "Breakdown"

    return df

