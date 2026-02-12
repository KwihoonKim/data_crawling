# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 2026

@author: Kwihoon
"""
"""
참고사이트 -> https://www.data.go.kr/data/15099919/openapi.do
"""

from urllib.parse import urlencode, unquote, quote_plus 
import urllib 
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
    
def level_table(fac_code, startDt, endDt, stnIds, pageNo):
    startDt = str(startDt)
    endDt = str(endDt)
    stnIds = str(stnIds)
    pageNo = str(pageNo)
    
    fac_code = "4423010045"
    startDt = "20150901"
    endDt = "20150931"

    url = 'http://apis.data.go.kr/B552149/reserviorWaterLevel/reservoirlevel/'
    # 인증키는 개별 고유값으로 (마이페이지->Open API->인증키 발급현황) 확인가능
    encoding_api_key = "API Key"
    decoding_api_key = 'API Key'
    params = '?' + urlencode({ quote_plus("fac_code"): fac_code,\
                          quote_plus("date_s"): startDt,\
                          quote_plus("date_e"): endDt,\
                          quote_plus("serviceKey"): encoding_api_key,\
                          quote_plus("numOfRows"): "30",\
                          quote_plus("pageNo"): "1",\
                          quote_plus("county"): "충청남도" }) 
    params = params.replace('25','')
    open_url = url + params
    req = requests.get(open_url)
    soup = BeautifulSoup(req.text, 'html')
    levels = soup.find_all('water_level')
    rates = soup.find_all('rate')        
    times = soup.find_all('check_date')        

    levels_list = []
    rates_list = []
    times_list = []

    for i, time in enumerate(times):
        level = levels[i].string
        rate = rates[i].string
        time = times[i].string 
        
        level = float(level)
        rate = float(rate)
        
        levels_list.append(level)
        rates_list.append(rate)
        times_list.append(time)

    levels_list = np.array(levels_list)
    rates_list = np.array(rates_list)
    times_list = np.array(times_list)

    table = np.column_stack([times_list, levels_list, rates_list])
    return table