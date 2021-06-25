import requests
from datetime import datetime, timedelta
import pandas as pd

def load_data(lat_start, lat_end, long_start, long_end, start_datetime, delta_hours):
    '''Function for loading the data out of the REST-API'''
    
    '''INPUT:'''
    
    '''lat_start:                          latitude range starting point, type: byte'''
    '''lat_end:                            latitude range ending point, type: byte'''
    '''long_start:                         longitude range starting point, type: byte'''
    '''long_end:                           longitude range ending point, type: byte'''
    '''start_year, start_month, start_day: year / month / day of the measurement to start, type: byte'''
    '''delta_hours:                        time delta to calculate time space of measurement, type: byte'''
    
    '''OUPUT:'''
    
    '''Merged data frame on P1 and P2 is outputted'''
    
    '''Defensive programming'''
    if not (isinstance(lat_start, float) or isinstance(lat_start, int)):                    # checks type of lat_start parameter with isinstance (int or float)
        raise TypeError("Coordinate value only supports int and float")                     # raise TypeError is not numeric
    if not (isinstance(lat_end, float) or isinstance(lat_end, int)):
        raise TypeError("Coordinate value only supports int and float")
    if not (isinstance(long_start, float) or isinstance(long_start, int)):
        raise TypeError("Coordinate value only supports int and float")
    if not (isinstance(long_end, float) or isinstance(long_end, int)):
        raise TypeError("Coordinate value only supports int and float")
    if not (isinstance(delta_hours, float) or isinstance(delta_hours, int)):
        raise TypeError("Time delta value only supports int and float")
    if delta_hours <= 0:                                                                    # if delta_hours is smaller equal zero:
        raise ValueError("Time delta only defined for positive numbers")                    # raise value error
    if lat_end <= lat_start:
        raise ValueError("Latitude range ending starting point must be larger than starting point")
    if long_end <= long_start:
        raise ValueError("Longitude range ending starting point must be larger than starting point")
    
    '''Import Data from REST_API'''
    # Basic parameters
    base_url='http://sensordata.gwdg.de/api/' 
    endpoint_url_P1='measurements/P1'          # P1 endpoint
    endpoint_url_P2='measurements/P2'          # P2 endpoint

    # Select geo-coordinates
    latrange=[lat_start, lat_end]
    longrange=[long_start, long_end]

    # Select time range
    end_date = (start_datetime + timedelta(hours = delta_hours))

    # Build the query
    mydata = '{"timeStart": "'+start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")+'",' + \
             '"timeEnd": "'+end_date.strftime("%Y-%m-%dT%H:%M:%SZ")+'", "area":  \
             {"coordinates":['+str(latrange)+','+str(longrange)+']}}'

    # Run the query
    response_P1 = requests.post(base_url + endpoint_url_P1, data=mydata)
    response_P2 = requests.post(base_url + endpoint_url_P2, data=mydata)
    
    '''Initialize data frames'''
    j_P1 = response_P1.json()                                                                            # convert REST-API data to json at first
    del j_P1[1]                                                                                          # delete 'sensor' string, that causes errors
    df_P1 = pd.DataFrame(j_P1[1], columns =j_P1[0])                                                      # put all in pandas data frame
    df_P1 = df_P1.rename(columns={"P1": "measurement_PM10"})                                             # Change column name for better overview
    l_P1 = list(range(len(df_P1["sensor_id"])))
    for i in range(len(l_P1)):                                                                           # Adding unique measurement_id to merge P1 and P2
        l_P1[i] = str(df_P1["sensor_id"][i]) + "_" + str(df_P1["time"][i])
    df_P1["measurement_id"] = l_P1
    df_P1 = df_P1.reindex(columns = ["measurement_PM10", "time", "lat", "lon", "sensor_id", "measurement_id"])    # rearranging column names for better overview 

    
    j_P2 = response_P2.json()
    del j_P2[1]
    df_P2 = pd.DataFrame(j_P2[1], columns =j_P2[0])
    df_P2 = df_P2.rename(columns={"P2": "measurement_PM2.5"})
    l_P2 = list(range(len(df_P2["sensor_id"])))
    for j in range(len(l_P2)):                                                                           # Adding unique measurement_id to merge P1 and P2
        l_P2[j] = str(df_P2["sensor_id"][j]) + "_" + str(df_P2["time"][j])
    df_P2["measurement_id"] = l_P2
    df_P2 = df_P2.reindex(columns = ["measurement_PM2.5", "measurement_id"])
    
    '''Initialize output'''
    df_total = pd.merge(df_P1, df_P2, on = "measurement_id")                                         # merge data frame on unique measurement_id
    df_total = df_total.reindex(columns = ["measurement_PM10", "measurement_PM2.5", "time", "lat", "lon", "sensor_id", "measurement_id"])
    return df_total                                                                                  # return combined data frame
