import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import warnings

# check for missing values and potentially remove those. Also print how many observations have been removed
def remove_missing(df):
    """Detects and removes missing values, the function prints out how many values were deleted."""
    '''The function deletes the entire row if either the PM10 or PM2.5 value is missing.'''
    
    '''INPUT:'''
    
    '''df:              A pandas data frame containing PM2.5 and PM10 measurements for a sensor at a given time'''
    
    '''OUTPUT:'''
    
    '''A pandas data frame without missing values'''
    
    # Defensive programming
    if not (isinstance(df,pd.core.frame.DataFrame)):
        raise TypeError("df must be a pandas dataframe")
    if not 'measurement_PM10' in df.columns: 
        raise NameError("there is no variable called measurement_PM10")
    if not 'measurement_PM2.5' in df.columns: 
        raise NameError("there is no variable called measurement_PM2.5")
        
    # code 
    miss = np.any([pd.isna(df['measurement_PM10']),pd.isna(df['measurement_PM2.5'])],axis = 0) # check which rows contain missing values
    n_miss = miss.sum() # get number of missings 
    print(n_miss,"observations with missing values were removed from the data frame")
    df = df[miss == False] # only retain rows without missing values
    df = df.reset_index(drop = True) # reset the rownumbers
    return df  


# check for outliers and filter those using different methods
def remove_outliers(df,method = "Z-score", z_val = 2.58, crit_val = [0,100], quantile = [0,0.99]):
    '''function to remove outliers following a selected method'''
    '''deletes entire row in case either Pm10 or PM2.5 values is an outlier'''
    
    '''INPUTS:'''
    
    '''df:                         Pandas Data Frame'''
    '''method:                     A string indicating which method to use for filtering the data possible options: Z-score, critical_value, quantile'''
    '''z_val:                      Z-value, default is 2.58 (only standardised values between -1.96 and 1.96 are kept). type = byte.'''
    '''crit_val:                   List of lower and upper bound to filter values. Type: list, default: [0,100]'''
    '''quantile:                   List of lower and upper quantile to filter values. Type: list, default: [0,0.95]'''
    
    '''OUTPUTS:'''
    
    '''Pandas data frame without outliers. Prints out how many observations were removed'''
    
    # Defensive programming
    if not isinstance(method,str):
        raise TypeError("Method should be a string")
    if not method in ["Z-score","critical_value","quantile"]:
        raise NameError("invalid method was provided. possible options are: Z-score, critical_value or quantile")
    
    if method == "Z-score":
        if not isinstance(z_val,(float,int)):
            raise TypeError("z_val should be float or integer")
    
    if method == "critical_value":
        if not isinstance(crit_val,list):
            raise TypeError("crit_val should be a list with two elements")
        if len(crit_val) < 2:
            raise ValueError("need a lower and an upper bound (i.e. two elements)")
        if crit_val[0] > crit_val[1]:
            raise ValueError("the first element of crit_val should be smaller than the second")
        if len(crit_val) > 2:
            warnings.warn("Only first two elements of crit_val will be used!")
            
    
    if method == "quantile":
        if not isinstance(quantile,list):
            raise TypeError("quantile should be a list with two elements")
        if len(quantile) < 2:
            raise ValueError("need a lower and an upper bound (i.e. two elements)")
        if quantile[0] > quantile[1]:
            raise ValueError("the first element of quantile should be smaller than the second")
        if len(quantile) > 2:
            warnings.warn("Only first two elements of quantile will be used!")
        
    measurement = df[['measurement_PM10','measurement_PM2.5']] # extract PM10 and PM2.5 measurements from the df
    
    if method == "Z-score": 
        mean = measurement.mean()
        sd = measurement.std()
        z_score = (measurement - mean)/sd # calculate the z_score
        # exclude observations based their z-scores
        exclude_PM10 = np.any([z_score['measurement_PM10'] < -z_val, z_score['measurement_PM10'] > z_val],axis = 0)
        exclude_PM25 = np.any([z_score['measurement_PM2.5'] < -z_val, z_score['measurement_PM2.5'] > z_val],axis = 0)
    
    if method == "critical_value":
        exclude_PM10 = np.any([measurement['measurement_PM10'] < crit_val[0], measurement['measurement_PM10'] > crit_val[1]],axis = 0)
        exclude_PM25 = np.any([measurement['measurement_PM2.5'] < crit_val[0], measurement['measurement_PM2.5'] > crit_val[1]],axis = 0)
        
    if method == "quantile":
        upper = measurement.quantile(quantile[1])
        lower = measurement.quantile(quantile[0])
        exclude_PM10 = np.any([measurement['measurement_PM10'] < lower[0], measurement['measurement_PM10'] > upper[0]],axis = 0)
        exclude_PM25 = np.any([measurement['measurement_PM2.5'] < lower[1], measurement['measurement_PM2.5'] > upper[1]],axis = 0)
    
    exclude = np.any([exclude_PM10 == True, exclude_PM25 == True],axis = 0) # exclude observations as soon as at least one of the two measurements is an outlier
    n_excluded = exclude.sum()
    print(n_excluded,"outlier observations were deleted")
    df = df[exclude == False]
    df = df.reset_index(drop = True) # reset the rownumbers
    return df

