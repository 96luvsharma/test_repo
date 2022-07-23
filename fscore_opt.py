#Automated Piotroski's F-Score Calculation.
#Luv Sharma
#University of Siena, Italy.

import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import yahoo_fin.stock_info as si

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



