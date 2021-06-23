import requests
import datetime
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt

from Load_Data import load_data
from Clean_Data import remove_outliers
from Clean_Data import remove_missing


def plot_average_pol(df):
    '''Function to plot the time series of the polution of the sensors with the highest/lowest average polution over time'''
    
    '''INPUT:'''
    
    '''df:                         dataframe out of load_data function, where missing measurements are removed'''
    
    '''OUTPUT:'''
    
    '''time series of the polution of the sensors; one per measurement (PM10 and PM2.5)'''
    
    '''Check whether data frame contains any NaN, if yes: remove'''
    if df.isnull().values.any() == True:
        df = remove_missing(df)
    
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
    fig1, ax1 = plt.subplots(1, 2, sharey = False, figsize = (10, 6))
    
    # define each subplot
    ax1[0].plot(df_max_PM10.time, df_max_PM10.measurement_PM10, label='average max.', c = 'red')                             # get time on x-axis, the measurement on y-axis
    ax1[0].set_xlabel('Time')                                                                                                # set labels and titles
    ax1[0].set_ylabel('μg/m³')
    ax1[0].set_title('Polution over requested time (threshold: PM10)')
    ax1[0].grid(True)                                                                                                        # activate background grid
    ax1[0].legend(loc='upper left')                                                                                          # add legend
    ax1[0].xaxis.set_major_locator(plt.MaxNLocator(10))                                                                      # reducing maximum number of x-axis ticks to 10 for better readableness
    
    ax1[1].plot(df_min_PM10.time, df_min_PM10.measurement_PM10, label='average min.', c = 'darkblue')
    ax1[1].set_xlabel('Time')
    ax1[1].set_ylabel('μg/m³')
    ax1[1].set_title('Polution over requested time (threshold: PM10)')
    ax1[1].grid(True)
    ax1[1].legend(loc='upper left')
    ax1[1].xaxis.set_major_locator(plt.MaxNLocator(10))
    
    fig1.autofmt_xdate(rotation = 45)
    
    # Initialize two subplots for PM2.5 (min and max)
    fig2, ax2 = plt.subplots(1, 2, sharey = False, figsize = (10, 6))
    
    # define each subplot
    ax2[0].plot(df_max_PM25.time, df_max_PM25['measurement_PM2.5'], label='average max.', c = 'red')
    ax2[0].set_xlabel('Time')
    ax2[0].set_ylabel('μg/m³')
    ax2[0].set_title('Polution over requested time (threshold: PM2.5)')
    ax2[0].grid(True)
    ax2[0].legend(loc='upper left')
    ax2[0].xaxis.set_major_locator(plt.MaxNLocator(10))
    
    ax2[1].plot(df_min_PM25.time, df_min_PM25['measurement_PM2.5'], label='average min.', c = 'darkblue')
    ax2[1].set_xlabel('Time')
    ax2[1].set_ylabel('μg/m³')
    ax2[1].set_title('Polution over requested time (threshold: PM2.5)')
    ax2[1].grid(True)
    ax2[1].legend(loc='upper left')
    ax2[1].xaxis.set_major_locator(plt.MaxNLocator(10))
    
    fig2.autofmt_xdate(rotation = 45)
