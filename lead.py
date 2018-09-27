import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd


# converts tract number to 6-character FIPS string
def format_geoid(g):
    if len(g)==4:
        return '00'+g[:-2]
    elif len(g)==5:
        return '0'+g[:-1]
    else:
        return g


lead_levels = pd.read_csv("lead_census_tracts_cuyahoga.csv", skiprows=3)    # lead level data
map_df = gpd.read_file("tl_2015_39_tract.shp")
tract_ids = lead_levels.iloc[:,1]*100
lead_levels['lead_pct'] = lead_levels['lead_pct'].map(lambda x: max(0, x))
geoids = []
for i in tract_ids:
    # print(format_geoid(str(int(i))))
    geoids.append('39035'+format_geoid(str(int(i))))    # 39035 is the FIPS ID for Cuyahoga County, OH

lead_levels['GEOID'] = geoids
# print(lead_levels)

map_df = map_df[map_df['GEOID'].isin(geoids)]   # select only the tracts that are in the lead level dataset
map_df = map_df.cx[-81.8:-81.5, 41.4:41.6]  # approximate Cleveland bounding box
map_df = map_df.merge(lead_levels, on='GEOID')
map_df.head()

plt.figure()
ax = map_df.plot(column='lead_pct', figsize=(20, 16), legend=True)
plt.title('Children under 6 with elevated blood lead levels')
plt.show()