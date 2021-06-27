import numpy as np
import pandas as pd
import seaborn as sns

def corr_coeff(df):
    """Computes the correlation coefficient between the PM2.5 and PM10 measurements"""
    
    '''INPUT: '''
    
    '''df:              A pandas data frame containing PM2.5 and PM10 measurements for a sensor at a given time'''
    
    '''OUTPUT:'''
    
    '''A float value for the correlation coefficient'''
    
    pm25 = np.array(df['measurement_PM2.5'])
    pm10 = np.array(df['measurement_PM10'])
    
    n = len(pm25)
    
    meanpm25 = np.mean(pm25)
    meanpm10 = np.mean(pm10)
    
    stdpm25 = np.std(pm25)
    stdpm10 = np.std(pm10)
    
    num = (1/n) * np.sum((pm25 - meanpm25) * (pm10 - meanpm10))
    denom = stdpm25 * stdpm10
        
    return (num/denom)


def corr_matrix(df, plot = True):
    """Computes the correlation matrix between the PM2.5 and PM10 measurements"""
    
    '''INPUT: '''
    
    '''df:              A pandas data frame containing PM2.5 and PM10 measurements for a sensor at a given time'''
    
    '''OUTPUT:'''
    
    '''A numpy array for the correlation matrix. If plot = True, the correlation matrix plot using seaborn is shown'''
    
    ###remove missing check###
    
    pm25 = np.array(df['measurement_PM2.5'])
    pm10 = np.array(df['measurement_PM10'])
    
    n = len(pm25)
    
    meanpm25 = np.mean(pm25)
    meanpm10 = np.mean(pm10)
    
    stdpm25 = np.std(pm25)
    stdpm10 = np.std(pm10)
    
    num = (1/n) * np.sum((pm25 - meanpm25) * (pm10 - meanpm10))
    denom = stdpm25 * stdpm10
    
    res = np.ones((2,2))
    res[0,1], res[1,0] = (num/denom), (num/denom)
    
    if (plot == True):
        corrdf = pd.DataFrame(res)
        sns.heatmap(corrdf, annot = True)
    
    return res