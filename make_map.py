import folium
from folium.plugins import TimeSliderChoropleth
import numpy as np 
import pandas as pd
from datetime import datetime
import json
from shapely.geometry import shape, Point
import geopandas as gpd
from branca.colormap import linear

from Clean_Data import remove_outliers
from Clean_Data import remove_missing
from Load_Data import load_data


def map_data(df, geo_boundaries, lat = "lat", lon = "lon", measurement_type = "measurement_PM10", time_interval = "5Min"):
    '''
    Maps the PM10 and PM2.5 concentration 
    
    INPUTS:
    df:                  A pandas dataframe containing PM10 and Pm2.5 measurements, the location and time of the measurement
    geo_boundaries:      A geojson file containinig the geoboundaries on which to aggregate the data
    measurement_type:    String either measurement_PM10 or measurement_PM2.5
    lat:                 String with the column name of latitudes in df
    lon:                 String with the column name of longitude in df
    time_interval:       String specifying the time interval to which to aggregate the data (e.g. 30S, 10Min, 1H, 1D)
    
    
    
    OUTPUTS:
    index_measurement_type.html:               An HTML file with an interactive map
    m:                                         The map
    '''
    
    # first load the geo boundaries and create a geopandas dataframe out of df
    plz = gpd.read_file(geo_boundaries)
    geo_df = gpd.GeoDataFrame(df,geometry = gpd.points_from_xy(df["lon"], df["lat"]), crs = 4326)
    
    # combine the geoboundaries with the geo_df (allocate the points to the correct polygons)
    plz_pm = gpd.sjoin(plz,geo_df)
    plz_pm['polygon_id'] = plz_pm.index
    plz_pm = plz_pm.reset_index()
    plz_geom = plz_pm[['polygon_id','geometry']]
    
    plz_pm = plz_pm[['polygon_id',measurement_type,'time']]
    plz_pm['time'] = pd.to_datetime(plz_pm['time'])
    
    # aggreagte the data within each polygon by some prespecified time interval
    # this decides on how fine grained the slider is. 
    gr_plz_pm = plz_pm.groupby([pd.Grouper(key = "time",freq = time_interval), 'polygon_id']).mean()
    gr_plz_pm = gr_plz_pm.reset_index()
    gr_plz_pm['geometry'] = plz['geometry'][gr_plz_pm['polygon_id']].reset_index()['geometry']
    
    # define the style dictionary which is needed for the time slider (for each polygon and 
    # each time we assign a color based on the measured PM value)
    gr_plz_pm["dt_index"] = gr_plz_pm['time'].astype(int) // 10**9 # translate time to integer values
    cmap = linear.BuPu_09.scale(0, 50) # define the color scale
    cmap.caption = "PM10 concentration(μg/m³)" # define the label of the color scale (needed for plotting later)
    
    styledict = {}
    for poly in pd.unique(gr_plz_pm['polygon_id']):
    
        meas = gr_plz_pm.loc[gr_plz_pm['polygon_id'] == poly] # only retain measurements in that polygon
        poly = int(poly)
        styledict[poly] = {}
    
        for date_time in meas['dt_index']: # for each timestamp within that polygon assign a color
            value = float(meas[measurement_type][meas['dt_index'] == date_time]) #extract the measured value
            styledict[poly][date_time] = {'color': cmap(value),'opacity': 0.1}  # assign a color for the polygon - time - value combination
            # similar values will have similar colors because of the color scale cmap.
          
          
    # prepare data for plotting
    gr_plz_pm = gr_plz_pm.set_index(gr_plz_pm['polygon_id'])
    geo_gr_plz_pm = gpd.GeoDataFrame(gr_plz_pm)
    geo_gr_plz_pm = geo_gr_plz_pm.drop('time', axis = 1) # drop the time variable sicne else not convertibleto json file (needed for plotting)

    # extract the location of all sensors
    markers = df[df.duplicated('sensor_id') == False]
    markers = markers[['lat','lon','sensor_id']]
    markers = markers.reset_index()
    
    # Lastly define the map object
    center = [np.median(df[lat]), np.median(df[lon])] # define the center of the map

    m = folium.Map(location=center, zoom_start=12) # create the base map

    g = TimeSliderChoropleth(
        data = geo_gr_plz_pm.to_json(), # transform the geopandas dataframe to a json file
        styledict=styledict # use the styledictionary defined earlier
    ).add_to(m) 

    for jj in range(markers.shape[0]): # add circle markers for all sensors
        folium.CircleMarker(location = [markers['lat'][jj],markers['lon'][jj]],
                            color = "green",radius = 1,fill = True,
                            popup = str("sensor id:"+markers['sensor_id'][jj])).add_to(m)
    m.add_child(cmap) # finally add the legend
    
    m.save(str("index_"+measurement_type+".html"))
    
    return m