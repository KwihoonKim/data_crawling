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
    open_api_key = "key"
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


'''
65개소 대상 테스트
'''
stnIds = [127,114,202,90,203,211,101,108,95,99,119,112,201,104,105,106,216,271,136,272,273,137,143,281,284,285,289,192,288,152,159,130,277,138,295,294,155,162,238,\
226,131,236,232,129,140,235,245,243,244,247,170,174,262,168,156,260,175,261,251,165,169,185,184,189,187]

stnIds = [108,112,119,201,101,105,131,135,129,133,146,156,168,260,143,138,136,159,152,192,184]
ids = stnIds[0]
test = prec_table(20000101, 20000101, ids, 1)

def hourRain(stnIds):
    stnIds = [stnIds]
    for i, num in enumerate(stnIds):
        test = []
        test1 = []
        stnId = num
        test = prec_table(20000101, 20000101, stnId, 1)

        for j in range(21):
            for k in range(10):
                test1 = prec_table(20000101+j*10000, 20001231+j*10000, stnId, k+1)
                test = np.concatenate([test,test1])
            print(j)
        print(num)
# =============================================================================
#     np.savetxt('test'+str(i)+'.csv', test, delimiter = ',')
# =============================================================================
        np.savetxt('hourly_rainfall_'+str(num)+'.csv', test, delimiter = ',')
        
for i, num in enumerate(stnIds):
    test = []
    test1 = []
    stnId = num
    test = prec_table(20000101, 20000101, stnId, 1)

    for j in range(21):
        for k in range(10):
            test1 = prec_table(20000101+j*10000, 20001231+j*10000, stnId, k+1)
            test = np.concatenate([test,test1])
        print(j)
    print(num)
    np.savetxt('hourly_rainfall_'+str(num)+'.csv', test, delimiter = ',')
    

    
    
    
    