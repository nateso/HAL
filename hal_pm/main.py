from argparse import ArgumentParser, Namespace
import datetime
from package import *
import matplotlib.pyplot as plt
#from load_data import load_data
#from filter_data import remove_missing, remove_outliers
import pandas as pd
import os

def main(args):
    start_date = datetime.datetime.fromisoformat(args.start_date)
    
    #2. load data
    pmdata = Load_Data.load_data(args.lat_start, args.lat_end, args.long_start, args.long_end, start_date, args.delta_hours)
    
    #3. filter data
    print("\n")
    print("Results after filtering:")
    pmdata = Filter_Data.remove_missing(pmdata)
    pmdata = Filter_Data.remove_outliers(pmdata, method = args.filter) 
    

    #4. descriptive stats
    print("\n")
    print("The following are the maximum values for the two particle measurements:")
    pmmax, maxmap = Descriptive_Stats.get_max(pmdata, get_map = True)
    print(pmmax)

    fig, axes = plt.subplots(1, figsize=(20, 20))
    Plot_Mean.plot_mean_pm(pmdata, ax = axes)
    plt.savefig('plot_mean.png')


    #5 Time Plots
    fig, axes = plt.subplots(2, 2, figsize=(20, 20))
    Time_Plots.plot_average_pol(pmdata, ax = axes)
    plt.savefig('maxplots.png')


    #6 Correlation
    fig, axes = plt.subplots(1, figsize=(20, 20))
    corr = Corr_Fct.corr_matrix(pmdata, plot = True)
    print("\n")
    print("The correlation between the PM2.5 and the PM10 series is " + str(corr[0,1]))
    plt.savefig('corrmatrix.png')


    #7 Second dataframe
    if args.scd_start_date is not None:
        scd_start_date = datetime.datetime.fromisoformat(args.scd_start_date)
        pmdata2 = Load_Data.load_data(args.lat_start, args.lat_end, args.long_start, args.long_end, scd_start_date, args.delta_hours)
        fig, axes = plt.subplots(1, figsize=(20, 20))
        print("\n")
        print("Results for the second time interval")
        Plot_Mean.plot_mean_pm(pmdata, df2 = pmdata2, ax = axes)
        plt.savefig('plot_mean_2nddf')

    #8 Map
    PM25_map = Map.map_data(df, "package/mapping_data/plz_ger.geojson", measurement_type = "measurement_PM2.5")

if __name__ == "__main__":
    parser = ArgumentParser()
    
    parser.add_argument('lat_start', action="store", type=float)
    parser.add_argument('lat_end', action="store", type=float)
    parser.add_argument('long_start', action="store", type=float)
    parser.add_argument('long_end', action="store", type=float)
    parser.add_argument('start_date', action = "store", type=str)
    parser.add_argument('delta_hours', action="store", type=int)
    parser.add_argument('filter', action="store", type=str)
    parser.add_argument('scd_start_date', action="store", type=str)

    args = parser.parse_args()
    main(args)
