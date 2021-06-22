import requests
from datetime import datetime, timedelta
import pandas as pd
import warnings
import numpy as np


def remove_missing(df):
    miss = pd.isna(df["measurement_PM10"]) | pd.isna(df["measurement_PM2.5"])
    n_miss = miss.sum()
    print(n_miss,"observations were removed from the data frame")
    return df[~miss]  


def remove_outliers(df, method = "Z-score", z_val = 1.96, crit_val = [0,0], quantile = [0,0.95]):
    measurement = df["measurement_PM10"]
    
    if method == "Z-score":
        mean = measurement.mean()
        sd = measurement.std()
        z_score = (measurement.values - mean)/sd
        exclude = np.any([z_score < -z_val, z_score > z_val],axis = 0)
    
    if method == "critical_value":
        if len(crit_val) < 2:
            print("ERROR: please provide a lower and an upper bound")
            return
        if len(crit_val) > 2:
            warnings.warn("Only first two elements of crit_val will be used!")
        exclude = np.any([measurement < crit_val[0], measurement > crit_val[1]],axis = 0)
        

    if method == "quantile":
        if len(quantile) < 2:
            print("ERROR: please provide a lower and an upper quantile")
            return 
        if len(quantile) > 2:
            warnings.warn("Only first two elements of quantile will be used!")
        upper = measurement.quantile(quantile[1])
        lower = measurement.quantile(quantile[0])
        exclude = np.any([measurement  < lower, measurement > upper],axis = 0)
    
    n_excluded = exclude.sum()
    print(n_excluded,"observations were deleted")
    return df[exclude == False]