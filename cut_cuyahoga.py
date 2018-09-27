import pandas as pd
import geopandas as gpd
import numpy as np


# convert o 6-digit FIPS standard
def format_geoid(g):
    if len(g)==4:
        return '00'+g[:-2]
    elif len(g)==5:
        return '0'+g[:-1]
    else:
        return g

shapes = gpd.read_file("tl_2015_39_tract.shp")
lead = pd.read_csv("lead_census_tracts_cuyahoga.csv", skiprows=3)
tract_ids = lead.iloc[:,1]*100
geoids = []
for i in tract_ids:
    print(format_geoid(str(int(i))))
    geoids.append('39035'+format_geoid(str(int(i))))

# select only the rows whose tracts appear in the lead data`1       1`
shapes.GEOID = [str(g) for g in shapes.GEOID]
# print(geoids)
print(shapes.GEOID)
cuyahoga = shapes[shapes['GEOID'].isin(geoids)]
print(cuyahoga)

cuyahoga.to_csv("cuyahoga_shapefiles.shp")