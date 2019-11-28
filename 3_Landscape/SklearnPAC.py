'''
@Author: Muhaowei
@Date: 2019-10-01 22:01:39
@LastEditors: Muhaowei
@LastEditTime: 2019-10-08 14:39:06
@Description: 
'''
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np

RSdata = pd.read_csv('Data.csv')
# print(RSdata)
training_data = np.array(RSdata.iloc[:, 1:])
# print(training_data)

Dim_Set = []
mean_values = np.mean(training_data, axis=0)
std_mat = (training_data - mean_values) / np.std(training_data, axis=0, ddof=1)
# print(std_mat)

pca = PCA(n_components=2)
newData = pca.fit_transform(std_mat)
PCs = pca.components_
# print(PCs)
# for Cat_Num in range(len(std_mat)):
#     pca = PCA()
#     # print(std_mat[:, Cat_Num])
#     # print(std_mat[:, Cat_Num].shape)
#     pca.fit(std_mat[:, Cat_Num])
#     # 累计贡献率 又名 累计方差贡献率 不要简单理解为 解释方差！！！
#     EV_List = pca.explained_variance_
#     EVR_List = []
#     for j in range(len(EV_List)):
#         EVR_List.append(EV_List[j] / EV_List[0])
#     for j in range(len(EVR_List)):
#         if (EVR_List[j] < 0.10):
#             Dim = j
#             break
#     Dim_Set.append(Dim)

# print(newData)
# print(newData.shape)

fileNew = open('PacResult1.csv', 'w')
training_id = np.array(RSdata.iloc[:, 0]).reshape(702, 1)
# print(training_id)
# print(training_id.shape)
FinallyData = np.hstack((training_id, newData))
# print(FinallyData)
for i in FinallyData:
    # print(i)
    # print(i[0])
    line = str(i[0]) + ',' + str(i[1]) + ',' + str(i[2]) + '\n'
    fileNew.write(line)
    # break
