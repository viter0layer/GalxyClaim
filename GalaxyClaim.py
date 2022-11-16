from web3 import Web3
from eth_account.messages import encode_defunct
from web3.auto import w3
from eth_account import Account
from requests import post
from json import loads
from fake_useragent import UserAgent
from loguru import logger
from os import system
from ctypes import windll
from sys import stderr
from time import sleep
from msvcrt import getch

system("cls")
clear = lambda: system('cls')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <level>{message}</level>")

filesfolder = str(input('Drop your TXT with privatekeys here \n>> '))

with open(filesfolder, 'r') as file:
    clear()
    for private_key in file:
        try:
            GAME_CONTRACT_ADDRESS = '0x5c1274456be4dd280429b9a8319e552cad2595fa'

            web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
            acc = Account.from_key(private_key.strip())
            nonce = web3.eth.getTransactionCount(acc.address)
            gasprice = web3.toWei('5', 'gwei')
            r = post('https://graphigo.prd.galaxy.eco/query', json={"operationName":"PrepareParticipate","variables":{"input":{"signature":"","campaignID":"GCRkYUUH6m","address":acc.address,"mintCount":1,"chain":"BSC"}},"query":"mutation PrepareParticipate($input: PrepareParticipateInput!) {\n  prepareParticipate(input: $input) {\n    allow\n    disallowReason\n    signature\n    mintFuncInfo {\n      funcName\n      nftCoreAddress\n      verifyIDs\n      powahs\n      cap\n      __typename\n    }\n    extLinkResp {\n      success\n      data\n      error\n      __typename\n    }\n    metaTxResp {\n      metaSig2\n      autoTaskUrl\n      metaSpaceAddr\n      forwarderAddr\n      __typename\n    }\n    __typename\n  }\n}\n"}, headers={'user-agent': UserAgent().random, 'accept': '*/*', 'Accept-Language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'authorization': 'null', 'content-type': 'application/json', 'Origin': 'https://galaxy.eco', 'Referer': 'https://galaxy.eco/'})
            if loads(r.text)['data']['prepareParticipate']['allow'] != True:
                logger.error(f'[{acc.address}] unaviable to claim')
                continue
            sign = loads(r.text)['data']['prepareParticipate']['signature']
            verifyid = loads(r.text)['data']['prepareParticipate']['mintFuncInfo']['verifyIDs'][0]
            tx = {
                'nonce': nonce,
                'to': Web3.toChecksumAddress(GAME_CONTRACT_ADDRESS),
                'value': 0,
                'gas': 300000,
                'gasPrice': gasprice,
                'data': '0x2e4dbe8f000000000000000000000000000000000000000000000000000000000000028700000000000000000000000009fe144196e7d2446c781ff271483337b1c9c5cd000000000000000000000000000000000000000000000000000000000'+str(hex(verifyid))[2:]+'000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000041'+str(sign)[2:]+'00000000000000000000000000000000000000000000000000000000000000',
            }
            signed_tx = acc.signTransaction(tx)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            logger.success(f'[{acc.address}] Cycle done, tx: {web3.toHex(tx_hash)}')
            tx_res = web3.eth.waitForTransactionReceipt(tx_hash)
        except Exception as error:
            logger.error(f'Error: {error}')
            continue

logger.success('Работа успешно завершена!')
print('Нажмите любую клавишу для выхода...')
getch()
exit()

