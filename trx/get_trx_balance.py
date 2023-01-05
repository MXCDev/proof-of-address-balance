# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError,Timeout
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class TRXCommon:

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
            response = session.get(url,params=data,timeout=10,headers=header)
            return response.json()
        except Exception as e :
            pass
        except ConnectionError as ce:
            pass
        except Timeout as te :
            pass

    def get_balance(self,url:str, address:str, block:int ,contract:int=None):
        '''
        get tron balance
        :param url: tron public node
        :param address: search tron address
        :param block: search balance of tron address at block
        :param contract: search balance of tron address about contract
        :return:
        '''
        data = {"chainShortName":"tron",
                "height":block,
                "address":address,
                "tokenContractAddress":contract}
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': '*/*',
                   'Ok-Access-Key': 'a5a1a279-e445-4603-b76c-e1d4a7b9b67c',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        try:
            result = self.request(url,data,headers)
            return result['data'][0]["balance"]
        except Exception as e:
            return e