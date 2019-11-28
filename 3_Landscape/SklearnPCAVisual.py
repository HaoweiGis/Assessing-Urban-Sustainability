'''
@Author: Muhaowei
@Date: 2019-10-03 01:18:43
@LastEditors: Muhaowei
@LastEditTime: 2019-10-20 20:48:07
@Description: 
'''
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
sns.set()

# fileNew = open('PacResult1.csv', 'w')
RSdata = np.array(pd.read_csv('PacResult1Select.csv'))
# print(RSdata)

km = KMeans(
    n_clusters=5, init='k-means++', max_iter=500, n_init=3, random_state=0)
print(RSdata[:, 2:])
km.fit(RSdata[:, 2:])
kmResult = km.labels_

# fileNew = open('goubi.csv', 'w')
# imgData = np.c_[RSdata[:, 0:], kmResult]
# print(imgData.shape)
# for line in imgData:
#     line = [str(i) for i in line]
#     lineNew = ','.join(line) + '\n'
#     fileNew.write(lineNew)

cmap = LinearSegmentedColormap.from_list(
    'own', ["#71EB30", "#216D9E", "#3DB868", "#007D65", "#FEFF80"])
plt.scatter(
    RSdata[:, 2],
    RSdata[:, 3],
    c=km.labels_,
    edgecolor='none',
    cmap=cmap,
    s=18
    # alpha=0.5,
)
plt.xlabel('component 1')
plt.ylabel('component 2')
# plt.colorbar()
plt.show()
