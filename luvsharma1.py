   st.title("Historical Effecient Frontier Calculation.")


    X = st.selectbox('Markets', options=['Please select a market from this dropdown menu.','CAC40 (^FCHI)', 'DOW30 (^DJI)','DAX40 (^GDAXI)','FTSE MIB Index (^FTSEMIB.MI)','NASDAQ-100 (^NSC)', 'FTSE100 (^FTSE)' ,'S&P500 (^GSPC)'],index=0)

    btn = st.button(' Calculate Efficient Frontier ')
    if btn:
        
        
        tickers = []
        if len(X) > 1: 
            if X == 'S&P500 (^GSPC)':
                tickers = fs.tickers_sp500()
            elif X == 'DOW30 (^DJI)':
                tickers = si.tickers_dow()
            elif X == 'NASDAQ-100 (^NSC)':
                tickers = fs.tickers_nasdaq100()
            elif X =='FTSE100 (^FTSE)':
                tickers = fs.tickers_ftse100()
            elif X == 'FTSE MIB Index (^FTSEMIB.MI)':
                tickers = fs.tickers_mib()
            elif X == 'DAX40 (^GDAXI)':
                tickers = fs.tickers_dax()
            elif X == 'CAC40 (^FCHI)':
                tickers = fs.tickers_cac40()
            else :
                b = 1 #Random place holder.


        if 1 < len(X) < 40 :

            st.text("Please wait a few minutes and scroll down for details once the process is completed. ")
            st.text("It may take 1-15 minutes depending on the market selected. (Takes the longest for S&P 500 \U0001F605)")
            st.write("Please feel free to reach out as the projects are made using web scraping and even small changes to the sources like yahoo finance and wikipedia websites may break the process. Thank you!")
            with hc.HyLoader('Fetching live data from yahoo...',hc.Loaders.pacman):

                weight = []

                
                for i in range(len(tickers)):
                    weight.append(1/len(tickers))
    
                weights = np.array(weight)
  
                Returns, Std, mWeights, ResultGraph, SR, RET = fs.eff_front(tickers,weights, graph= True)
            

                Frame = pd.DataFrame()
                Frame['Stocks'] = tickers
                Frame['Weights'] = mWeights
                Frame['Weights'] = round(Frame['Weights']*100,2)




            
                Frame1 = Frame[Frame.Weights > 0 ]
                # Frame1.to_csv('./Frame')

                ind = []
                for i in range(len(Frame1['Weights'])):
                    i = i+1
                    ind.append(i)
                
                FinalFrame = pd.DataFrame(columns=['Ticker','Weights'])
                
                FinalFrame['Ticker'] = Frame1['Stocks']
                
                #company = list()
                
                names = FinalFrame['Ticker'].to_list()
            
                # for i in range(0,len(names)):
                #     name = str()
                #     name = fs.get_company_name(names[i])  
                #     company.append(name)  
                st.success("Done!")
                st.plotly_chart(ResultGraph, use_container_width=True)
                # FinalFrame['Company'] = company
                FinalFrame['Weights'] = Frame1['Weights']
                FinalFrame.set_index([pd.Index(ind)],inplace=True)    
                t = len(FinalFrame['Weights'])
                sharperatios = RET/SR
                st.text(f'Sharpe ratio for this distribution = {sharperatios:.2f}')
                st.table(FinalFrame.style.format(subset=['Weights'], formatter="{:.2f}"))
                st.download_button(label='Download data as CSV',data=fs.convert_csv(FinalFrame),file_name=f'{X} Effecient Frontier.csv',mime='text/csv')
                st.text(f'Total Number of Assets invested in = {t}')
                st.text("Calculated over the period of 5 years or 1260 days in total.")
                st.text(f"Max Returns = {RET}")
                st.text(f"Max Volatility = {SR}")
            
            
        else:
            st.text("Please select a market from the select box above.")
