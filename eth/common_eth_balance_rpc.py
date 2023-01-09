# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from decimal import Decimal
from requests.exceptions import ConnectionError,Timeout
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class ETHCommon:

    def get_balance(self,url: str, address: str, block: int, contract: str=None):
        '''
        get common eth-like balance
        :param url: eth-like public node
        :param address: search balance of address
        :param block: search balance of block
        :param contract: search balance of contract
        :return:
        '''
        try:
            data = self.deal_params(address,contract,block)
            result = self.request(url,data)
            decimal = self.get_decimal(url,contract)
            value = self.deal_amount(result['result'],decimal)
            return value
        except KeyError as ke:
            return result

    def deal_params(self, address: str, contract: str, block: int):
        '''
        Assembly request data
        :param address:search balance of address
        :param contract:search balance of contract
        :param block:search balance of block
        :return:
        '''
        return {"jsonrpc":"2.0","method":"eth_getBalance","params":[address,hex(block)],"id":1} \
            if not contract else {"jsonrpc":"2.0",
                                  "method":"eth_call",
                                  "params":[{"to":contract,"data":self.get_data(address)},hex(block)],
                                  "id":1}

    def get_data(self,address,function="0x70a08231"):
        '''
        Get the inputdata of the query token
        :param address:search balance of address
        :param function:query token function
        :return:
        '''
        return "{}{}{}".format(function,"0" * 24, address[2:].lower())

    def get_decimal(self,url,contract):
        '''
        Get decimal of query token
        :param url:eth-like public node
        :param contract:search balance of contract
        :return:
        '''
        if not contract:
            return 18
        function = "0x313ce567"
        data = {"jsonrpc":"2.0",
                "method":"eth_call",
                "params":[{"to":contract,"data":function},"latest"],
                "id":1}
        result = self.request(url,data)
        return int(result['result'],16)

    def deal_amount(self,amount,decimal):
        '''
        calc balance
        :param amount:search balance amount
        :param decimal:The precision of the associated currency
        :return:
        '''
        amount = Decimal(int(amount,16))
        value = amount / 10 ** Decimal(decimal)
        return value

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
            response = session.post(url,json=data,timeout=10,verify=False)
            return response.json()
        except Exception as e :
            pass
        except ConnectionError as ce:
            pass
        except Timeout as te :
            pass
