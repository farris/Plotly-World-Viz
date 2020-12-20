#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 19:39:27 2020

@author: farrisatif
"""
import pandas as pd
import numpy as np
import json
import plotly.express as px


import plotly.io as pio



from plotly import graph_objects

data = pd.read_csv('economic_freedom_index2019_data.csv', encoding='latin-1')
null_c = data[data['World Rank'].isnull()] ## countries w nan values, need to be removed
data = data[data['World Rank'].notna()] #### remove those countries
no = data.columns[data.isna().any()].tolist() ### columns w nan values, need to be removed
data = data.drop(no,axis=1) #### remove those columns
data = data.drop(['Country'],axis=1) ### Drop column b/c it messes w loop

columns = list(data.columns.values) 

# ##############################################################

data = data.replace(',','', regex=True)
data[columns[22]] = data[columns[22]].str.replace('$', '')
data[columns[24]] = data[columns[24]].str.replace('$', '')
data.loc[88,[columns[22]]] = 40 ###hardcode
data.loc[88,[columns[24]]] = 1700 ##hardcode
# store = []
# for i in (range(7,24)):
#     b = np.corrcoef(data['World Rank'].to_numpy(),data[columns[int(i)]].to_numpy(dtype = float))
#     store.append([np.abs(b[0,1]),columns[i]])
# df = pd.DataFrame(store, columns=['Correlation', 'Feature'])    
# print(df.sort_values('Correlation' , ascending=False))

dataECON = data
dataHD = pd.read_csv('human_development.csv', encoding='latin-1')
dataHD = dataHD.iloc[:188,[i for i in range(8) ] ]
null_data = dataHD[dataHD.isnull().any(axis=1)]
dataEDU = dataHD.loc[:,['Country','Mean Years of Education']]
#dataEDU = dataHD.iloc[:188,[i for i in range(8) ] ]
dataEDU=  dataEDU.set_index(['Country'])
dataECON = dataECON.set_index(['Country Name'])
dataECON = dataECON['World Rank']
df = pd.merge(dataECON,dataEDU,left_index=True, right_index=True)


# map1 = json.load(open('custom.geo.json','r'))
# id_map = {}
# for feature in map1["features"]:
#     feature["id"] = feature["properties"]["gdp_md_est"]
#     id_map[feature["properties"]["name_long"]] = feature["id"]


# idx = df.index.tolist()
# for i in idx:
#      if i not in id_map: 
#           df = df.drop([i])





# %%

map3 = json.load(open('countries.geojson','r'))
for i in range(255):
    (map3['features'][i]['id']) = i

id_map = {}
for feature in map3["features"]:

    id_map[feature["properties"]["ADMIN"]] = feature["id"]




df  = df.reset_index() 
#df.at[151,'index']='United States of America'
s = df['index'].tolist()

store1 =[]

for key in id_map:  ## check to see if in original df
    b = key in s
    if b == False:
        store1.append(key)

s = df['index'].tolist()
for s in store1: 
    del id_map[s]

s = df['index'].tolist()   
for i in s:
    if i not in id_map:
        df = df[df['index'] != i]
      
df["id"] = df["index"].apply(lambda x: id_map[x])


# %%
# import plotly.graph_objects as go
# pio.renderers.default='browser'
# g  = ['World Rank','Mean Years of Education']
# for i in range(2):
#     fig = go.Figure(go.Choroplethmapbox(geojson=map3, locations=df.id, z=df[g[i]],
#                                         colorscale="Viridis", zmin=0, zmax= np.max((df['World Rank'].to_numpy())),
#                                         marker_opacity=0.5, marker_line_width=0))
#     fig.update_layout(mapbox_style="carto-positron",
#                       mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#     fig.show()
    
#     updatemenus = list([dict(buttons=list()), 
#                         dict(direction='down',
#                              showactive=True)])

# %%
df = df.set_index('index')
import plotly.express as px
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import plotly.graph_objects as go
traces=[]
metrics = np.array(['World Rank','Mean Years of Education'])
for metric in metrics:
    traces.append(go.Choropleth(locations=df.index.tolist(),
                                locationmode='country names',
                                z=df[metric],
                                colorscale='Portland',
                                marker_line_color='darkgray',
                                marker_line_width=0.5,
                                text= df.index.tolist(),
                                reversescale=True,
                                colorbar = {'title':metric, 'len':200,'lenmode':'pixels' },
                                visible=True if metric== 'World Rank' else False)
                 )
    
data = dict(type = 'choropleth',
            locations = df.index.tolist(),
            locationmode = 'country names',
            colorscale= 'Portland',
            marker_line_color='darkgray',
            marker_line_width=0.5,
            reversescale=True,
            z=df['World Rank'].tolist(),
            colorbar = {'title':metric, 'len':200,'lenmode':'pixels' })


updatemenus = []
metrics = np.array(['World Rank','Mean Years of Education'])

buttons=[]
for metric in metrics:
    # May also need colorbox title?
    buttons.append(dict(method='update',
                        label=metric,
                        args=[{'visible': metrics==metric}])
                  )
    
dropdown = dict(buttons=buttons, direction='down',x = 0.01,xanchor = 'left',
                y = 0.99,yanchor = 'bottom',font = dict(size=11))
updatemenus=[dropdown] # If we want multiple dropdowns, add em to the list!
layout = dict(updatemenus=updatemenus,
              title='Title')
    
col_map = go.Figure(data = traces,layout = layout)
iplot(col_map)
















