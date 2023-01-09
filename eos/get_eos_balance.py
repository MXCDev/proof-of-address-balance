# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError,Timeout
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class EOSCommon:

    def request(self,url:str,data:dict,header:dict):
        '''
        Send request
        :param url:send request address
        :param data:send request data
        :param header:send request header
        :return:
        '''
        try:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            retry_times = HTTPAdapter(max_retries=10)
            session = requests.Session()
            session.mount(url, retry_times)
            response = session.post(url,json=data,timeout=10,headers=header,verify=False)
            return response.json()
        except Exception as e :
            pass
        except ConnectionError as ce:
            pass
        except Timeout as te :
            pass

    def get_balance(self,url:str,address:str,block:int,contract:str=None):
        '''
        get eos balance
        :param url: eos public node
        :param address: search eos address
        :param block: search balance of eos address at block
        :param contract: search balance of eos address about contract
        :return:
        '''
        try:
            data = {"account":address,"code":contract,"symbol":"USDT"}
            headers = {"Content type":"application/json"}
            result = self.request("{}/v1/chain/get_currency_balance".format(url),data,headers)
            if result == []:
                return 0
            return result[0].split(" ")[0]
        except Exception as e:
            return
