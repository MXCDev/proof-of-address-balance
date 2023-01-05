# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from decimal import Decimal
from requests.exceptions import ConnectionError,Timeout
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class ALGOCommon:

    def request(self,url:str,data:dict=None,header:dict=None):
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
            response = session.get(url,params=data,timeout=10,headers=header,verify=False)
            return response.json()
        except Exception as e :
            pass
        except ConnectionError as ce:
            pass
        except Timeout as te :
            pass

    def get_balance(self,url:str,address:str,block:int=None,contract:str=None):
        '''
        get algo balance
        :param url: algo public node
        :param address: search algo address
        :param block: search balance of algo address at block
        :param contract: search balance of algo address about contract
        :return:
        '''
        headers = {"Content-Type": "application/json"}
        url1 = "{}/v2/accounts/{}".format(url, address)
        results = self.request(url1, header=headers)
        decimal = self.get_asset(url,contract)
        for result in results['account']['assets']:
            if result['asset-id'] == contract:
                return Decimal(result['amount']) / 10 ** decimal

    def get_asset(self,url:str,contract:str):
        '''
        get asset of id
        :param url: algo public node
        :param contract: algo contract of id
        :return:
        '''
        headers = {"Content-Type": "application/json"}
        url = "{}/v2/assets/{}".format(url, contract)
        response = self.request(url, header=headers)
        results = response.json()['asset']['params']['decimals']
        return Decimal(results)