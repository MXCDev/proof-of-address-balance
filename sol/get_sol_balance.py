# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError,Timeout
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class SOLCommon:

    def get_signature_for_address(self,url:str,address:str,limit:int=1,before:str=None,until:str=None):
        '''
        Get the signature information of the address
        :param url:sol public node
        :param address:search balance of address
        :param limit:Query limit num
        :param before:The data before the corresponding transaction of the query
        :param until:The corresponding transaction of the query until this transaction
        :return:
        '''
        data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [address,
                       {"until":until,"limit": limit,"before":before}]
                }
        result = self.request(url,data)
        for signature in result['result']:
            yield self.get_transaction(url,signature['signature'],contract,address)

    def get_balance(self,url:str,address:str,block:int,contract:str=None):
        '''
        Get sol balance
        :param url: sol public node
        :param address: search balance of address
        :param block: search balance of block
        :param contract: search balance of contract
        :return:
        '''
        data = {"jsonrpc": "2.0","id":1,
                "method":"getBlock",
                "params":[
                    block,
                    {"encoding": "json",
                     "maxSupportedTransactionVersion":0,
                     "transactionDetails":"full",
                     "rewards":False}
                ]}
        result = self.request(url,data)
        if not result:
            return "Please replace sol node url"
        try:
            for value in result['result']['transactions']:
                addresses = value['transaction']['message']['accountKeys']
                if address in addresses:
                    return self.get_transaction(url,value['transaction']["signatures"][0],contract)
        except Exception as e:
            return

    def get_transaction(self,url:str,signature:str,contract:str):
        '''
        Get the details of the corresponding transaction
        :param url:sol public node
        :param signature:sol transaction of hash
        :param contract:search balance of contract
        :return:
        '''
        data = {"jsonrpc": "2.0","id": 1,"method": "getTransaction","params": [signature,"json"]}
        result = self.request(url,data)
        try:
            for value in result['result']['meta']['postTokenBalances']:
                mint = value['mint']
                if mint == contract:
                    balance = value['uiTokenAmount']['uiAmountString']
                    return balance
        except Exception as e:
            return

    def request(self,url:str,data:dict):
        '''
        Send request
        :param url:send request address
        :param data:send request data
        :return:
        '''
        try:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            retry_times = HTTPAdapter(max_retries=10)
            session = requests.Session()
            session.mount(url, retry_times)
            response = session.post(url,json=data,timeout=10)
            return response.json()
        except Exception as e :
            pass
        except ConnectionError as ce:
            pass
        except Timeout as te :
            pass