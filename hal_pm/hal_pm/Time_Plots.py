from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .hal_pm import *

def plot_average_pol(df, ax = None):
    '''Function to plot the time series of the polution of the sensors with the highest/lowest average polution over time'''
    
    '''INPUT:'''
    
    '''df:                         dataframe out of load_data function, where missing measurements are removed'''
    
    '''OUTPUT:'''
    
    '''time series of the polution of the sensors; one per measurement (PM10 and PM2.5)'''
    
    '''Defensive programming'''
    if df.isnull().values.any() == True:                                                                                     # Check whether data frame contains any NaN, if yes: remove
        df = Filter_Data.remove_missing(df)
    
    '''Find maximum and minimum avergae polututed sensor_id'''
    # For PM10:
    max_PM10 = max(df.groupby("sensor_id").mean()['measurement_PM10'])                                                       # group data by sensor_id, average the measurements, save maximum of measurement_PM10
    min_PM10 = min(df.groupby("sensor_id").mean()['measurement_PM10'])
    max_PM10_id = df.groupby("sensor_id").mean()[df.groupby("sensor_id").mean()['measurement_PM10'] == max_PM10].index[0]    # get sensor_id of maximum average measurement
    min_PM10_id = df.groupby("sensor_id").mean()[df.groupby("sensor_id").mean()['measurement_PM10'] == min_PM10].index[0]
    df_max_PM10 = df.loc[df['sensor_id'] == max_PM10_id]                                                                     # get data frame that contains only measurements of the sensor with maximum average observations
    df_min_PM10 = df.loc[df['sensor_id'] == min_PM10_id]
    
    # For PM2.5
    max_PM25 = max(df.groupby("sensor_id").mean()['measurement_PM2.5'])
    min_PM25 = min(df.groupby("sensor_id").mean()['measurement_PM2.5'])
    max_PM25_id = df.groupby("sensor_id").mean()[df.groupby("sensor_id").mean()['measurement_PM2.5'] == max_PM25].index[0]
    min_PM25_id = df.groupby("sensor_id").mean()[df.groupby("sensor_id").mean()['measurement_PM2.5'] == min_PM25].index[0]
    df_max_PM25 = df.loc[df['sensor_id'] == max_PM25_id]
    df_min_PM25 = df.loc[df['sensor_id'] == min_PM25_id]
    
    '''Plot maximum and minimum average polututed time series per measurement and maximum/minumum'''
    # Initialize two subplots for PM10 (min and max)
    _ax = 0
    if ax is None:
        fig, ax = plt.subplots(nrows = 2, ncols= 2, sharey = False, figsize = (10, 6))
        _ax = 1
    
    # define each subplot
    ax[0,0].plot(pd.to_datetime(df_max_PM10['time']).dt.strftime("%Y/%m/%d %H:%M"), df_max_PM10.measurement_PM10, label='average max.', c = 'red')        # get time on x-axis, the measurement on y-axis
        # moreover, the 'time' column is formatted to pd's datetime first and to a time string of "%Y/%m/%d %H:%M" format second to have better x-axis lables
    ax[0,0].set_xlabel('Time')                                                                                                # set labels and titles
    ax[0,0].set_ylabel('μg/m³')
    ax[0,0].set_title('Pollution requested time (threshold: PM10)')
    ax[0,0].grid(True)                                                                                                        # activate background grid
    ax[0,0].legend(loc='upper left')                                                                                          # add legend
    ax[0,0].xaxis.set_major_locator(plt.MaxNLocator(10))                                                                      # reducing maximum number of x-axis ticks to 10 for better readableness
    
    ax[0,1].plot(pd.to_datetime(df_min_PM10['time']).dt.strftime("%Y/%m/%d %H:%M"), df_min_PM10.measurement_PM10, label='average min.', c = 'darkblue')
    ax[0,1].set_xlabel('Time')
    ax[0,1].set_ylabel('μg/m³')
    ax[0,1].set_title('Pollution requested time (threshold: PM10)')
    ax[0,1].grid(True)
    ax[0,1].legend(loc='upper left')
    ax[0,1].xaxis.set_major_locator(plt.MaxNLocator(10))
    
    #fig1.autofmt_xdate(rotation = 45)
    
    # Initialize two subplots for PM2.5 (min and max)
    #fig1, ax1 = plt.subplots(1, 2, sharey = False, figsize = (10, 6))
    
    # define each subplot
    ax[1,0].plot(pd.to_datetime(df_max_PM25['time']).dt.strftime("%Y/%m/%d %H:%M"), df_max_PM25['measurement_PM2.5'], label='average max.', c = 'red')
    ax[1,0].set_xlabel('Time')
    ax[1,0].set_ylabel('μg/m³')
    ax[1,0].set_title('Pollution requested time (threshold: PM2.5)')
    ax[1,0].grid(True)
    ax[1,0].legend(loc='upper left')
    ax[1,0].xaxis.set_major_locator(plt.MaxNLocator(10))
    
    ax[1,1].plot(pd.to_datetime(df_min_PM25['time']).dt.strftime("%Y/%m/%d %H:%M"), df_min_PM25['measurement_PM2.5'], label='average min.', c = 'darkblue')
    ax[1,1].set_xlabel('Time')
    ax[1,1].set_ylabel('μg/m³')
    ax[1,1].set_title('Pollution requested time (threshold: PM2.5)')
    ax[1,1].grid(True)
    ax[1,1].legend(loc='upper left')
    ax[1,1].xaxis.set_major_locator(plt.MaxNLocator(10))
    
    if _ax == 1:
        fig.autofmt_xdate(rotation = 45)

    return ax.show()
