'''
@Author: Muhaowei
@Date: 2019-10-02 10:00:44
@LastEditors: Muhaowei
@LastEditTime: 2019-11-15 08:47:06
@Description: 
'''
import numpy as np
import pandas as pd

filename = 'Data.xls'  #要分析的文件名
tofile = 'pca.xls'  #保存所产生数据的文件名

df = pd.DataFrame(pd.read_excel(filename))  # 打开文件
data_mat = df.drop(df.columns[0], axis=1).values  # 删除第一列，即“地区”那一列

# PCA Algorithm begin
mean_values = np.mean(data_mat, axis=0)
std_mat = (data_mat - mean_values) / np.std(data_mat, axis=0, ddof=1)

cov_mat = np.cov(std_mat, rowvar=0)
eig_values, eig_vectors = np.linalg.eig(np.mat(cov_mat))

indices = np.argsort(eig_values)[::-1]
eig_values = eig_values[indices]
eig_vectors = eig_vectors[:, indices]

m = np.dot(std_mat, eig_vectors)
explained_variance_ratio = eig_values / sum(eig_values)  # 计算贡献率
explained_variance_ratio_cumulative = np.cumsum(
    explained_variance_ratio)  # 计算累计贡献率
# PCA Algorithm end

writer = pd.ExcelWriter(tofile)

# 写入相关系数矩阵
data_df = pd.DataFrame(cov_mat)
data_df.columns = df.columns[1:]
data_df.index = df.columns[1:]
data_df.to_excel(writer, 'Correlation Matrix', float_format='%.5f')
writer.save()

eigenvalues = {
    'component': [],
    'value': [],
    'difference': [],
    'proportion': [],
    'cumulative': []
}
for i in range(len(explained_variance_ratio)):
    eigenvalues['component'].append(i + 1)
    eigenvalues['value'].append(eig_values[i])
    if i != len(explained_variance_ratio) - 1:
        eigenvalues['difference'].append(eig_values[i] - eig_values[i + 1])
    else:
        eigenvalues['difference'].append(0)
    eigenvalues['proportion'].append(explained_variance_ratio[i])
    eigenvalues['cumulative'].append(explained_variance_ratio_cumulative[i])

data_df = pd.DataFrame(eigenvalues, columns=eigenvalues.keys())
data_df.to_excel(writer, 'Eigenvalues', float_format='%.5f')
writer.save()