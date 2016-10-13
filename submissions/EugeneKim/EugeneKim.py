# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:35:33 2016

@author: e.a.kim

Data received from OpenData DC which is pulled from 
Restaurant Inspection data released by the DC Department of Health
"""
import os, sys, csv, rauth, math
import numpy as np
import pandas as pd

os.chdir('C:\Users\e.a.kim\Documents\Kaggle\Michelin')

# Read Data and set up
df = pd.read_csv("restaurants.csv", header=0 )
bad = pd.read_csv("inspections.csv", header=0)
yelp = pd.read_csv("yelp_crosswalk.csv", header = 0)

#%% Data Cleansing
df = df.drop(['Address','Lattitude', 'Longitude'], axis=1)
df = df.drop_duplicates('Name')

#%% Filter out restaurants without yelp
yelp = yelp.fillna(value = 0)
for index, x in yelp.iterrows():
    if x['YelpID'] == 0:
        df = df[df.permit_id != x['PermitID']]
yelp = yelp.drop_duplicates('YelpID')

#%% Filter out inspection violated restaurants
for index, x in bad.iterrows():
    if x['Critical_Violations'] > 0 or x['Non_Critical_Violations'] > 0:
        df = df[df.permit_id != x['permit_id']]
        yelp = yelp[yelp.PermitID != x['permit_id']]

#%% function to pull ratings from yelp API
def yelp_api( business_id ):
    #authentication header
    token = "w1LVuxMpFEu_41ys90r_45OvSkqnMKC51wMmmbcLS_UcqW8oSUZPEmHtibZL1sMw7s-j_xsS3njP41Yx8B0hGJr7eNAqQu1jQG41uo1izM67QfdfdIkIGV8B56H-V3Yx"
    session = rauth.OAuth2Session(access_token = token)
    business_id = str(business_id)
    request = session.get("https://api.yelp.com/v3/businesses/" + business_id)
    data = request.json()
    session.close()
    return data;

#%% Open Submission File
result_file = open("results.csv", "wb")
result_file_object = csv.writer(result_file)
result_file_object.writerow(['Name','Michelin Stars']) #header rows

#%% Predictions
for index, x in yelp.iterrows():
    api_call = yelp_api(x['YelpID'])
    rating = api_call['rating']
    if rating == 4.0:
        result_file_object.writerow([df['Name'][x['PermitID']==df.permit_id].values[0],'1'])
    elif rating == 4.5:
        result_file_object.writerow([df['Name'][x['PermitID']==df.permit_id].values[0],'2'])
    elif rating == 5:
        result_file_object.writerow([df['Name'][x['PermitID']==df.permit_id].values[0],'3'])
    continue

#%% Close Submission File
result_file.close()
