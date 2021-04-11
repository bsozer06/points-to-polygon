# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

@author: Burhan Sözer
"""

import pandas as pd
import numpy as np
from osgeo import ogr
# from operator import itemgetter, attrgetter



""" for parameters to generate a polygon """
l_id =  502243                                          #47942                   
t_id =  14126205                                        #13818425        
alanAdi =  r"SIVI FERMANTE ÜRÜN DEPOLAMA ALANI"         #np.nan
alaniTuru =  r"CURUTUCU_VE_REAKTOR_ALANI"                #np.nan


path = r"D:\burhan\Data\CbsKoordinatBilgileriNoktaWgs_Yeni\CbsKoordinatBilgileriNoktaWgs_XY.csv"
df = pd.read_csv(path, sep=';')

df_group = df.groupby(["lisans_id", "tesis_id", "koordinatAlaniTuru", "bagimsizAlanAdi"], 
                      dropna=False).size().reset_index(name='Count') 

if ( df["bagimsizAlanAdi"].isna().any() | df_group["koordinatAlaniTuru"].isna().any() ):
    df[["koordinatAlaniTuru","bagimsizAlanAdi"]] = df[["koordinatAlaniTuru","bagimsizAlanAdi"]].fillna('null')
    df_group[["koordinatAlaniTuru","bagimsizAlanAdi"]] = df_group[["koordinatAlaniTuru","bagimsizAlanAdi"]].fillna('null')


if ( pd.isnull(alanAdi) ):
    # alanAdi= np.nan_to_num(alanAdi)
    alanAdi = 'null'

if (  pd.isnull(alaniTuru) ):             ###np.isnan(alaniTuru)
    # alaniTuru =np.nan_to_num(alaniTuru)
    alaniTuru = 'null'



df_morethan2 = df_group[ df_group['Count']>2 ]



df_parcel_x = df[
                    (df["lisans_id"]== l_id) &
                    (df["tesis_id"]== t_id) &
                    (df["koordinatAlaniTuru"]== alaniTuru) &
                    (df["bagimsizAlanAdi"]== alanAdi)
                ].longitude

df_parcel_y = df[
                    (df["lisans_id"]== l_id) &
                    (df["tesis_id"]== t_id) &
                    (df["koordinatAlaniTuru"]== alaniTuru) &
                    (df["bagimsizAlanAdi"]== alanAdi)
                ].latitude


df_parcel_sorting = df[
                    (df["lisans_id"]== l_id) &
                    (df["tesis_id"]== t_id) &
                    (df["koordinatAlaniTuru"]== alaniTuru) &
                    (df["bagimsizAlanAdi"]== alanAdi)
                ].adi


a1 = df_parcel_sorting.values
a2 = df_parcel_sorting.index

a3 = df_parcel_sorting.to_list()
a3.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

a3 = pd.DataFrame(data=a3, index=a3, columns=["adi"])
a4 = np.vstack((a2,a1, df_parcel_x,df_parcel_y )).T
a4 = pd.DataFrame(data=a4, index=a1, columns=["index","adi","x","y"])

a_son = pd.merge(a3, a4, on="adi")             ### inner join 1!!


wkt = "POLYGON (("

for i in range(0, len(a_son)):
    # s +=  str( df['x'].loc[i] )                 ## loc shows index 
    # s +=  str( df[df["lisans_id"]==32377].x.to_numpy()[i] )
    wkt +=  str( a_son["x"][i] )
    wkt += " "
    wkt +=  str( a_son["y"][i] )
    wkt += ","
    
wkt += str(  a_son["x"][0] )  + " " + str(  a_son["y"][0] ) + "))" 

# geom = shapely.wkt.loads(wkt)
geom = ogr.CreateGeometryFromWkt(wkt)






## To crete SHP file
driver = ogr.GetDriverByName('Esri Shapefile')
driver.DeleteDataSource('my.shp')
ds = driver.CreateDataSource('my.shp')
layer = ds.CreateLayer('', None, ogr.wkbPolygon)

# Add one attribute
layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn('lisans_id', ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn('tesis_id', ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn('koordinatAlaniTuru', ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn('bagimsizAlanAdi', ogr.OFTInteger))
defn = layer.GetLayerDefn()

# Create a new feature (attribute and geometry)
feature = ogr.Feature(defn)
feature.SetField('id', 1)
feature.SetField("lisans_id", l_id)
feature.SetField("tesis_id", t_id)
feature.SetField("koordinatAlaniTuru", alaniTuru)
feature.SetField("bagimsizAlanAdi", alanAdi)


# Make a geometry
feature.SetGeometry(geom)

layer.CreateFeature(feature)
feature = geom = None 

# Save and close everything
ds = layer = feat = geom = None




