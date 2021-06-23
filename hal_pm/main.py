from argparse import ArgumentParser, Namespace
import datetime
from package import *
import matplotlib.pyplot as plt
#from load_data import load_data
#from filter_data import remove_missing, remove_outliers
import pandas as pd

def main(args):
    start_date = datetime.datetime.fromisoformat(args.start_date)
    
    pmdata = Load_Data.load_data(args.lat_start, args.lat_end, args.long_start, args.long_end, start_date, args.delta_hours)
    
    pmdata = Filter_Data.remove_missing(pmdata)
    pmdata = Filter_Data.remove_outliers(pmdata, method = args.filter) 
    
    maxims, maxmap = Descriptive_Stats.get_max(pmdata)
    
    maxmap.show()
    #print(pmdata.head())

if __name__ == "__main__":
    parser = ArgumentParser()
    
    parser.add_argument('lat_start', action="store", type=float)
    parser.add_argument('lat_end', action="store", type=float)
    parser.add_argument('long_start', action="store", type=float)
    parser.add_argument('long_end', action="store", type=float)
    parser.add_argument('start_date', action = "store", type=str)
    parser.add_argument('delta_hours', action="store", type=int)
    parser.add_argument('filter', action="store", type=str)
    
    args = parser.parse_args()
    main(args)
