#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from dotenv import dotenv_values

from ArticutAPI import Articut
from pprint import pprint

config = dotenv_values('.env')

#取得金鑰
username = config["ARTICUT_USERNAME"]
apikey = config["ARTICUT_PASSWORD"]
articut = Articut(username, apikey)




def main(inputSTR):
	articut = Articut(username=username, apikey=apikey)
	resultDICT = articut.parse(inputSTR)
	return resultDICT

def GetAddress(inputAddress):
    Address = main(inputAddress)
    add = articut.getLocationStemLIST(Address)
    return add



inputSTR = inputSTR = """以原告就訴訟標的所有之利益為準。民事訴訟法第77條之1第2 項定有明文。查原告起訴請求被告將，地址是高雄市三民區長榮路臉書。""".replace(" ","").replace("\n","")
resultDICT = main(inputSTR)
#pprint(resultDICT)

print(GetAddress(inputSTR))
