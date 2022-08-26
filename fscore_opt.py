#Automated Piotroski's F-Score Calculation.
#Luv Sharma
#University of Siena, Italy.

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

def get_statements(stocks):
    global balance_sheet
    global income_statement
    global cash_flow
    balance_sheet = si.get_balance_sheet(stocks)
    income_statement = si.get_income_statement(stocks)
    cash_flow = si.get_cash_flow(stocks)
    return balance_sheet, income_statement, cash_flow



def save_statements(stocks):
    get_statements(stocks)
    i = 0
    while i <1:
        balance_sheet.to_csv(f'{stocks}_Balance_Sheet.csv')
        income_statement.to_csv(f'{stocks}_Income_Statement.csv')
        cash_flow.to_csv(f'{stocks}_Cash_Flows.csv')
        i =+1

#Calculating Profitability Score.

def profitability():
    profit_score = 0
    totalassets = balance_sheet.loc['totalAssets']
    netincome = income_statement.loc['netIncome']
    operatingcash = cash_flow.loc['totalCashFromOperatingActivities']
    netincome_cy = netincome[0]
    operatingcash_cy = operatingcash[0]
    operatingcash_py = operatingcash[1]
    ROA_cy = netincome[0]/totalassets[0]
    ROA_py = netincome[1]/totalassets[1]
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
        


def leverage():

    leverage_score = 0

    #LongTermDebt
    long_debt = balance_sheet.loc['longTermDebt']
    long_debt_cy = long_debt[0]
    long_debt_py = long_debt[1]

    #Total Current Assets
    current_assets = balance_sheet.loc['totalCurrentAssets']
    current_assets_cy = current_assets[0]
    current_assets_py = current_assets[1]

    #Total Current Liabilities
    current_liab = balance_sheet.loc['totalCurrentLiabilities']
    current_liab_cy = current_liab[0]
    current_liab_py = current_liab[1]

    #Curretn Ratio for CY and PY
    Currentratio_cy = (current_assets_cy/current_liab_cy)
    Currentratio_py = (current_assets_py/current_liab_py)

    #Absence of Dilution (New shares issued or not)
    shares = balance_sheet.loc['totalStockholderEquity']
    shares_cy = shares[0]
    shares_py = shares[1]

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



def op_eff():
    operation = 0
    grossprofit = income_statement.loc['grossProfit']
    grossprofit_cy = grossprofit[0]
    grossprofit_py = grossprofit[1]
    
    #Asset Turnover Ratio
    totalassets = balance_sheet.loc['totalAssets']
    totalassets_cy = totalassets[0]
    totalassets_py = totalassets[1]
    
    totalrevenue = income_statement.loc['totalRevenue']
    totalrevenue_cy = totalrevenue[0]
    totalrevenue_py = totalrevenue[1]
    
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
    

def total_score():
    profit = profitability()
    lev = leverage()
    op = op_eff()
    total_score = (profit + lev + op)
    return total_score, profit, lev, op

def get_info(stocks):
    info = si.get_company_info(stocks)
    return info


def get_data(stock, start, end):
    data = pd.DataFrame()
    for i in range(len(stock)):
        # inter += 1
        p = si.get_data(stock[i], start_date= start, end_date=  end)['adjclose']
        data[stock[i]] = p
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


def negSR(weights, meanReturns, covMatrix, riskFreerate = 0):
    pReturns, pStd = pfolio_perf(weights, meanReturns, covMatrix)
    return -(pReturns - riskFreerate)/pStd


def maxSR(meanReturns, covMatrix, riskfreeRate = 0, constraintSet=(0,1)):
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


def minVar(meanReturns, covMatrix, constraintSet=(0,1)):
    "Minimize the porfolio variance by altering the weights/allocation of assets"
    numAssets = len(meanReturns)
    args = (meanReturns, covMatrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = constraintSet
    bounds = tuple(bound for asset in range (numAssets))
    result = sc.minimize(pfolio_var, numAssets*[1/numAssets], args = args, method='SLSQP', bounds = bounds, constraints= constraints)

    return result


def calculatedResults(meanReturns, covMatrix, riskfreerate=0, constraintSet =(0,1)):
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


def efficientOpt(meanReturns, covMatrix, returnTarget,constraintSet=(0,1)):
    "For each return target we want to optimize the porfolio for min variance."
    numAssets = len(meanReturns)
    args = (meanReturns, covMatrix)
    

    #"defining what the portfolio range is."
    constraints= ({'type':'eq', 'fun': lambda x: portfolioReturn(x, meanReturns, covMatrix) - returnTarget},
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = constraintSet
    bounds = tuple(bound for asset in range(numAssets))
    effopt = sc.minimize(pfolio_var , numAssets*[1/numAssets], args = args, method='SLSQP', bounds = bounds, constraints = constraints)

    return effopt


def EF_graph(meanReturns, covMatrix, riskFreeRate=0, constraintSet=(0,1)):
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

    meanReturns, covMatrix = get_data(stockList, start = startDate, end = endDate)

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
    dax_tickers = sorted(table['Ticker symbol'].tolist())

    return dax_tickers
