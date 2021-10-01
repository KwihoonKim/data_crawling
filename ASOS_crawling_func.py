# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 13:26:29 2021

@author: Kwihoon
"""
"""
참고사이트 -> https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15057210
"""

from urllib.parse import urlencode, unquote, quote_plus 
import urllib 
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
    
def prec_table(startDt, endDt, stnIds, pageNo):
    startDt = str(startDt)
    endDt = str(endDt)
    stnIds = str(stnIds)
    pageNo = str(pageNo)
    url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList'
    open_api_key = "A1puTRqIGilbZ5ysD619HWAJOqzTULbMIyx8McBXXQcEdFMiWsE0pVv14A4ae4xd06d5Hdu5Q+ADFqm/KRZZjw=="
    params = '?' + urlencode({ quote_plus("dataType"): "XML",\
                          quote_plus("dataCd"): "ASOS",\
                          quote_plus("dateCd"): "HR",\
                          quote_plus("startDt"): startDt,\
                          quote_plus("startHh"): "00",\
                          quote_plus("endDt"): endDt,\
                          quote_plus("endHh") : "23",\
                          quote_plus("stnIds"): stnIds,\
                          quote_plus("pageNo"): pageNo,\
                          quote_plus("numOfRows"): "999",\
                          quote_plus("ServiceKey"): open_api_key }) 
    open_url = url + params
    req = requests.get(open_url)
    soup = BeautifulSoup(req.text, 'html')
    precs = soup.find_all('rn')
    times = soup.find_all('tm')        

    precs_list = []
    times_list = []
    years_list = []
    months_list = []
    days_list = []
    hours_list = []

    for i, prec in enumerate(precs):
        prec = prec.string
        time = times[i].string 
        if prec == None:
            prec = 0
        else:
            prec = int(float(prec)*10)
        precs_list.append(prec)
        times_list.append(time)
        
        year = int(time.split('-')[0])
        month = int(time.split('-')[1])
        day = int(time.split('-')[2].split(' ')[0])
        hour = int(time.split('-')[2].split(' ')[1].split(':')[0])

        years_list.append(year)
        months_list.append(month)
        days_list.append(day)
        hours_list.append(hour)

    years_list = np.array(years_list)
    months_list = np.array(months_list)
    days_list = np.array(days_list)
    hours_list = np.array(hours_list)
    precs_list = np.array(precs_list)

    table = np.column_stack([years_list, months_list, days_list, hours_list, precs_list])
    return table

test = []
test1 = []
stnIds = 156
test = prec_table(19900101, 19901231, stnIds, 1)
for j in range(30):
    for i in range(10):
        test1 = prec_table(19900101+j*10000, 19901231+j*10000, stnIds, i+1)
        test = np.concatenate([test,test1])
        print(i)
    print(j)
    
np.savetxt('test156.csv', test, delimiter = ',')




