from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_mean_pm(df, df2 = None, time_interval = None):
    '''plots the mean PM10 and PM2.5 concentration over the given location against time'''
    
    '''INPUTS:'''
    
    '''df:             Pandas Data Frame with PM10 and PM2.5 measurements as column'''
    '''df2:            optional: second Pandas Data Frame with PM10 and PM2.5 measurements
                       as column. If provided, its series are plotted against the ones in df'''
    '''time_interval:  A String indicating over which time interval to average the data.
                       If none is provided, the function automatically calculates a value that leads
                       to 30 data points after averaging'''
    '''                Look at documentation of pandas.DataFrame.resample to get permissive values'''
    
    '''OUTPUTS:'''
    
    
    
    df['date_time'] = pd.to_datetime(df['time']) #convert time column to date_time
    df1 = df[['date_time','measurement_PM10','measurement_PM2.5']] #keep only the columns we need
    
    
    ######time_interval over which to average#####
    #if no time_interval is passed, calculate appropriate value here
    if time_interval is None:
        secinday = 60 * 60 * 24 #seconds in a day
        
        #get range of time over which we have data
        timediff = df['date_time'][len(df['date_time'])-1] - df['date_time'][0]
        
        #30 points make for a good default value for number of data points after averaging
        #get minute value (for smoothing) that leads to 30 points
        min_smoother = divmod(timediff.days * secinday + timediff.seconds, 60)[0] // 25
        
        time_interval = str(min_smoother) + "Min" #final value for time_interval
    
    
    
    #average over the given time_interval
    mean_data1 = df1.set_index('date_time').resample(time_interval, label='right').mean()
    mean_data1['date_time'] = mean_data1.index.strftime("%H:%M")
    
    #get date that data was collected on
    day1 = df1['date_time'][0].strftime("%y/%m/%d")

    
    #if a second dataframe is supplied, perform the same averaging operations
    if df2 is not None:
        #same exact as with df1
        df2['date_time'] = pd.to_datetime(df2['time'])
        df2 = df2[['date_time','measurement_PM10','measurement_PM2.5']]
        mean_data2 = df2.set_index('date_time').resample(time_interval, label='right').mean()
        mean_data2['date_time'] = mean_data2.index.strftime("%H:%M")
        
        #additionally (for the plot legend), rename columns to include the respecitive dates
        day2 = df2['date_time'][0].strftime("%y/%m/%d")

        mean_data1 = mean_data1.rename(columns = {'measurement_PM10': 'PM10: ' + day1, 
                                                  'measurement_PM2.5': 'PM2.5: ' + day1})
        mean_data2 = mean_data2.rename(columns = {'measurement_PM10': 'PM10: ' + day2, 
                                                  'measurement_PM2.5': 'PM2.5: ' + day2})

    
    
    ########Plotting###########
    plt.rc('font', size=20)          # controls default text sizes
    fig, ax = plt.subplots(figsize = (20,10))
    if df2 is None:
        mean_data1 = mean_data1.rename(columns = {'measurement_PM10': 'PM10', 
                                                  'measurement_PM2.5': 'PM2.5'})
        ax.plot('date_time', 'PM10', data = mean_data1, 
                color = "darkred",  linewidth = 3)
        ax.plot('date_time', 'PM2.5', data = mean_data1, 
                color = 'steelblue', linewidth = 3)
        ax.set_title("Average PM concentration for " + day1)

    
    if df2 is not None: 
        #first, print correlation between the two respective series
        corrpm10 = np.round(np.corrcoef(mean_data1['PM10: ' + day1], mean_data2['PM10: ' + day2])[0,1], 4)
        corrpm25 = np.round(np.corrcoef(mean_data1['PM2.5: ' + day1], mean_data2['PM2.5: ' + day2])[0,1], 4)
        print("The correlation between the two PM10 series is " + str(corrpm10) + " and \n" +
             "the correlation between the two PM2.5 series is " + str(corrpm25))
        
        #then, plotting
        ax.plot('date_time', 'PM2.5: ' + day1, data = mean_data1, 
                color = 'skyblue', linewidth = 3)
        ax.plot('date_time', 'PM10: ' + day1, data = mean_data1, 
                color = "steelblue", linewidth = 3)
        ax.plot('date_time', 'PM2.5: ' + day2, data = mean_data2, 
                color = 'darksalmon', linewidth = 3)
        ax.plot('date_time', 'PM10: ' + day2, data = mean_data2, 
                color = 'darkred', linewidth = 3)
        ax.set_title("Average PM concentration for " + day1 + " and " + day2)
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.grid(True)
    ax.legend(loc = "best")
    ax.set_xlabel("Date and Time")
    ax.set_ylabel("μg/m³")
    fig.autofmt_xdate(rotation = 45)
    
    
    