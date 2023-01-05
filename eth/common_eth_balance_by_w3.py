# !/usr/bin/env python
# -*- coding: utf-8 -*-

from web3 import Web3,HTTPProvider
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
from decimal import Decimal

class ETHCommonW3:

    def __init__(self,url):
        '''
        :param url: public url node
        '''
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.w3 = Web3(HTTPProvider(url,request_kwargs={"verify":False}))
        self.CONTRACT_ABI = [{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],
                              "payable":False,"stateMutability":"view","type":"function"},
                             {"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],
                              "name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},
                             {"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},
                             {"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],
                              "name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},
                             {"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},
                             {"constant":False,"inputs":[{"name":"_value","type":"uint256"}],"name":"burn","outputs":[{"name":"success","type":"bool"}],
                              "payable":False,"stateMutability":"nonpayable","type":"function"},
                             {"constant":True,"inputs":[{"name":"_to","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},
                             {"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_value","type":"uint256"}],"name":"burnFrom","outputs":[{"name":"success","type":"bool"}],
                              "payable":False,"stateMutability":"nonpayable","type":"function"},
                             {"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},
                             {"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],
                              "payable":False,"stateMutability":"nonpayable","type":"function"},
                             {"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"},{"name":"_extraData","type":"bytes"}],
                              "name":"approveAndCall","outputs":[{"name":"success","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},
                             {"constant":True,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],
                              "payable":False,"stateMutability":"view","type":"function"},
                             {"inputs":[{"name":"initialSupply","type":"uint256"},{"name":"tokenName","type":"string"},{"name":"tokenSymbol","type":"string"}],
                              "payable":False,"stateMutability":"nonpayable","type":"constructor"},
                             {"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],
                              "name":"Transfer","type":"event"},
                             {"anonymous":False,"inputs":[{"indexed":True,"name":"owner","type":"address"},{"indexed":True,"name":"spender","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],
                              "name":"Approval","type":"event"},
                             {"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Burn","type":"event"},
                             { "constant": False,"inputs": [{"name": "term", "type": "uint256"}],"name":"claimRank","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"}]

        self.denomination = {"wei":Decimal(1),
                             "kwei":Decimal(1000),
                             "mwei":Decimal(1000000),
                             "gwei":Decimal(1000000000),
                             "szabo":Decimal(1000000000000),
                             "finney":Decimal(1000000000000000),
                             "ether":Decimal(1000000000000000000),
                             "kether":Decimal(1000000000000000000000),
                             "mether":Decimal(1000000000000000000000000),
                             "gether":Decimal(1000000000000000000000000000),
                             "tether":Decimal(1000000000000000000000000000000)}

    def get_balance(self, address: str, block: int, contract=None):
        '''
        获取对应地址的余额(Get the balance of the corresponding address)
        :param address: 查询余额的地址(get balance address)
        :param contract: 查询代笔的余额对应的合约 (contract of token coin)
        :param block: 高度(height to be queried)
        :return:number

        E.G.
        conn = Common("https://bsc-dataseed1.ninicoin.io")
        address = "0xE949C429E234B371DCeD4630fdFCE59fc01a9a85"
        contract = "0xfD0fD32A20532ad690731c2685d77c351015ebBa"
        balance = conn.get_balance(address)
        balance_token = conn.get_balance(address,contract)

        result:
        0.179951015498914253
        460.00000000000000001
        '''
        if not contract:
            return self.w3.fromWei(
                self.w3.eth.get_balance(
                    account=self.w3.toChecksumAddress(address),
                    block_identifier=block),
                "ether")
        else:
            contract_w3 = self.w3.eth.contract(
                address=self.w3.toChecksumAddress(self.w3.toChecksumAddress(contract)),
                abi=self.CONTRACT_ABI)
            return self.w3.fromWei(
                contract_w3.functions.balanceOf(
                    self.w3.toChecksumAddress(address)).call(block_identifier=block),
                self.get_decimal(contract))

    def get_decimal(self, contract: str):
        if not contract:
            return "ether"
        contract_w3 = self.w3.eth.contract(
            address = self.w3.toChecksumAddress(self.w3.toChecksumAddress(contract)),
            abi=self.CONTRACT_ABI)
        decimal = Decimal(contract_w3.functions.decimals().call())
        for key,value in self.denomination.items():
            if 10 ** decimal == value:
                return key