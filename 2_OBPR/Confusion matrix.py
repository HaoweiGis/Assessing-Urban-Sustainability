'''
@Author: Muhaowei
@Date: 2019-09-24 11:28:06
@LastEditors: Muhaowei
@LastEditTime: 2019-10-06 17:15:30
@Description: 
'''
# -*-coding:utf-8-*-
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#labels表示你不同类别的代号，比如这里的demo中有13个类别
labels = ['SB', 'CCSH', 'V', 'I', 'T', 'BL', 'LC', 'W']


def plot_confusion_matrix(cm, title='Confusion Matrix', cmap=plt.cm.binary):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, fontsize=16, family='Times New Roman')
    plt.colorbar()
    xlocations = np.array(range(len(labels)))
    # plt.xticks(xlocations, labels, rotation=90)
    plt.xticks(xlocations, labels, fontsize=16, family='Times New Roman')
    plt.yticks(xlocations, labels, fontsize=16, family='Times New Roman')
    plt.ylabel('True label', fontsize=16, family='Times New Roman')
    plt.xlabel('Predicted label', fontsize=16, family='Times New Roman')


# name = 'Accuracy/PtestAccuracy.csv'
# name = 'Accuracy/PtestAccuracy_SVM.csv'
# name = 'Accuracy/ObjectAccuracy_SVM.csv'
name = 'Accuracy/ObjectAccuracy.csv'

df = pd.read_csv(name, header=None)
# print(np.array(df))
cm = np.array(df)
tick_marks = np.array(range(len(labels))) + 0.5
np.set_printoptions(precision=2)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
print(cm_normalized)
plt.figure(figsize=(12, 8), dpi=800)

ind_array = np.arange(len(labels))
x, y = np.meshgrid(ind_array, ind_array)

for x_val, y_val in zip(x.flatten(), y.flatten()):
    c = cm_normalized[y_val][x_val]
    if c > 0.01:
        plt.text(
            x_val,
            y_val,
            "%0.2f" % (c, ),
            color='red',
            fontsize=16,
            va='center',
            ha='center',
            family='Times New Roman')
# offset the tick
plt.gca().set_xticks(tick_marks, minor=True)
plt.gca().set_yticks(tick_marks, minor=True)
plt.gca().xaxis.set_ticks_position('none')
plt.gca().yaxis.set_ticks_position('none')
plt.grid(True, which='minor', linestyle='-')
plt.gcf().subplots_adjust(bottom=0.15)
plot_confusion_matrix(cm_normalized, title='Normalized confusion matrix')
# show confusion matrix
plt.savefig(name.split('.')[0] + 'confusion_matrix.jpg', format='jpg', dpi=800)
# plt.show()
