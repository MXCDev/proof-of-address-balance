# !/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import os
import datetime
from config.config import *
from itertools import product
from eth.common_eth_balance_rpc import ETHCommon
from sol.get_sol_balance import SOLCommon
from trx.get_trx_balance import TRXCommon
from algo.get_algo_balance import ALGOCommon
from eos.get_eos_balance import EOSCommon
import argparse

class Start:

    def read_excel(self,filename,**kwargs):
        '''
        read excel info
        :param filename: input file name
        :param kwargs: (chain:search chain name,address:search coin of address,name:search coin name)
        '''
        try:
            path = os.path.abspath(os.path.dirname(__file__))
            if not os.path.exists(os.path.join(path,filename)):
                return {"code":2,"msg":"You entered file name {} does not exist, please re-enter".format(filename)}
            work_book = xlrd.open_workbook(os.path.join(path,filename))
            work_sheet = work_book.sheets()[0]
            nrow,ncol = work_sheet.nrows,work_sheet.ncols
            temp = []
            for row,col in product(range(1,nrow),range(ncol)):
                temp.append(work_sheet.cell(row,col).value)
                if col == ncol - 1:
                    if kwargs == {}:
                        self.run(temp)
                    else:
                        if all([temp[2].lower() == kwargs['address'].lower(),
                                temp[0].upper() == kwargs['name'].upper(),
                                temp[1].upper() == kwargs["chain"].upper()]):
                            return self.run(temp)
                    temp = []
        except Exception as e:
            return e

    def run(self,values):
        '''
        Program entry
        :param values:array to be queried
        '''
        for key,infos in COMMON_INFO.items():
            if values[1] in infos:
                return self.dispatch("common_{}".format(key.lower()), values[0], values[1], values[2],int(values[-1]))
        return self.dispatch("common_{}".format(values[1].lower()), values[0], values[1], values[2],int(values[-1]))

    def dispatch(self,work,*args,**kwargs):
        '''
        scheduler program
        :param work:work module
        :param args:
        :param kwargs:
        '''
        try:
            return getattr(self, work)(*args,**kwargs)
        except AttributeError as ae:
            pass

    def deal_info(self,info):
        '''
        Process config information
        :param info:config parameter
        :return:
        '''
        try:
            return eval("{}.value".format(info))
        except Exception as e:
            return

    def common_func(self,conn,coin_name,wallet_name,address,height):
        '''
        Public processing module
        :param conn:Connection of different currencies
        :param coin_name:search coin name
        :param wallet_name:search chain name
        :param address:search address of coin name
        :param height: search balance in height
        '''
        url = self.deal_info("{}.{}_URL".format(wallet_name, wallet_name))
        contract = self.deal_info("{}.{}_{}_CONTRACT".format(wallet_name, wallet_name, coin_name))
        if not height or not url :
            return
        balance = conn.get_balance(url, address, height, contract)
        try:
            if balance is None:
                return
            if balance['error']['code'] :
                print("[{}] the node data is expired，please replace config {} url with other node. you can find in https://chainlist.org/zh ".format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),wallet_name))
                return
        except Exception as ke:
            print("[{}] address:{} network:{} balance:{} coin:{}\t height:{}".format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                address if len(address) == 58 else "{}{}".format(address," "*(58-len(address))),
                wallet_name if len(wallet_name) == 15 else "{}{}".format(wallet_name," "*(15-len(wallet_name))),
                balance if len(str(balance)) == 30 else "{}{}".format(str(balance)," "*(30-len(str(balance)))),
                coin_name,
                height))
            return {"code":1}

    def common_eth(self,*args):
        '''
        ETH-like query method
        :param args:
        :return:
        '''
        conn = ETHCommon()
        coin_name = args[0]
        wallet_name = args[1].replace(" ", "").replace("BEP20(BSC)", "BSC").replace("ERC20", "ETH")
        address = args[2]
        height = args[-1]
        return self.common_func(conn,coin_name,wallet_name,address,height)

    def common_sol(self,*args):
        '''
        SOL-like query method
        :param args:
        :return:
        '''
        conn = SOLCommon()
        return self.common_func(conn,*args)

    def common_trx(self,*args):
        '''
        TRON-like query method
        :param args:
        :return:
        '''
        conn = TRXCommon()
        coin_name = args[0]
        wallet_name = args[1].replace("TRC20", "TRX")
        address = args[2]
        height = args[-1]
        return self.common_func(conn,coin_name,wallet_name,address,height)

    def common_algo(self,*args):
        '''
        ALGO query method
        :param args:
        :return:
        '''
        conn = ALGOCommon()
        return self.common_func(conn, *args)

    def common_eos(self,*args):
        '''
        EOS query method
        :param args:
        :return:
        '''
        conn = EOSCommon()
        return self.common_func(conn, *args)

def main(chain,address,name,file):
    '''
    Main program
    :param chain:search chain name
    :param address:search address of coin name
    :param name:search coin name
    :param file:official data files
    :return:
    '''
    if not file:
        print("\033[31mPlease enter query file\033[0m")
        return

    start = Start()
    if all([not chain,not address,not name]):
        path = os.path.abspath(os.path.dirname(__file__))
        if not os.path.exists(os.path.join(path, file)):
            print("\033[31mYou entered file name {} does not exist, please re-enter\033[0m".format(file))
            return
        print("\033[32mStart ....\033[0m")
        start.read_excel(file)
        print("\033[32mQuery completed\033[0m")
        return

    if all([chain, address, name]):
        print("\033[32mStart search chain:{} address:{} coin name:{}\033[0m".format(chain,address,name))
        value = start.read_excel(file,chain=chain,address=address,name=name)
        if not value:
            print("\033[31mPlease check the parameters entered\033[0m")
            return
        elif value['code'] == 2:
            print("\033[31m{}\033[0m".format(value['msg']))
            return
        elif value['code'] != 1:
            print("\033[31mPlease check the parameters entered\033[0m")
            return
        else:
            print("\033[32mQuery completed\033[0m")
            return

    print("\033[31mPlease check whether the input parameters are missing\033[0m")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Query address balance")
    parser.add_argument("-c","--chain",type=str)
    parser.add_argument("-a","--address",type=str)
    parser.add_argument("-n","--name",type=str)
    parser.add_argument('-f',"--file",type=str)
    args = parser.parse_args()
    main(args.chain,args.address,args.name,args.file)
