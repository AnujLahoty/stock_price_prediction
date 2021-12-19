# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 16:33:42 2020

@author: Anuj, Abhijeeth, Aditya, Sadaqhath
"""


#############################################################

import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style
import matplotlib.animation as animation
import pandas as pd
import numpy as np
import urllib
import json
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.ticker as ticker
from mpl_finance import candlestick2_ohlc
import tweepy
#from tweepy import Stream
from tweepy import OAuthHandler
#from tweepy.streaming import StreamListener
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas_datareader.data as web
from datetime import timedelta
import numpy
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
import math
from sklearn import preprocessing
from datetime import datetime


print(datetime.today())

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Helvetica", 10)
SMALL_FONT= ("Helvetica", 8)

style.use('ggplot')

f = plt.figure()


company_name = 'Microsoft corporation'    
link = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=TPVVLSFMNUVDDO82'
data_time_span = 100
symbol = 'MSFT'
candleWidth = 0.5
chartLoad = True
topIndicator = 'none'
middleIndicator = 'none'
bottomIndicator = 'none'
light_color = '#00A3E0'
dark_color = '#183A54'
candel_stick_graph = False
api_time_span = '5min'
time_span_choice = 'none'
algorithm_choice = 'none'
period_to_put_in_link = 1
ema_or_sma = 'sma'
rsi_or_macd = 'rsi'
time_periods_to_calculate_ema_or_sma = 14
time_periods_to_calculate_rsi = 14
dateList = []
dateList_of_sma = []
closedPriceList = []
volumeList = []
sma_values = []
rsi_values = []
dateList_of_rsi = []
#company_name_for_sentiment = "Tesla" # Not required
sentiments = []
tweets = []
time_frame = "None"
company_choice_for_prediction = "None"


#consumer key, consumer secret, access token, access secret.
ckey = "aI7F7LLc3e9MK8sE0izk5PZpt"
csecret = "zkpK52HcOTABeiH5nnJpn4BKhHmQx6lZCMTU6Z48wOH0fByBbV"
atoken = "1171759399456501760-zI8gjyAAk1BZrmJ8LNKizFGDcKApc3"
asecret = "3PSZWVL9BPvYf73wFigCheoe0hcXXFazGvB37Ii2xTzwt"
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)


def popupmsg(msg):
    
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def get_tweets(company):
    
    print(company)
    global sentiments
    global tweets
    
    
    class MyStreamListener(tweepy.StreamListener):
        
        def __init__(self, time_limit=60):
            self.start_time = time.time()
            self.limit = time_limit
            super(MyStreamListener, self).__init__()
    
        def on_data(self, data):
            if (time.time() - self.start_time) < self.limit:
                all_data = json.loads(data)
    
                tweet = all_data["text"]
        
                #username = all_data["user"]["screen_name"]
                sentiments.append(sia.polarity_scores(tweet)['compound'])
                tweets.append(tweet)
                print(tweet)
                #print((username,tweet))
                return True
    
            else:
                return False
    
    myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(time_limit=13))
    if company == "Tesla":
        myStream.filter(track=["Tesla"])
        
    elif company == "Microsoft":
        myStream.filter(track=["Microsoft"])
        
    elif company == "Virgin Galactic":
        myStream.filter(track=["Virgin Galactic"])
    
    elif company == "S And P 500":
        myStream.filter(track=["S And P 500"])
    
    # Matplotlib code begins here
    a = plt.subplot2grid((7, 4), (1, 0), rowspan = 6, colspan = 4)
    
    a.clear() 
    a.plot(sentiments)
    
    title = "Sentiment plot of the company "+str(company)
    a.set_title(title, fontsize = 10)        
    
    sentiments  = []
    tweets = []

'''
def get_time():

    time_frame = "33"
    e = ttk.Entry(app)
    e.insert(0, 14)
    e.pack()
    e.focus_set()

    def callback():
        global time_frame
        time_frame = e.get()
        print("OUR TIME FRAME SELECTED IS "+time_frame)
        e.destroy()
    
    
    b = ttk.Button(app, text="Submit", width=10, command=callback)
    b.pack()
 '''


def create_dataset(dataset, time_step):
	dataX, dataY = [], []
	for i in range(len(dataset)-time_step-1):
		a = dataset[i:(i+time_step), :]   ###i=0, 0,1,2,3-----99   100 
		dataX.append(a)
		dataY.append(dataset[i + time_step, 5])
	return numpy.array(dataX), numpy.array(dataY)


def get_prediction(company_name, time_frame):

    
    if time_frame =="None":
        popupmsg("Please select time frame from the Time Frame menu")
        
    elif company_choice_for_prediction == "None":
        popupmsg("Please select company name from the Company Prediction menu")
        
    else:
        #popupmsg("Final choices for prediction are "+company_name+ " "+str(time_frame))
        time_frame = int(time_frame)
        today = datetime.today()
        yesterday = today - timedelta(days=time_frame)
        print(today)
        print()
        print(yesterday)

        df = web.DataReader(company_name, 'yahoo', yesterday, today)
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)
        
        print(df.head())
        df.to_csv("5_years_microsoft_data.csv")
        #print(df.describe())

        ##############################################################
        
        # STANDARDIZING THE DATA
        
        scaler = preprocessing.StandardScaler()
        df = scaler.fit_transform(np.array(df))
        
        
        scaling_dict = scaler.__dict__
        
        mean_closing_price = scaling_dict["mean_"][5]
        std_dev_closing_price = scaling_dict["scale_"][5]
        
        
        ##splitting dataset into train and test split
        training_size=int(len(df)*0.80)
        #test_size=len(df)-training_size
        train_data,test_data=df[0:training_size,:],df[training_size:len(df),:]
        
        # convert an array of values into a dataset matrix

        
        scaler.__dict__
        
        if time_frame <= 33:
            time_step = 1
            batch_size = 2
            
        elif time_frame <= 185:
            time_step = 10
            batch_size = 4
        
          
        elif time_frame <= 285:
            time_step = 15
            batch_size = 8
        
        
        elif time_frame <= 365:
            time_step = 30
            batch_size = 16
          
        elif time_frame <= 1828:
            time_step = 50
            batch_size = 32
            
        elif time_frame <= 3667:
            time_step = 100
            batch_size = 64
        
        else:
            time_step = 1
            batch_size = 2
            
        
        X_train, y_train = create_dataset(train_data, time_step)
        X_test, ytest = create_dataset(test_data, time_step)
          
        
        print(X_train.shape)
        print(y_train.shape)
        print(X_test.shape)
        print(ytest.shape)
        
        # reshape input to be [samples, time steps, features] which is required for LSTM
        X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 6)
        X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 6)
        
        #########################################################################
        
        # CREATING THE MODEL
        
        ### Create the Stacked LSTM model
        
        model=Sequential()
        model.add(LSTM(50,return_sequences=True,input_shape=(time_step,6)))
        model.add(LSTM(50,return_sequences=True))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error',optimizer='adam')
        
        model.summary()
        
        
        # Fitting the model.
        model.fit(X_train,y_train,validation_data=(X_test,ytest),batch_size=batch_size,epochs=100,verbose=1)
        
        
        train_predict=model.predict(X_train)
        test_predict=model.predict(X_test)
                
        ### Calculate RMSE performance metrics
        
        # Training data error
        from sklearn.metrics import mean_squared_error
        math.sqrt(mean_squared_error(y_train,train_predict))
        
        # Testing data error
        math.sqrt(mean_squared_error(ytest,test_predict))
        
        # getting the next day's i.e tomorrow's prediction
         
        X_tommo = pd.DataFrame(data=df)
        X_tommo = X_tommo.tail(time_step)
        
        X_tommo = X_tommo.values
        
        X_tommo_reshape = X_tommo.reshape(-1, time_step, 6)
        
        price_predict = model.predict(X_tommo_reshape)
        
        popupmsg("Final price after inversing the transform would be "+str((price_predict*std_dev_closing_price)+mean_closing_price))
    
 
def tutorial():
    popupmsg("Not yet supported!")

def loadChart(run):
    
    global chartLoad
    
    if run == 'start':
        chartLoad = True
        
    elif run == 'stop':
        chartLoad = False


def addTopIndicator(what):
    
    global topIndicator
    
    if what == "none":
        topIndicator = "none"
        print('Top indicator value is ', topIndicator)
        '''
        Code to destroy the graph of a particular indicator
        '''

    elif what == "rsi":
        topIndicator = "rsi"
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ, text = "Choose how many periods you want each RSI calculation to consider.")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0,14)
        e.pack()
        e.focus_set()

        def callback():
            global topIndicator
            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)

            topIndicator = group
            print("Set top indicator to",group)
            rsiQ.destroy()

        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()
        print('Top indicator value is ', topIndicator)


    elif what == "macd":
        topIndicator = "macd"
        print('Top indicator value is ', topIndicator)
        
        
def addBottomIndicator(what):

    global bottomIndicator
    
    if what == "none":
        bottomIndicator = "none"
        print('Bottom indicator value is ', bottomIndicator)
        '''
        Code to destroy the graph of a particular indicator
        '''

    elif what == "rsi":
        bottomIndicator = "rsi"
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ, text = "Choose how many periods you want each RSI calculation to consider.")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0,14)
        e.pack()
        e.focus_set()

        def callback():
            
            global bottomIndicator
            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)

            bottomIndicator = group
            print("Set bottom indicator to",group)
            rsiQ.destroy()

        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()
        print('Bottom indicator value is ', bottomIndicator)


    elif what == "macd":
        bottomIndicator = "macd"
        print('Bottom indicator value is ', bottomIndicator)

    
    #print('Resuming the updation of chart with bottom indicator!')
    #popupmsg('The bottom indicator choosen by the user is now : '+param)
    
    # link = 'https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=60min&time_period=15&series_type=open&apikey=TPVVLSFMNUVDDO82'
    '''
    print(bottomIndicator)
    print(type(bottomIndicator))
    
    
    if type(bottomIndicator) != str():
        print('RSI indicator selected')
        rsi_periods = param[1]
        print('\n'+str(rsi_periods)+'\n')
        
        #link = 
        
        
        
    elif bottomIndicator == 'macd':
        print('MACD indicator selected')
        
    else:
        print('\nNo bottom indicator selected\n')
    '''
    


def addMiddleIndicator(what):
    
    global middleIndicator
    
    if what == "none":
        middleIndicator = "none"
        print('Middle indicator value is ', middleIndicator)
        '''
        Code to destroy the graph of a particular indicator
        '''
    
    elif what == "sma":
        middleIndicator = "sma"
        print('Middle indicator value is ', middleIndicator)
        smaQ = tk.Tk()
        smaQ.wm_title("Periods?")
        label = ttk.Label(smaQ, text = "Choose how many periods you want for calculating SMA.")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(smaQ)
        e.insert(0,14)
        e.pack()
        e.focus_set()

        def callback():
            global middleIndicator
            periods = (e.get())
            group = []
            group.append("sma")
            group.append(periods)

            middleIndicator = group
            print("Set middle indicator to",group)
            smaQ.destroy()

        b = ttk.Button(smaQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()
        print('Middle indicator value is ', middleIndicator)


    elif what == "ema":
        middleIndicator = 'ema'
        print('Middle indicator value is ', middleIndicator)
        emaQ = tk.Tk()
        emaQ.wm_title("Periods?")
        label = ttk.Label(emaQ, text = "Choose how many periods you want for calculating EMA.")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(emaQ)
        e.insert(0,14)
        e.pack()
        e.focus_set()

        def callback():
            global middleIndicator
            periods = (e.get())
            group = []
            group.append("ema")
            group.append(periods)

            middleIndicator = group
            print("Set middle indicator to",group)
            emaQ.destroy()

        b = ttk.Button(emaQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()
        print('Middle indicator value is ', middleIndicator)


   
def company_sel(name_of_company):
    
    global company_choice_for_prediction
    company_choice_for_prediction = name_of_company
    popupmsg('You have selected '+ company_choice_for_prediction)

def time_frame_selection(time_frame_sel):
    
    global time_frame
    time_frame = time_frame_sel
    popupmsg('You have selected '+ str(time_frame))
    
    
        
def on_closing():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        app.destroy()
    
def quit_fun():
    if messagebox.askyesno("Warning", "Do you really disagree with our policy ?") == True:
        app.destroy()
    else:
        pass



def confirmation_choices_of_user(*args):
    if 'none' in args:
        popupmsg('Your choices are invalid!')
    else:      
        if messagebox.askyesno("Confirmation!", "Do you want to proceed with these choices?\n" +company_choice_for_prediction+ ',' + time_span_choice + ', '+ algorithm_choice) == True:
            popupmsg('Your choices are recorded!')
        
        else:
            popupmsg('Click Reset button! or Select other choices')

def get_link(*args):
    
    global link
    global company_name
    global symbol

    if len(args) != 0:
        symbol = args[0]
        
        if symbol == 'TSLA':
            company_name = 'Tesla'
        elif symbol == 'SPCE':
            company_name = 'Virgin Group'
        elif symbol == 'SPY':
            company_name = 'S&P 500'
        elif symbol == 'MSFT':
            company_name = 'Microsoft corporation'
        else:
            print('Not valid!!')
            
        link = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+str(symbol)+"&apikey=TPVVLSFMNUVDDO82"
     

def get_candle_stick_graph(*args):

    global link
    global company_name
    global data_time_span
    global candleWidth
    global candel_stick_graph
    global symbol
    global api_time_span
    
    candel_stick_graph = True
    
    try:
        api_time_span = args[1]
        data_time_span = args[2]
        candleWidth = args[3]
        print('API TIME SPAN IS : ', api_time_span)
        print('DATA TIME SPAN IS : ', data_time_span)
        
    except:
        pass

    print('Resuming the candle stick graph!')

    print(args)
    link = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+str(symbol)+"&interval="+str(api_time_span)+"min&outputsize=full&apikey=TPVVLSFMNUVDDO82"
    
    data = urllib.request.urlopen(link)
    data = data.read().decode('utf-8')
    data = json.loads(data)
    
    closedPriceList = []
    dateList = []
    volumeList = []
    openList = []
    highList = []
    lowList = []
    
    a = plt.subplot2grid((7, 4), (1, 0), rowspan = 6, colspan = 4)
    a.clear()
    
    for key in data['Time Series (' + str(api_time_span)+'min)']:
        open_price = float(data['Time Series (' + str(api_time_span)+'min)'][key]['1. open'])
        high_price = float(data['Time Series (' + str(api_time_span)+'min)'][key]['2. high'])
        low_price = float(data['Time Series (' + str(api_time_span)+'min)'][key]['3. low'])
        closed_price = float(data['Time Series (' + str(api_time_span)+'min)'][key]['4. close'])
        volume = int(float(data['Time Series (' + str(api_time_span)+'min)'][key]['5. volume']))
        
        date = key 
        date = pd.to_datetime(date)
        dateList.append(date)
        openList.append(open_price)
        highList.append(high_price)
        lowList.append(low_price)
        closedPriceList.append(closed_price)
        volumeList.append(volume)
        
    dateList = dateList[:data_time_span]
    openList = openList[:data_time_span]
    highList = highList[:data_time_span]
    lowList = lowList[:data_time_span]
    closedPriceList = closedPriceList[:data_time_span]
    volumeList = volumeList[:data_time_span]
    
    dateList_ = [datetime.timestamp(i) for i in dateList]   

    quotes1 = np.array([i for i in zip(dateList_, openList, highList, lowList, closedPriceList)], 
                        dtype=[('time', '<i4'), ('open', '<f4'), ('high', '<f4'), ('low', '<f4'), ('close', '<f4')])
    
    candlestick2_ohlc(a,quotes1['open'],quotes1['high'],quotes1['low'],quotes1['close'],width=candleWidth)
    
    xdate = [datetime.fromtimestamp(i) for i in quotes1['time']]
    
    a.xaxis.set_major_locator(ticker.MaxNLocator(10))
    
    def mydate(x,pos):
        try:
            return xdate[int(x)]
        except IndexError:
            return ''
    
    a.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
    
    f.autofmt_xdate()
    f.tight_layout()
            
    a.legend(bbox_to_anchor = (0, 1.02, 1, 0.102), loc = 3, ncol = 2, borderaxespad = 0)
    title = "Stock price of "+str(company_name)+"\n" + "Latest Price : " + str(closedPriceList[0])
    a.set_title(title, fontsize = 10)  
    
    print(data)
    print("LENGTH OF DATA POINTS ",len(dateList))
    print(link)

    '''   

    link = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+str(symbol)+"&interval="+str(api_time_span)+"min&apikey=TPVVLSFMNUVDDO82"
    popupmsg(link)

    for key in data['Time Series (Daily)']:
        open_price = float(data['Time Series (Daily)'][key]['1. open'])
        high_price = float(data['Time Series (Daily)'][key]['2. high'])
        low_price = float(data['Time Series (Daily)'][key]['3. low'])
        closed_price = float(data['Time Series (Daily)'][key]['4. close'])
        volume = int(float(data['Time Series (Daily)'][key]['5. volume']))
        
        date = key 
        date = pd.to_datetime(date)
        dateList.append(date)
        openList.append(open_price)
        highList.append(high_price)
        lowList.append(low_price)
        closedPriceList.append(closed_price)
        volumeList.append(volume)
    
    dateList_ = [datetime.timestamp(i) for i in dateList]   

    
    '''

def get_simple_graph(*args):
    
    global symbol
    global link
    global candel_stick_graph
    global data_time_span
    global period_to_put_in_link
    global dateList
    global closedPriceList
    global volumeList
    
    candel_stick_graph = False
    
    dateList = []
    closedPriceList = []
    volumeList = []
    
    print('Resuming the updation of chart with no indicator!')
    print(period_to_put_in_link)
    
    if period_to_put_in_link != 0:
        try:
            period_to_put_in_link = args[1]
            data_time_span = args[2]
        except:
            period_to_put_in_link = period_to_put_in_link
            data_time_span = data_time_span
        print('Length of arguments are not 0')
        print('period_to_put_in_link : ',period_to_put_in_link)
        print('data_time_span : ',data_time_span)
        
        if period_to_put_in_link < 5:
            print('\n')
            print('\n')
            link = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+str(symbol)+"&apikey=TPVVLSFMNUVDDO82"

            print(link)
            print('INTERDAY SERIES')
            print('\n')
            print('\n')

            dataLink_daily_prices = link
            data = urllib.request.urlopen(dataLink_daily_prices)
            data = data.read().decode('utf-8')
            data = json.loads(data)
            print("Data time span is ",data_time_span)
            
            for key in data['Time Series (Daily)']:
                closed_price = float(data['Time Series (Daily)'][key]['4. close'])
                
                volume = int(float(data['Time Series (Daily)'][key]['5. volume']))
                
                date = key 
                date = pd.to_datetime(date)
                dateList.append(date)
                closedPriceList.append(closed_price)
                volumeList.append(volume)

        else:
            
            link = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+str(symbol)+"&interval="+str(period_to_put_in_link)+"min&outputsize=full&apikey=TPVVLSFMNUVDDO82"

            print('\n')
            print('\n')
            print(link)
            print('INTRADAY SERIES')
            print('\n')
            print('\n')

            closedPriceList = []
            dateList = []
            volumeList = []
            
            data = urllib.request.urlopen(link)
            data = data.read().decode('utf-8')
            data = json.loads(data)

            a = plt.subplot2grid((7, 4), (1, 0), rowspan = 6, colspan = 4)
            a.clear()
            
            for key in data['Time Series (' + str(period_to_put_in_link)+'min)']:
                closed_price = float(data['Time Series (' + str(period_to_put_in_link)+'min)'][key]['4. close'])
                volume = int(float(data['Time Series (' + str(period_to_put_in_link)+'min)'][key]['5. volume']))
                
                date = key 
                date = pd.to_datetime(date)
                dateList.append(date)
                closedPriceList.append(closed_price)
                volumeList.append(volume)
    
    

    print('DATELIST FROM THE SIMPLE GRAPH METHOD IS ', dateList)
    print('LENGTH OF DATELIST FROM THE SIMPLE GRAPH METHOD IS ', len(dateList))
    a = plt.subplot2grid((7, 4), (1, 0), rowspan = 6, colspan = 4)
    
    a.clear()
    
    dateList = dateList[:data_time_span]
    closedPriceList = closedPriceList[:data_time_span]
    volumeList = volumeList[:data_time_span]
    
    
    a.plot_date(dateList, closedPriceList, 'g', label = 'prices') 

    a.xaxis.set_major_locator(mticker.MaxNLocator(5))
    a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                    
    a.legend(bbox_to_anchor = (0, 1.02, 1, 0.102), loc = 3, ncol = 2, borderaxespad = 0)
    title = "Stock price of "+str(company_name)+"\n" + "Latest Price : " + str(closedPriceList[0])
    a.set_title(title, fontsize = 10)  
    print('\n')
    print("LENGTH OF DATELIST ", len(dateList))
    print("LENGTH OF CLOSEDPRICELIST ", len(closedPriceList))
    print("LENGTH OF VOLUMELIST ",len(volumeList))
    print('\n')


def get_bottomIndicator_graph(param):
    
    global data_time_span
    global period_to_put_in_link
    global rsi_or_macd
    global time_periods_to_calculate_rsi
    global symbol
    global rsi_values
    global dateList_of_rsi
    
    rsi_values = []
    dateList_of_rsi = []
    
    print("%%%%%"*20)
    
    print("FROM BOTTOM INDICATOR GRAPH THE PARAMETERS ARE ", param)
    print("LENGTH OF THE PARAMETER IS ",len(param))
    
    print("%%%%%"*20)
    
    if len(param) == 2:
        rsi_or_macd = 'rsi'
        time_periods_to_calculate_rsi = param[1]
        
    elif len(param) == 4: # here param is a string so it would consider the length as 4
        rsi_or_macd = 'macd'
    
    else:
        rsi_or_macd = rsi_or_macd
        time_periods_to_calculate_rsi = time_periods_to_calculate_rsi
    
    
    print('\n')
    print('\n')
    print('rsi_or_macd ', rsi_or_macd)
    print('Company selected is ', symbol)
    print('data time span is ', data_time_span)
    print('period to put in link is ', period_to_put_in_link)
    print('Length of volume price list is', len(volumeList))
    print('Length of closed price list is ', len(closedPriceList))
    print('Length of date price list is ', len(dateList))    
    print('\n')
    print('\n')
    

    if rsi_or_macd == 'rsi':
        
        if period_to_put_in_link >= 5:
            
            print('time_periods_to_calculate_rsi ',time_periods_to_calculate_rsi)
            link_of_rsi = 'https://www.alphavantage.co/query?function=RSI&symbol='+str(symbol)+'&interval='+str(period_to_put_in_link)+'min&time_period='+str(time_periods_to_calculate_rsi)+'&series_type=close&apikey=TPVVLSFMNUVDDO82'
            
            print("#"*20)
            print('LINK FOR THE RSI ', link_of_rsi)
            print("#"*20)
            
            dataLink_daily_prices = link_of_rsi
            data = urllib.request.urlopen(dataLink_daily_prices)
            data = data.read().decode('utf-8')
            data = json.loads(data)
            #print(data)
            #dateList_of_rsi = [] 
            rsi = []
            
            dict_1 = data['Technical Analysis: RSI']
            for k,v in dict_1.items():
                k = pd.to_datetime(k)
                dateList_of_rsi.append(k)
                rsi.append(v)
            
            #rsi_values = []
            
            for i in rsi:
                for k, v in i.items():
                    rsi_values.append(v)
            
            rsi_values = [float(i) for i in rsi_values]
            
            dateList_of_rsi = dateList_of_rsi[:data_time_span]
            rsi_values = rsi_values[:data_time_span]
            
            print(len(dateList))
            print(len(dateList_of_rsi))
                        
            print(rsi_values[:10])
            print(closedPriceList[:10])
            
            print(dateList == dateList_of_rsi)
                
            
        elif period_to_put_in_link < 5:
            
            link_of_rsi = 'https://www.alphavantage.co/query?function=RSI&symbol='+str(symbol)+'&interval=daily&time_period='+str(time_periods_to_calculate_rsi)+'&series_type=close&apikey=TPVVLSFMNUVDDO82'
            
            print("#"*20)
            print('LINK FOR THE RSI ', link_of_rsi)
            print("#"*20)
            
            dataLink_daily_prices = link_of_rsi
            data = urllib.request.urlopen(dataLink_daily_prices)
            data = data.read().decode('utf-8')
            data = json.loads(data)
            #print(data)
            dataLink_daily_prices = link_of_rsi
            data = urllib.request.urlopen(dataLink_daily_prices)
            data = data.read().decode('utf-8')
            data = json.loads(data)
            #print(data)
            #dateList_of_rsi = [] 
            rsi = []
            
            dict_1 = data['Technical Analysis: RSI']
            for k,v in dict_1.items():
                k = pd.to_datetime(k)
                dateList_of_rsi.append(k)
                rsi.append(v)
            
            #rsi_values = []
            
            for i in rsi:
                for k, v in i.items():
                    rsi_values.append(v)
            
            rsi_values = [float(i) for i in rsi_values]
            
            dateList_of_rsi = dateList_of_rsi[:data_time_span]
            rsi_values = rsi_values[:data_time_span]
            
            print(len(dateList))
            print(len(dateList_of_rsi))
                        
            print(rsi_values[:10])
            print(closedPriceList[:10])
            
            print(dateList == dateList_of_rsi)
            print(dateList)
            print(dateList_of_rsi)

        a = plt.subplot2grid((7, 4), (0, 0), rowspan = 4, colspan = 4)
        a2 = plt.subplot2grid((7, 4), (5, 0), rowspan = 2, colspan = 4, sharex = a)
        
        a.clear()
        a2.clear() 
        
        a.plot_date(dateList, closedPriceList, 'g', label = 'prices') 
        a2.fill_between(dateList_of_rsi, 0, rsi_values, facecolor = "#183A54") 
    
        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                        
        a.legend(bbox_to_anchor = (0, 1.02, 1, 0.102), loc = 3, ncol = 2, borderaxespad = 0)
        title = "Stock price of "+str(company_name)+"\n" + "Latest Price : " + str(closedPriceList[0])
        a.set_title(title, fontsize = 10)  
        plt.setp(a.get_xticklabels(), visible = False)
    
    elif rsi_or_macd == 'macd':
        
        popupmsg('Sorry but MACD not supported yet!')
        '''
        if period_to_put_in_link >= 5:
            
            link_of_rsi = 'https://www.alphavantage.co/query?function=MACD&symbol='+str(symbol)+'&interval='+str(period_to_put_in_link)+'min&series_type=close&apikey=TPVVLSFMNUVDDO82'

            print("#"*20)
            print('LINK FOR THE MACD ', link_of_rsi)
            print("#"*20)
        
        elif period_to_put_in_link < 5:
            
            link_of_rsi = 'https://www.alphavantage.co/query?function=MACD&symbol='+str(symbol)+'&interval=daily'+'&series_type=close&apikey=TPVVLSFMNUVDDO82'
            
            print("#"*20)
            print('LINK FOR THE MACD ', link_of_rsi)
            print("#"*20)
         '''
    
    else:
        popupmsg('Not live yet!')


def get_middleIndicator_graph(param):
        
    global data_time_span
    global period_to_put_in_link
    global ema_or_sma
    global time_periods_to_calculate_ema_or_sma
    global symbol
    global sma_values
    global dateList_of_sma
    
    sma_values = []
    dateList_of_sma = []
    
    if len(param) == 2:
        ema_or_sma = param[0]
        time_periods_to_calculate_ema_or_sma = param[1]
    
    else:
        ema_or_sma = ema_or_sma
        time_periods_to_calculate_ema_or_sma = time_periods_to_calculate_ema_or_sma
    
    #print('Resuming the updation of chart with middle indicator!')
    #print('The middle indicator choosen by the user is now : ',param)
    
    print('\n')
    print('\n')
    #print('Link from the get_middle_indicator ', link)
    print('ema_or_sma ', ema_or_sma)
    print('time_periods_to_calculate_ema_or_sma ',time_periods_to_calculate_ema_or_sma)
    print('Company selected is ', symbol)
    print('data time span is ', data_time_span)
    print('period to put in link is ', period_to_put_in_link)
    print('Length of volume price list is', len(volumeList))
    print('Length of closed price list is ', len(closedPriceList))
    print('Length of date price list is ', len(dateList))    
    print('\n')
    print('\n')
    
    '''
    Here according to the logic the dateList and dateList_of_sma would be same.
    As the period i.e 30min, daily etc are used in both links i.e link_of_sma and simple_graph_link and are same only,
    Check for those.
    
    Change the string values from sma_values to float by first converting into int (as . will give base literal error)
    
    Make the sma_values global like closedPriceList, dateList and volumeList since we will need them 
    in the combination of the bottom_indi and top_indi graph also and othrer such combinations.
    
    
    SAME STEPS ARE VALID FOR THE EMA LIST ALSO WHILE DEALING WITH THE EMA INDICATOR..
    
    '''
    
    if period_to_put_in_link >= 5:
        
        link_of_sma = 'https://www.alphavantage.co/query?function='+str(ema_or_sma)+'&symbol='+str(symbol)+'&interval='+str(period_to_put_in_link)+'min&time_period='+str(time_periods_to_calculate_ema_or_sma)+'&series_type=close&apikey=TPVVLSFMNUVDDO82'
        
        print("#"*20)
        print('LINK FOR THE SMA ', link_of_sma)
        print("#"*20)
        
        dataLink_daily_prices = link_of_sma
        data = urllib.request.urlopen(dataLink_daily_prices)
        data = data.read().decode('utf-8')
        data = json.loads(data)
        
        #dateList_of_sma = []
        sma = []
        
        
        dict_1 = data['Technical Analysis: {}'.format(str(ema_or_sma).upper())]
        for k,v in dict_1.items():
            k = pd.to_datetime(k)
            dateList_of_sma.append(k)
            sma.append(v)
        
        #sma_values = []
        
        for i in sma:
            for k, v in i.items():
                sma_values.append(v)
        
        sma_values = [float(i) for i in sma_values]
        
        dateList_of_sma = dateList_of_sma[:data_time_span]
        sma_values = sma_values[:data_time_span]
        
        print(len(dateList))
        print(len(dateList_of_sma))
        
        #print(dateList[:10])
        #print(dateList_of_sma[:10])
        
        print(sma_values[:10])
        print(closedPriceList[:10])
        
        print(dateList == dateList_of_sma)
        a = plt.subplot2grid((7, 4), (0, 0), rowspan = 7, colspan = 4)
        a.clear()
        
        a.plot(dateList, closedPriceList, 'g', label = 'prices') 
        a.plot(dateList_of_sma, sma_values, 'b', label = str(ema_or_sma)) 
    
        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                        
        a.legend(bbox_to_anchor = (0, 1.02, 1, 0.102), loc = 3, ncol = 2, borderaxespad = 0)
        title = "Stock price of "+str(company_name)+"\n" + "Latest Price : " + str(closedPriceList[0])
        a.set_title(title, fontsize = 10)  
        
    elif period_to_put_in_link < 5:
        
        link_of_sma = 'https://www.alphavantage.co/query?function='+str(ema_or_sma)+'&symbol='+str(symbol)+'&interval=daily&time_period='+str(time_periods_to_calculate_ema_or_sma)+'&series_type=close&apikey=TPVVLSFMNUVDDO82'
        
        print("#"*20)
        print('LINK FOR THE SMA ', link_of_sma)
        print("#"*20)
        
        dataLink_daily_prices = link_of_sma
        data = urllib.request.urlopen(dataLink_daily_prices)
        data = data.read().decode('utf-8')
        data = json.loads(data)
        
        dateList_of_sma = []
        sma = []
        
        
        dict_1 = data['Technical Analysis: {}'.format(str(ema_or_sma).upper())]
        for k,v in dict_1.items():
            k = pd.to_datetime(k)
            dateList_of_sma.append(k)
            sma.append(v)
        
        sma_values = []
        
        for i in sma:
            for k, v in i.items():
                sma_values.append(v)
        
        sma_values = [float(i) for i in sma_values]
        
        dateList_of_sma = dateList_of_sma[:data_time_span]
        sma_values = sma_values[:data_time_span]
        
        print(len(dateList))
        print(len(dateList_of_sma))
        
        #print(dateList[:10])
        #print(dateList_of_sma[:10])
        
        print(sma_values[:10])
        print(closedPriceList[:10])
        
        print(dateList == dateList_of_sma)
        a = plt.subplot2grid((7, 4), (0, 0), rowspan = 7, colspan = 4)
        a.clear()
        
        a.plot(dateList, closedPriceList, 'g', label = 'prices') 
        a.plot(dateList_of_sma, sma_values, 'b', label = str(ema_or_sma)) 
    
        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                        
        a.legend(bbox_to_anchor = (0, 1.02, 1, 0.102), loc = 3, ncol = 2, borderaxespad = 0)
        title = "Stock price of "+str(company_name)+"\n" + "Latest Price : " + str(closedPriceList[0])
        a.set_title(title, fontsize = 10)  
    
    
    
    else:
        popupmsg('Not live yet!')


def get_topIndicator_graph(param):
    
    global data_time_span
    global period_to_put_in_link
    global rsi_or_macd
    global time_periods_to_calculate_rsi
    global symbol
    global rsi_values
    global dateList_of_rsi
    
    rsi_values = []
    dateList_of_rsi = []
    
    print("%%%%%"*20)
    
    print("FROM TOP INDICATOR GRAPH THE PARAMETERS ARE ", param)
    print("LENGTH OF THE PARAMETER IS ",len(param))
    
    print("%%%%%"*20)
    
    if len(param) == 2:
        rsi_or_macd = 'rsi'
        time_periods_to_calculate_rsi = param[1]
        
    elif len(param) == 4: # here param is a string so it would consider the length as 4
        rsi_or_macd = 'macd'
    
    else:
        rsi_or_macd = rsi_or_macd
        time_periods_to_calculate_rsi = time_periods_to_calculate_rsi
    
    
    print('\n')
    print('\n')
    print('rsi_or_macd ', rsi_or_macd)
    print('Company selected is ', symbol)
    print('data time span is ', data_time_span)
    print('period to put in link is ', period_to_put_in_link)
    print('Length of volume price list is', len(volumeList))
    print('Length of closed price list is ', len(closedPriceList))
    print('Length of date price list is ', len(dateList))    
    print('\n')
    print('\n')
    

    if rsi_or_macd == 'rsi':
        
        if period_to_put_in_link >= 5:
            
            print('time_periods_to_calculate_rsi ',time_periods_to_calculate_rsi)
            link_of_rsi = 'https://www.alphavantage.co/query?function=RSI&symbol='+str(symbol)+'&interval='+str(period_to_put_in_link)+'min&time_period='+str(time_periods_to_calculate_rsi)+'&series_type=close&apikey=TPVVLSFMNUVDDO82'
            
            print("#"*20)
            print('LINK FOR THE RSI ', link_of_rsi)
            print("#"*20)
            
            dataLink_daily_prices = link_of_rsi
            data = urllib.request.urlopen(dataLink_daily_prices)
            data = data.read().decode('utf-8')
            data = json.loads(data)
            #print(data)
            #dateList_of_rsi = [] 
            rsi = []
            
            dict_1 = data['Technical Analysis: RSI']
            for k,v in dict_1.items():
                k = pd.to_datetime(k)
                dateList_of_rsi.append(k)
                rsi.append(v)
            
            #rsi_values = []
            
            for i in rsi:
                for k, v in i.items():
                    rsi_values.append(v)
            
            rsi_values = [float(i) for i in rsi_values]
            
            dateList_of_rsi = dateList_of_rsi[:data_time_span]
            rsi_values = rsi_values[:data_time_span]
            
            print(len(dateList))
            print(len(dateList_of_rsi))
                        
            print(rsi_values[:10])
            print(closedPriceList[:10])
            
            print(dateList == dateList_of_rsi)
                
            
        elif period_to_put_in_link < 5:
            
            link_of_rsi = 'https://www.alphavantage.co/query?function=RSI&symbol='+str(symbol)+'&interval=daily&time_period='+str(time_periods_to_calculate_rsi)+'&series_type=close&apikey=TPVVLSFMNUVDDO82'
            
            print("#"*20)
            print('LINK FOR THE RSI ', link_of_rsi)
            print("#"*20)
            
            dataLink_daily_prices = link_of_rsi
            data = urllib.request.urlopen(dataLink_daily_prices)
            data = data.read().decode('utf-8')
            data = json.loads(data)
            #print(data)
            dataLink_daily_prices = link_of_rsi
            data = urllib.request.urlopen(dataLink_daily_prices)
            data = data.read().decode('utf-8')
            data = json.loads(data)
            #print(data)
            #dateList_of_rsi = [] 
            rsi = []
            
            dict_1 = data['Technical Analysis: RSI']
            for k,v in dict_1.items():
                k = pd.to_datetime(k)
                dateList_of_rsi.append(k)
                rsi.append(v)
            
            #rsi_values = []
            
            for i in rsi:
                for k, v in i.items():
                    rsi_values.append(v)
            
            rsi_values = [float(i) for i in rsi_values]
            
            dateList_of_rsi = dateList_of_rsi[:data_time_span]
            rsi_values = rsi_values[:data_time_span]
            
            print(len(dateList))
            print(len(dateList_of_rsi))
                        
            print(rsi_values[:10])
            print(closedPriceList[:10])
            
            print(dateList == dateList_of_rsi)
            print(dateList)
            print(dateList_of_rsi)

        a = plt.subplot2grid((7, 4), (3, 0), rowspan = 4, colspan = 4)
        a2 = plt.subplot2grid((7, 4), (1, 0), rowspan = 2, colspan = 4, sharex = a)
        
        a.clear()
        a2.clear() 
        
        a.plot_date(dateList, closedPriceList, 'g', label = 'prices') 
        a2.fill_between(dateList_of_rsi, 0, rsi_values, facecolor = "#183A54") 
    
        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                        
        a.legend(bbox_to_anchor = (0, 1.02, 1, 0.102), loc = 3, ncol = 2, borderaxespad = 0)
        title = "Stock price of "+str(company_name)+"\n" + "Latest Price : " + str(closedPriceList[0])
        a2.set_title(title, fontsize = 10)  
        plt.setp(a2.get_xticklabels(), visible = False)
    
    elif rsi_or_macd == 'macd':
        
        popupmsg('Sorry but MACD not supported yet!')
        '''
        if period_to_put_in_link >= 5:
            
            link_of_rsi = 'https://www.alphavantage.co/query?function=MACD&symbol='+str(symbol)+'&interval='+str(period_to_put_in_link)+'min&series_type=close&apikey=TPVVLSFMNUVDDO82'

            print("#"*20)
            print('LINK FOR THE MACD ', link_of_rsi)
            print("#"*20)
        
        elif period_to_put_in_link < 5:
            
            link_of_rsi = 'https://www.alphavantage.co/query?function=MACD&symbol='+str(symbol)+'&interval=daily'+'&series_type=close&apikey=TPVVLSFMNUVDDO82'
            
            print("#"*20)
            print('LINK FOR THE MACD ', link_of_rsi)
            print("#"*20)
         '''
    
    else:
        popupmsg('Not live yet!')
        

    
def get_bottomIndicator_graph_and_middleIndicator_graph(btm_indi, mid_indi):

    if len(sma_values) == 0:
        get_middleIndicator_graph(middleIndicator)
    
    if len(rsi_values) == 0:
        get_bottomIndicator_graph(bottomIndicator)
    
    print('\n')
    print('\n')
    print('Call to get_bottomIndicator_graph_and_middleIndicator_graph successfully made!')
    print('Length of sma is ', len(sma_values))
    print('Length of rsi is ', len(rsi_values))

    print(sma_values[:10])
    print(rsi_values[:10])
    
    print('\n')
    print('\n')
    
    a = plt.subplot2grid((7, 4), (0, 0), rowspan = 5, colspan = 4)
    a2 = plt.subplot2grid((7, 4), (5, 0), rowspan = 2, colspan = 4, sharex = a)

    a.clear()
    a2.clear() 
    
    a.plot(dateList, closedPriceList, 'g', label = 'prices') 
    a.plot(dateList_of_sma, sma_values, 'b', label = str(ema_or_sma)) 
    a2.fill_between(dateList_of_rsi, 0, rsi_values, facecolor = "#183A54") 

    a.xaxis.set_major_locator(mticker.MaxNLocator(5))
    a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                    
    a.legend(bbox_to_anchor = (0, 1.02, 1, 0.102), loc = 3, ncol = 2, borderaxespad = 0)
    title = "Stock price of "+str(company_name)+"\n" + "Latest Price : " + str(closedPriceList[0])
    a.set_title(title, fontsize = 10)  
    plt.setp(a.get_xticklabels(), visible = False)    


def get_topIndicator_graph_and_middleIndicator_graph(topIndicator, middleIndicator):

    if len(rsi_values) == 0:
        get_topIndicator_graph(topIndicator)
    
    if len(sma_values) == 0:
        get_middleIndicator_graph(middleIndicator)
        
    a = plt.subplot2grid((7, 4), (2, 0), rowspan = 5, colspan = 4)
    a2 = plt.subplot2grid((7, 4), (0, 0), rowspan = 2, colspan = 4, sharex = a)

    a.clear()
    a2.clear() 
    
    a.plot(dateList, closedPriceList, 'g', label = 'prices') 
    a.plot(dateList_of_sma, sma_values, 'b', label = str(ema_or_sma)) 
    a2.fill_between(dateList_of_rsi, 0, rsi_values, facecolor = "#183A54") 

    a.xaxis.set_major_locator(mticker.MaxNLocator(5))
    a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                    
    a.legend(bbox_to_anchor = (0, 0), borderaxespad = 0)
    title = "Stock price of "+str(company_name)+"\n" + "Latest Price : " + str(closedPriceList[0])
    a2.set_title(title, fontsize = 10)  
    plt.setp(a2.get_xticklabels(), visible = False)    


def get_topIndicator_graph_and_bottomIndicator_graph(topIndicator, bottomIndicator):
    
    if len(rsi_values) == 0:
        get_bottomIndicator_graph(bottomIndicator)
        
    
    a = plt.subplot2grid((7, 4), (2, 0), rowspan = 3, colspan = 4)
    a2 = plt.subplot2grid((7, 4), (0, 0), rowspan = 2, colspan = 4, sharex = a)
    a3 = plt.subplot2grid((7, 4), (5, 0), rowspan = 2, colspan = 4, sharex = a)
    a.plot(dateList, closedPriceList, 'g', label = 'prices') 
    a2.fill_between(dateList_of_rsi, 0, rsi_values, facecolor = "#183A54") 
    a3.fill_between(dateList_of_rsi, 0, rsi_values, facecolor = "#183A54") 
                    
                    
    a.xaxis.set_major_locator(mticker.MaxNLocator(5))
    a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                    
    a.legend(bbox_to_anchor = (0, 1.02, 1, 0.102), loc = 3, ncol = 2, borderaxespad = 0)
    title = "Stock price of "+str(company_name)+"\n" + "Latest Price : " + str(closedPriceList[0])
    a2.set_title(title, fontsize = 10)  
             
    plt.setp(a.get_xticklabels(), visible = False)  
    plt.setp(a2.get_xticklabels(), visible = False)    


def get_topIndicator_graph_and_bottomIndicator_graph_and_middleIndicator_graph(topIndicator, bottomIndicator, middleIndicator):

    if len(rsi_values) == 0:
        get_bottomIndicator_graph(bottomIndicator)
        
    if len(sma_values) == 0:
        get_middleIndicator_graph(middleIndicator)
        
    a = plt.subplot2grid((7, 4), (2, 0), rowspan = 3, colspan = 4)
    a2 = plt.subplot2grid((7, 4), (0, 0), rowspan = 2, colspan = 4, sharex = a)
    a3 = plt.subplot2grid((7, 4), (5, 0), rowspan = 2, colspan = 4, sharex = a)
    
    a.plot(dateList, closedPriceList, 'g', label = 'prices') 
    a.plot(dateList_of_sma, sma_values, 'b', label = str(ema_or_sma))
    a2.fill_between(dateList_of_rsi, 0, rsi_values, facecolor = "#183A54") 
    a3.fill_between(dateList_of_rsi, 0, rsi_values, facecolor = "#183A54") 
                    
                    
    a.xaxis.set_major_locator(mticker.MaxNLocator(5))
    a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                    
    a.legend()
    title = "Stock price of "+str(company_name)+"\n" + "Latest Price : " + str(closedPriceList[0])
    a2.set_title(title, fontsize = 10)  
             
    plt.setp(a.get_xticklabels(), visible = False)  
    plt.setp(a2.get_xticklabels(), visible = False)    



def animate(i):

    '''
    args: 
        i - intervals for refreshing rate of this
            animate function.For now i have used
            refresh rate of 12 seconds for the smooth
            functioning of the matplotlib graph.
    '''

    global link
    global data_time_span
    global candleWidth
    global chartLoad
    global candel_stick_graph
    
    print("animate function executed")
    print('From animate function Currently Top indicator is ',topIndicator)
    print('From animate function Currently Bottom indicator is ',bottomIndicator)
    print('From animate function Currently Middle indicator is ',middleIndicator)
    
    if chartLoad and candel_stick_graph == False: 
        if topIndicator == 'none' and bottomIndicator == 'none' and middleIndicator == 'none':
            get_simple_graph()
            
        elif bottomIndicator != 'none' and topIndicator == 'none' and middleIndicator == 'none':
            '''
            we are passing param so that we can put those indicators
            in our graph accordingly.
            '''
            get_bottomIndicator_graph(bottomIndicator)
            
        elif bottomIndicator == 'none' and topIndicator == 'none' and middleIndicator != 'none':
            get_middleIndicator_graph(middleIndicator)
            
        elif bottomIndicator == 'none' and topIndicator != 'none' and middleIndicator == 'none':
            get_topIndicator_graph(topIndicator)
            
        elif bottomIndicator != 'none' and topIndicator == 'none' and middleIndicator != 'none':
            get_bottomIndicator_graph_and_middleIndicator_graph(bottomIndicator, middleIndicator)
            
        elif bottomIndicator == 'none' and topIndicator != 'none' and middleIndicator != 'none':
            get_topIndicator_graph_and_middleIndicator_graph(topIndicator, middleIndicator)
            
        elif bottomIndicator != 'none' and topIndicator != 'none' and middleIndicator == 'none':
            get_topIndicator_graph_and_bottomIndicator_graph(topIndicator, bottomIndicator)
            
        elif bottomIndicator != 'none' and topIndicator != 'none' and middleIndicator != 'none':
            get_topIndicator_graph_and_bottomIndicator_graph_and_middleIndicator_graph(topIndicator, bottomIndicator, middleIndicator)

        else:
            get_simple_graph()
            popupmsg('Wait! Not ready as of now for your current choices of {}, {} and {}'.format(topIndicator, bottomIndicator, middleIndicator))

    elif chartLoad and candel_stick_graph == True:
        get_candle_stick_graph()        
        
    else:
        print('Stopping the updation of graph')
    
class StockMarketapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "Stock Market App")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        '''
        Adding the Menu bar
        '''
        
        menubar = tk.Menu(container)
        homeMenu = tk.Menu(menubar, tearoff = 0)
        homeMenu.add_command(label = "Save settings", command = lambda : popupmsg("Not supported yet !"))
        homeMenu.add_separator()
        homeMenu.add_command(label = "Exit", command = on_closing)
        menubar.add_cascade(label = "Home", menu = homeMenu) # shoving the File option in thr menubar with options.
        
        stockCompanyOptionMenu = tk.Menu(menubar, tearoff=1)
        stockCompanyOptionMenu.add_command(label = "Tesla", command = lambda : get_link("TSLA"))
        stockCompanyOptionMenu.add_separator()
        stockCompanyOptionMenu.add_command(label = "S&P 500", command = lambda : get_link("SPY"))
        stockCompanyOptionMenu.add_separator()
        stockCompanyOptionMenu.add_command(label = "Virgin Group", command = lambda : get_link("SPCE"))
        stockCompanyOptionMenu.add_separator()
        stockCompanyOptionMenu.add_command(label = "Microsoft Corporation", command = lambda : get_link("MSFT"))
        
        menubar.add_cascade(label = "Stock Companies", menu = stockCompanyOptionMenu)
        
        sentimentanalysismenu = tk.Menu(menubar, tearoff=0)
        sentimentanalysismenu.add_command(label = 'Tesla', command = lambda : get_tweets("Tesla"))
        sentimentanalysismenu.add_separator()
        sentimentanalysismenu.add_command(label = 'Microsoft', command = lambda : get_tweets("Microsoft"))
        sentimentanalysismenu.add_separator()
        sentimentanalysismenu.add_command(label = 'Virgin Galactic', command = lambda : get_tweets("Virgin Galactic"))
        sentimentanalysismenu.add_separator()
        sentimentanalysismenu.add_command(label = 'S And P 500', command = lambda : get_tweets("S And P 500"))

        menubar.add_cascade(label = 'Sentiment analysis', menu = sentimentanalysismenu)
        
        timeframemenu = tk.Menu(menubar, tearoff=1)
        
        timeframemenu.add_command(label = '1 Day with 5 mins period', command = lambda : get_simple_graph("1 Day with 5 mins period", 5, 288)) # Intraday link
        timeframemenu.add_command(label = '1 Day with 15 mins period', command = lambda : get_simple_graph("1 Day with 15 mins period", 15, 96)) # Intraday link
        timeframemenu.add_command(label = '1 Day with 30 mins period', command = lambda : get_simple_graph("1 Day with 30 mins period", 30, 48)) # Intraday link
        timeframemenu.add_command(label = '1 Day with 60 mins period', command = lambda : get_simple_graph("1 Day with 60 mins period", 60, 24)) # Intraday link
        timeframemenu.add_command(label = '3 Days with 15 mins period', command = lambda : get_simple_graph("3 Days with 15 mins period", 15, 288)) # Intraday link
        timeframemenu.add_command(label = '3 Days with 30 mins period', command = lambda : get_simple_graph("3 Days with 30 mins period", 30, 144)) # Intraday link
        timeframemenu.add_command(label = '3 Days with 60 mins period', command = lambda : get_simple_graph("3 Days with 60 mins period", 60, 72)) # Intraday link
        timeframemenu.add_command(label = '1 Week with 30 mins period', command = lambda : get_simple_graph("1 Week with 30 mins period", 30, 336)) # Intraday link
        timeframemenu.add_command(label = '1 Week with 60 mins period', command = lambda : get_simple_graph("1 Week with 60 mins period", 60, 168)) # Intraday link
        timeframemenu.add_command(label = '1 Week with 1 day period', command = lambda : get_simple_graph("1 Week with 1 day period", 1, 7)) # Daily link
        timeframemenu.add_command(label = '3 Weeks with 60 mins period', command = lambda : get_simple_graph("3 Weeks with 60 mins period", 60, 504)) # Intraday link
        timeframemenu.add_command(label = '3 Weeks with 1 day period', command = lambda : get_simple_graph("3 Weeks with 1 day period", 1, 21)) # Daily link
        timeframemenu.add_command(label = '1 Month with 1 day period', command = lambda : get_simple_graph("1 Month with 1 day period", 1, 30)) # Daily link
        timeframemenu.add_command(label = '3 Months with 1 day period', command = lambda : get_simple_graph("3 Months with 1 day period", 3, 90)) # Daily link
        
        
        menubar.add_cascade(label = 'Simple Graph Analysis', menu = timeframemenu)
        
        ohlcintervalmenu = tk.Menu(menubar, tearoff=1)
        
        '''
        use intraday link to achieve below
        API limit : 576
        '''
        ohlcintervalmenu.add_command(label = '5 mins bars And 1 Day', command = lambda : get_candle_stick_graph('5 mins bars And 1 Day', 5, 288, 0.5)) # 288 data points
        ohlcintervalmenu.add_command(label = '15 mins bars And 1 Day', command = lambda : get_candle_stick_graph('15 mins bars And 1 Day',15, 96, 0.5)) # 96 data points
        ohlcintervalmenu.add_command(label = '30 mins bars And 1 Day', command = lambda : get_candle_stick_graph('30 mins bars And 1 Day', 30, 48, 0.5)) # 48 data points
        ohlcintervalmenu.add_command(label = '60 min bars And 1 Day', command = lambda : get_candle_stick_graph('60 mins bars And 1 Day', 60, 24, 0.5)) # 24 data points
        ohlcintervalmenu.add_command(label = '15 mins bars And 3 Days', command = lambda : get_candle_stick_graph('15 mins bars And 3 Days', 15, 288, 0.5)) # 288 data points
        ohlcintervalmenu.add_command(label = '30 mins bars And 3 Days', command = lambda : get_candle_stick_graph('30 mins bars And 3 Days', 30, 144, 0.5)) # 144 data points
        ohlcintervalmenu.add_command(label = '60 mins bars And 3 Days', command = lambda : get_candle_stick_graph('60 mins bars And 3 Days', 60, 72, 0.5)) # 72 data points
        ohlcintervalmenu.add_command(label = '30 mins bars And 1 Week', command = lambda : get_candle_stick_graph('30 mins bars And 1 Week', 30, 336, 0.5)) # 336 data points
        ohlcintervalmenu.add_command(label = '60 mins bars And 1 Week', command = lambda : get_candle_stick_graph('60 mins bars And 1 Week', 60, 168, 0.5)) # 168 data points
        ohlcintervalmenu.add_command(label = '60 mins bars And 3 Weeks', command = lambda : get_candle_stick_graph('60 mins bars And 3 Weeks', 60, 504, 0.5)) # 504 data points

        menubar.add_cascade(label = 'OHLC Analysis', menu = ohlcintervalmenu)
       
        
       
        companypredmenu = tk.Menu(menubar, tearoff = 0)
    
        companypredmenu.add_command(label = 'Tesla', command = lambda : company_sel("TSLA"))
        companypredmenu.add_separator()
        
        companypredmenu.add_command(label = 'Microsoft', command = lambda : company_sel("MSFT"))
        companypredmenu.add_separator()
        
        companypredmenu.add_command(label = 'S And P 500', command = lambda : company_sel("^GSPC"))
        companypredmenu.add_separator()
        
        companypredmenu.add_command(label = 'Virgin Galactic', command = lambda : company_sel("SPCE"))
        companypredmenu.add_separator()

        menubar.add_cascade(label = 'Company Prediction', menu = companypredmenu)



        timeframemenu = tk.Menu(menubar, tearoff = 0)
        
        timeframemenu.add_command(label = '10 Years Data', command = lambda : time_frame_selection(3650)) # 10 yeras contains approaximately 3650 days.We are passing number of days as a argument
        timeframemenu.add_separator()
        timeframemenu.add_command(label = '5 Years Data', command = lambda : time_frame_selection(1825))
        timeframemenu.add_separator()
        timeframemenu.add_command(label = '1 Year Data', command = lambda : time_frame_selection(365))
        timeframemenu.add_separator()
        timeframemenu.add_command(label = '9 Months Data', command = lambda : time_frame_selection(275))
        timeframemenu.add_separator()
        timeframemenu.add_command(label = '6 Months Data', command = lambda : time_frame_selection(183))
        timeframemenu.add_separator()
        timeframemenu.add_command(label = '1 Month Data', command = lambda : time_frame_selection(31))
       
        menubar.add_cascade(label = 'Time Frame', menu = timeframemenu)



        indicatormenu = tk.Menu(menubar, tearoff=1)
        
        topindicatorsmenu = tk.Menu(indicatormenu, tearoff = 0)
        topindicatorsmenu.add_command(label = 'RSI', command = lambda : addTopIndicator('rsi'))
        topindicatorsmenu.add_command(label = 'MACD', command = lambda : addTopIndicator('macd'))
        topindicatorsmenu.add_command(label = 'None', command = lambda : addTopIndicator('none'))
        indicatormenu.add_cascade(label = 'Top Indicators', menu=topindicatorsmenu)
        
        
        middleindicatorsmenu = tk.Menu(indicatormenu, tearoff = 0)
        middleindicatorsmenu.add_command(label = 'SMA', command = lambda : addMiddleIndicator('sma'))
        middleindicatorsmenu.add_command(label = 'EMA', command = lambda : addMiddleIndicator('ema'))
        middleindicatorsmenu.add_command(label = 'None', command = lambda : addMiddleIndicator('none'))
        indicatormenu.add_cascade(label = 'Middle Indicators', menu = middleindicatorsmenu)
        
        bottomindicatorsmenu = tk.Menu(indicatormenu, tearoff = 0)
        bottomindicatorsmenu.add_command(label = 'RSI', command = lambda : addBottomIndicator('rsi')) 
        bottomindicatorsmenu.add_command(label = 'MACD', command = lambda : addBottomIndicator('macd'))
        bottomindicatorsmenu.add_command(label = 'None', command = lambda : addBottomIndicator('none'))
        indicatormenu.add_cascade(label = 'Bottom Indicators', menu = bottomindicatorsmenu)
        
        menubar.add_cascade(label = 'Technical Indicators', menu = indicatormenu)
        
        
        tradeButton = tk.Menu(menubar, tearoff=1)
        tradeButton.add_command(label = "Manual Trading",
                                command=lambda: popupmsg("This is not live yet"))
        tradeButton.add_command(label = "Automated Trading",
                                command=lambda: popupmsg("This is not live yet"))

        tradeButton.add_separator()
        tradeButton.add_command(label = "Quick Buy",
                                command=lambda: popupmsg("This is not live yet"))
        tradeButton.add_command(label = "Quick Sell",
                                command=lambda: popupmsg("This is not live yet"))

        tradeButton.add_separator()
        tradeButton.add_command(label = "Set-up Quick Buy/Sell",
                                command=lambda: popupmsg("This is not live yet"))

        menubar.add_cascade(label="Trading", menu=tradeButton)

        startStop = tk.Menu(menubar, tearoff = 1)
        startStop.add_command( label="Resume",
                               command = lambda: loadChart('start'))
        startStop.add_command( label="Pause",
                               command = lambda: loadChart('stop'))
        menubar.add_cascade(label = "Resume/Pause client", menu = startStop)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Tutorial", command= lambda : tutorial())

        menubar.add_cascade(label="Help", menu=helpmenu)


        tk.Tk.config(self, menu = menubar)
        
        self.frames = {}

        for F in (StartPage, StockMarketLandingPage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        label = ttk.Label(self, text='''Stock Markets are subjected to risks. 
        Trade at your own risk!''', font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_frame(StockMarketLandingPage))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree",
                            command=quit_fun)
        button2.pack()


class StockMarketLandingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Home Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Terms and Conditions",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(side = tk.BOTTOM, pady=20)
        
        button2 = ttk.Button(self, text = "Get Prediction",
                            command = lambda: get_prediction(company_choice_for_prediction, time_frame))
        button2.pack(side = tk.BOTTOM, pady=5)

        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        
       
app = StockMarketapp()
app.geometry("1280x720")
app.protocol("WM_DELETE_WINDOW", on_closing)

ani = animation.FuncAnimation(f, animate, interval=20000)

app.mainloop()

'''
MISCELLANEOUS SECTION

1 . Alpha Vantage API Key : TPVVLSFMNUVDDO82

2 . How to add new page?

        Keeping it for reference.
        
        class PageOne(tk.Frame):
        
            def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = ttk.Label(self, text="Page One!!!", font=LARGE_FONT)
                label.pack(pady=10,padx=10)
        
                button1 = ttk.Button(self, text="Back to Home",
                                    command=lambda: controller.show_frame(StartPage))
                button1.pack()
        
                button2 = ttk.Button(self, text="Page Two",
                                    command=lambda: controller.show_frame(PageTwo))
                button2.pack()
                
3 . Point to note:

    In case of intraday where we need to update 
    the graph at time interval specified we will
    define both the variables dateList and 
    closedPriceList outside this function
    
    Also for intraday_call we need to manipulate
    data in different form because of the different
    key used by both intra_day and daily_time_series.
    '''                

'''

REFERENCE SECTION :
    1 . Tkinter gui series of - sentdex.
    2 . python programming series for finance - Sentdex.
    3 . Siraj Raval Bicoin Trading bot - Siraj Raval
            link : https://www.youtube.com/watch?v=F2f98pNj99k

'''