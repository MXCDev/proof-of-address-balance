# !/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

class ArbitrumOne(Enum):
    ArbitrumOne_URL = "https://rpc.ankr.com/arbitrum"
    ArbitrumOne_SNAPSHOT_BLOCK_ETH = 47962646
    ArbitrumOne_SNAPSHOT_BLOCK_USDT = 47962616
    ArbitrumOne_USDT_CONTRACT = "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9"

class ETH(Enum):
    ETH_URL = "https://eth-mainnet.public.blastapi.io"
    ETH_SNAPSHOT_BLOCK_ETH = 16320144
    ETH_SNAPSHOT_BLOCK_USDC = 16320144
    ETH_SNAPSHOT_BLOCK_USDT = 16320144
    ETH_USDT_CONTRACT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    ETH_USDC_CONTRACT = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

class BSC(Enum):
    BSC_URL = "https://bsc-dataseed1.ninicoin.io"
    BSC_SNAPSHOT_BLOCK_ETH = 24117164
    BSC_SNAPSHOT_BLOCK_BTC = 24117154
    BSC_SNAPSHOT_BLOCK_USDT = 24117144
    BSC_SNAPSHOT_BLOCK_USDC = 24117134
    BSC_USDT_CONTRACT = "0x55d398326f99059ff775485246999027b3197955"
    BSC_ETH_CONTRACT = "0x2170ed0880ac9a755fd29b2688956bd959f933f8"
    BSC_USDC_CONTRACT = "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"
    BSC_BTC_CONTRACT = "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c"

class TRX(Enum):
    TRX_URL = "https://www.oklink.com/api/v5/explorer/block/address-balance-history"
    TRX_SNAPSHOT_BLOCK_USDT = 47361343
    TRX_ETH_CONTRACT = "THb4CqiFdwNHsWsQCs4JhzwjMWys4aqCbF"
    TRX_USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    TRX_USDC_CONTRACT = "TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8"
    TRX_BTC_CONTRACT = "TN3W4H6rK2ce4vX9YnFQHwKENnHjoxb3m9"

class SOL(Enum):
    SOL_URL = "https://api.mainnet-beta.solana.com"
    SOL_SNAPSHOT_BLOCK_USDT = 139056003
    SOL_SNAPSHOT_BLOCK_USDC = 170463062
    SOL_USDT_CONTRACT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    SOL_USDC_CONTRACT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

class HECO(Enum):
    HECO_URL = "https://http-mainnet.hecochain.com"
    HECO_SNAPSHOT_BLOCK_USDT = 21598873
    HECO_USDT_CONTRACT = "0xa71edc38d189767582c38a3145b5873052c3e47a"

class MATIC(Enum):
    MATIC_URL = "https://polygon-rpc.com"
    MATIC_SNAPSHOT_BLOCK_USDT = 37128238
    MATIC_SNAPSHOT_BLOCK_USDC = 37128138
    MATIC_USDT_CONTRACT = "0xc2132d05d31c914a87c6611c10748aeb04b58e8f"
    MATIC_USDC_CONTRACT = "0x2791bca1f2de4661ed88a30c99a7a9449aa84174"

class OKC(Enum):
    OKC_URL = "https://exchainrpc.okex.org"
    OKC_SNAPSHOT_BLOCK_USDT = 16166795
    OKC_USDT_CONTRACT = "0x382bb369d343125bfb2117af9c149795c6c65c50"

class ALGO(Enum):
    ALGO_URL = "https://algoindexer.algoexplorerapi.io"
    ALGO_SNAPSHOT_BLOCK_USDT = 25720141
    ALGO_SNAPSHOT_BLOCK_USDC = 25720041
    ALGO_USDT_CONTRACT = 312769
    ALGO_USDC_CONTRACT = 31566704

class OP(Enum):
    OP_URL = "https://mainnet.optimism.io"
    OP_SNAPSHOT_BLOCK_USDT = 53325381
    OP_SNAPSHOT_BLOCK_ETH = 53325361
    OP_USDT_CONTRACT = "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58"

class EOS(Enum):
    EOS_URL = "https://eos.greymass.com"
    EOS_SNAPSHOT_BLOCK_USDT = 16232175
    EOS_USDT_CONTRACT = "tethertether"

class BTC(Enum):
    BTC_URL = ""
    BTC_SNAPSHOT_BLOCK = 16232175

class ZKSYNC(Enum):
    ZKSYNC_URL = "https://api.zksync.io/jsrpc"
    ZKSYNC_SNAPSHOT_BLOCK_ETH = 16232175

COMMON_INFO = {
    "ETH":["Arbitrum One","BEP20(BSC)","ERC20","HECO","MATIC","OP","OKC","ZKSYNC"],
    "TRX":"TRC20"
}