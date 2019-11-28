'''
@Author: Muhaowei
@Date: 2019-09-23 10:59:12
@LastEditors: Muhaowei
@LastEditTime: 2019-11-01 23:16:58
@Description: 
'''

import re
import numpy as np


def mathdata(num, His):
    pattern = str(num) + '=\d+.\d+'
    Data = re.findall(pattern, His)
    DataStr = ''.join(Data).replace(str(num) + '=', '')
    return DataStr


csvFile = open("THisFeatures.csv", "r").readlines()
fileNew = open('THis.csv', 'w')

for line in csvFile:
    # print(line)
    Index = line.split(',{')[0]
    His = line.split(',{')[1].replace('}', '')
    # print(His)
    # for i in range(80):
    #    Data0 = mathdata(0, His)
    Data0 = mathdata(0, His)
    Data1 = mathdata(1, His)
    Data2 = mathdata(2, His)
    Data3 = mathdata(3, His)
    Data4 = mathdata(4, His)
    Data5 = mathdata(5, His)
    Data6 = mathdata(6, His)
    Data7 = mathdata(7, His)
    lineData = np.array(
        [Index, Data0, Data1, Data2, Data3, Data4, Data5, Data6, Data7])

    lineData[lineData == ''] = '0'
    # print(lineData)
    lineNew = ','.join(lineData) + '\n'
    fileNew.write(lineNew)
# print(csvFile)
