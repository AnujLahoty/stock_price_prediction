import webbrowser
import requests
import bs4
import datetime
import time
import sys
import re
import pandas as pd
import numpy as np
import csv
import smtplib
import pyzmail
import subprocess
import pyperclip


# SCHEDULE THIS SCRIPT TO RUN AT 1:30 A.M WITH ONE DAY MORE.

dt = datetime.datetime.now()
print(dt)
unix_time = int(dt.timestamp())

# We are subtracting 34200 because of the difference of 11 hours and 30 minutes between the USA time and India time.

unix_time -= 34200
print(unix_time)
unix_time_str = str(unix_time)

# Creating the datetime object of 4:00 P.M for U.S Market
dt_us = datetime.datetime.fromtimestamp(unix_time)
print(dt_us)


# CREATING THE TIME TUPLE OF THE US DATETIME OBJECT TO CHECK THE CONDITION FOR WEEKEND. IF WEEKEND IS THERE IT WOULD SKIP THE PROCESSING AS ON WEEKEND THE MARKET WOULD BE CLOSE

time_tuple = datetime.datetime.timetuple(dt_us)

if time_tuple[6] == 5 or time_tuple[6] == 6:
	print("Market is closed today.So no operation required.")
	sys.exit(0)
else:
	print("Fetching value...")

#adj_close_value = "Default"
	
url = 'https://markets.businessinsider.com/index/s&p_500'
response_obj = requests.get(url)
soup_object = bs4.BeautifulSoup(response_obj.text, 'lxml')
adj_close_value = soup_object.find('span', attrs = {'class' : 'push-data'}).text
#adj_close_value = int(adj_close_value)
	
print(type(adj_close_value))

'''
# APPENDING OPERATION IN CSV FILE . REFORMATTING OUR DATETIME OBJECT TO APPEND IN THE CSV FILE
# STEP - 1 converting datetime object to the string.
string_dt_us = dt_us.strftime("%d-%m-%Y")
print(string_dt_us)
# STEP - 2 converting the string into datetome object.
dt_us_reformat = datetime.datetime.strptime(string_dt_us,"%d-%m-%Y").date()
print(dt_us_reformat)
print(type(dt_us_reformat))

output_file = open('^GSPC (2).csv', 'a', newline = '')
output_writer = csv.writer(output_file)
output_writer.writerow([dt_us_reformat, 0, 0, 0, 0, adj_close_value, 0])
output_file.close()
'''



'''
# Reading the data and storing it in the dataframe
df = pd.read_csv('^GSPC (2).csv')


#Info regarding null and not null object and the type of variable
df.info()

#setting index as date values
#df['Date'] = pd.to_datetime(df.Date,format='%Y-%m-%d')
df['day_of_week'] = 0
df['day_of_month'] = 0


for i in range(len(df['Date'])):  
	date_obj = datetime.datetime.strptime(df['Date'][i], "%Y-%m-%d")
	time_tup = datetime.datetime.timetuple(date_obj)
	time_sec = time.mktime(time_tup)
	df['Date'][i] = float(time_sec)
	day_of_week = time_tup[6] 
	if day_of_week == 4:
		df['day_of_week'][i] = 1
	
	day_of_month = time_tup[2]
	if day_of_month == 1:
		df['day_of_month'][i] = 1

modified_df = pd.DataFrame(columns=['Date', 'Adjusted_close', 'Friday', 'Month_begining_day'])
modified_df['Date'] = df['Date']
modified_df['Adjusted_close'] = df['Adj Close']
modified_df['Friday'] = df['day_of_week']
modified_df['Month_begining_day'] = df['day_of_month']

print(df.tail())
print(modified_df.head())
print(modified_df.tail())


####################################################################################################################################################################

X = modified_df.iloc[:, [0, 2, 3]].values
X = X.astype(float)

y = modified_df.iloc[:, 1].values



# TRAINING SET AND TEST SET
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)


# MACHINE LEARNING MODEL SECTION . 


# FITTING THE VALUES
# We are basicelly using the decision tree  algorithm to get our model learn and predict

# Bagging classifier

from sklearn.ensemble import BaggingRegressor
from sklearn.tree import DecisionTreeRegressor

bag_reg = BaggingRegressor(
                            DecisionTreeRegressor(), 
                            n_estimators = 100,
                            bootstrap = True,
                            n_jobs = -1,
                            )

bag_reg.fit(X_train, y_train)


# ASSESSING THE MODEL

# 1. Cross Validation score

# GOING FOR THE CROSS VALIDATION TEST ON THE TRAINING DATASET
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(bag_reg, X_train, y_train, cv=10)
mean = accuracies.mean()
print(mean)

# 2. Residual Squared Error
from sklearn.metrics import r2_score
r_2_score = r2_score(y_test, y_pred)
print('r_2 score is ', r_2_score)

'''

unix_time_future = unix_time + 86400
dt_us_future = datetime.datetime.fromtimestamp(unix_time_future)
print(dt_us_future)

# CHECKING FOR THE WEEKEND
time_tuple = datetime.datetime.timetuple(dt_us_future)

if time_tuple[6] == 5 or time_tuple[6] == 6:
	print("Market is closed today.So no operation required.")
	#sys.exit(0)
else:
	print("Predicting value...")

dt_us_future = dt_us_future.date()
print(dt_us_future)	

day_of_month_future_day = int(time_tuple[1])
day_of_week_future_day = int(time_tuple[6])
print(day_of_month_future_day)
print(day_of_week_future_day)
if day_of_week_future_day == 4:
	day_of_week_future_day = 1
else:
	day_of_week_future_day = 0

if day_of_month_future_day == 1:
	day_of_month_future_day = 1:
else:
	day_of_month_future_day = 0
	
future_pred = bag_reg.predict(np.array(unix_time_future,day_of_week_future_day, day_of_month_future_day).reshape(1, -1))
future_pred = str(future_pred)

####################################################################################################################################################################
# INTEGRATE THE EMAIL PART
# SMTP SCRIPT

# process to copy the password from another script pw.py
subprocess.Popen('python pw.py gmail')
password = pyperclip.paste()


#value_to_be_send_from_email = modified_df.iloc[1,:]
#value_to_be_send_from_email = str(value_to_be_send_from_email)
#print(value_to_be_send_from_email)

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
print(type(smtpObj))

print(smtpObj.ehlo())

print(smtpObj.starttls())

print(smtpObj.login('anujlahoty1997@gmail.com', password))

smtpObj.sendmail('anujlahoty1997@gmail.com', 'anujlahoty1997@gmail.com', 
					'Subject : TESTING\n I am sending this email for testing purpose.'+future_pred 
					)

print(smtpObj.quit())

####################################################################################################################################################################


