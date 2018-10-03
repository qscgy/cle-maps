import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx
from shapely.geometry import Point


def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    # restore original x/y limits
    ax.axis((xmin, xmax, ymin, ymax))


def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    # restore original x/y limits
    ax.axis((xmin, xmax, ymin, ymax))


# converts tract number to 6-character FIPS string
def format_geoid(g):
    if len(g)==4:
        return '00'+g[:-2]
    elif len(g)==5:
        return '0'+g[:-1]
    else:
        return g


data_col = 'lead_pct'

race = pd.read_csv('white_pct.csv', skiprows=3)
race['pct_nonwhite'] = 100-race['pct_white']

lead_levels = pd.read_csv("lead_census_tracts_cuyahoga.csv", skiprows=3)    # lead level data
lead_levels[data_col] = lead_levels[data_col].map(lambda x: max(0, x))
lead_levels.merge(race, on='Census Tract')
print(lead_levels.head())

map_df = gpd.read_file("tl_2015_39_tract.shp")
# print(map_df.crs)
tract_ids = lead_levels.iloc[:,1]*100

geoids = []
for i in tract_ids:
    # print(format_geoid(str(int(i))))
    geoids.append('39035'+format_geoid(str(int(i))))    # 39035 is the FIPS ID for Cuyahoga County, OH

lead_levels['GEOID'] = geoids
# print(lead_levels)

map_df = map_df[map_df['GEOID'].isin(geoids)]   # select only the tracts that are in the lead level dataset
map_df = map_df.cx[-81.8:-81.5, 41.4:41.6]  # approximate Cleveland bounding box
map_df = map_df.merge(lead_levels, on='GEOID')
# map_df = map_df.to_crs(epsg=3857)
map_df.head()

plt.figure()
ax = map_df.plot(column=data_col, figsize=(20, 16), legend=True)
# add_basemap(ax, zoom=13)
cc = Point(-81.62, 41.5)
g = gpd.GeoSeries([cc])
g.crs = map_df.crs
g.plot(ax=ax, color='red')
# ax.plot(-81.62, 41.5, color='red', markersize=1000)
plt.title('Number of children under 6 with elevated blood lead levels')

plt.figure()
# print(list(map_df))
ax2 = map_df.plot(column='pct_nonwhite', figsize=(20, 16), legend=True)
plt.show()