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

# THisFeatures 是在GEE上导出的交通小区内不同像元的面积 可以用来做优势比例分析
# 0,{1=1767.7333333333333, 3=132.72156862745098, 2=257.9411764705883, 7=1362.8156862745097, 6=8062.364705882347, 4=468.0, 5=1502.0274509803905, 0=110.0}
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
