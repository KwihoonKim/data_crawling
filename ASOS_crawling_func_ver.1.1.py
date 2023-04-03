# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 13:26:29 2021
revised on Mon Sep 26 2022
@author: Kwihoon
email: kgh0330@snu.ac.kr

"""
"""
참고사이트 -> https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15057210
1. data.go.kr 가입
2. 기상청_지상(종관, ASOS) 일자료 조회서비스 --> 서비스 사용신청
3. open_api_key 변수는 본인 아이디 key 찾아서 바꿔주기
4. 오픈 API 활용가이드.doc에서 필요한 항목 찾은 후 아래에 항목 추가해주기
5. 원하는 기상관측소 코드를 배열에 추가해주기
6. 원하는 연도를 입력
"""

from urllib.parse import urlencode, unquote, quote_plus 
import urllib 
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import json

'''
94개소 대상 테스트                                                                                            ===================> 5번 항목에 해당
==========================================================================================================================================
'''

stnIds = [90,93,95,98,99,100,101,102,104,105,106,108,112,114,115,119,121,127,129,130,131,133,135,136,137,138,140,143,146,152,155,156,159,
          162,165,168,169,170,172,174,177,184,185,188,189,192,201,202,203,211,212,216,217,221,226,232,235,236,238,239,243,244,245,247,248,
          251,252,253,254,255,257,258,259,260,261,262,263,264,266,268,271,272,273,276,277,278,279,281,283,284,285,288,289,294,295]
'''
==========================================================================================================================================
'''

def xxx(js):  
    try:
        json_object = json.loads(js)
    except ValueError as e:
        return False
    return True

def prec_table(startYe, stnIds):
    startDt = str(startYe)+'0101'
    endDt = str(startYe) + '1231'
    stnIds = str(stnIds)
    url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
    open_api_key = "A1puTRqIGilbZ5ysD619HWAJOqzTULbMIyx8McBXXQcEdFMiWsE0pVv14A4ae4xd06d5Hdu5Q+ADFqm/KRZZjw==" #===================> 3번 항목에 해당
    params = {'serviceKey': open_api_key,
              'numOfRows': '400',
              'pageNo': '1',
              'dataType': 'JSON',
              'dataCd': 'ASOS',
              'dateCd': 'DAY',
              'startDt': startDt,
              'endDt': endDt,
              'stnIds': stnIds}
    result = None
    response = requests.get(url, params = params) 
    js = response.text
        
    while xxx(js) == False:
        response = requests.get(url, params = params)
        js = response.text
        
    result = json.loads(js)
    
    try:
        items = result['response']['body']['items']['item']
        items = pd.DataFrame(items)
        times = items['tm']
        tmax = items['maxTa'] 
        tmin = items['minTa'] 
        wind = items['avgWs'] 
        rhum = items['avgRhm'] 
        rsds = items['sumGsr'] 
        
        
        # 원하는 변수 찾아서 time, precs 같이 추가                                                             ===================> 4번 항목에 해당
        table = np.column_stack([times, tmax, tmin, wind, rhum, rsds])
        
        # 위에서 만들어준 변수 명을 대괄호 안에 넣어주기                                                        ===================> 4번 항목에 해당
        
    except:
        print('해당기간 자료가 없습니다.')
        times = 0
        tmax = 0
        tmin = 0
        wind = 0
        rhum = 0
        rsds = 0
        table = np.column_stack([times, tmax, tmin, wind, rhum, rsds])
        # 위에서 만들어준 변수 명을 대괄호 안에 넣어주기                                                        ===================> 4번 항목에 해당
    return table




'''
stnIds: 관측소 번호
startYe: 시작연도
prec_table(startYe, stnIds) 입력 시, 변수 값을 얻을 수 있음.
'''
startYe = 1950                                                                                              
# 시작연도 입력해주기                                                                                           ===================> 5번 항목에 해당


for ids in stnIds:
    test =  np.array([[0,0,0,0,0,0]])
    for i in range(72):
        test1 =  prec_table(startYe+i, ids)
        test = np.concatenate([test,test1])
        print(i)
    data = pd.DataFrame(test, columns = ['tm', 'tmax', 'tmin', 'wind', 'rhum', 'rsds'])
    data.to_csv('hourly_rainfall_'+str(ids)+'.csv')
    print(ids)


        

    
    
    