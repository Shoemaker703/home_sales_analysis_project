import numpy as np
import pandas as pd
import geopandas as gpd
from scipy.spatial import cKDTree
from shapely.geometry import Point

def ckdnearest(gdA, gdB, name):
    '''
    Takes in two GeoDataFrames with point geometries and finds, for every point
    in gdA, the nearest point in gdB. Code slightly modified from that found
    on the first response 'https://gis.stackexchange.com/questions/222315/geopandas-find-nearest-point-in-other-dataframe'
    
    Input:
        gdA - GeoDataFrame whose points you want to find the closest point in gdB
        gdB - GeoDataFrame with the points you want to align with gdA's
        name - name of column from gdB that you want included in output 
    
    Returns:
        updated version of gdA with the specified column from gdB as well as the distance 
        between that point and the row's point'''
    
    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    
    dist, idx = btree.query(nA, k=1)
    
    gdB_nearest = gdB.iloc[idx].drop(columns='geometry').reset_index(drop=True)
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest['NAME'],
            pd.Series(dist, name='dist')
        ],
        axis = 1)
    
    return gdf