以识别城市棚户区为目的的实例分割网络架构思索

# 语义分割
## Unet-LSTM
https://github.com/mpapadomanolaki/UNetLSTM

CNN可以提供空间特征，LSTM可以提供时间特性，ConvLSTM可以同时利用时空特性
ConvLSTM核心本质还是和LSTM一样，不同的地方在于加上卷积操作后，不仅能够得到时序关系，还能够像卷积一样提取特征

## PSPNet
在全局均值池化（globe average pooling）的基础上空间金字塔池化，金字塔场景解析，但是会失去像素级别的位置信息，*是否可以参考HRnet加入一层1\*1卷积*，或者采用FPA（Feature Pyramid Attention）根据高层的特征来得到pixel-level的
attention来帮助低层的特征，从而增加感受野以及更好地分类小物体。


## DeeplabV3+
空洞卷积，（扩张率）依赖网络结构设计，对网络的输入尺寸也是有限制
空洞空间金字塔池化（ASPP），挖掘不同尺度的卷积特征，以编码 *如何以卷积的方式进行池化*
深度可分离卷积；
DeepLabv3+, extends DeepLabv3 by adding a simple yet eﬀective decoder module to reﬁne the segmentation results especially along object boundaries. We further ex-plore the Xception model and apply the depthwise separable convolution to both Atrous Spatial Pyramid Pooling and decoder modules, resulting
in a faster and stronger encoder-decoder network. 


## ENCnet
遥感更多的是一种纹理上面的特点，同时上下文语义之间的关系十分重要，从纹理上下文的角度出发也许能找到*Remote Sensing With deeplearning methon*。
捕获纹理信息等同于增加感受野？：PSPNet,DeepLab-v3

https://zhuanlan.zhihu.com/p/54949729
https://hangzhang.org//files/Deep-TEN-CVPR17.pdf 纹理和上下文的挖掘
https://hangzhang.org/PyTorch-Encoding/experiments/cifar.html


# 实例分割
## two stage
Mask R-CNN：Fast R-CNN(FPN)基础上面添加了mask分支

FPN:Multi-level Prediction with FPN多尺度预测

## one stage
FCOS：Fully Convolutional One-Stage Object Detection
PolarMask CenterNess找射线，设计了Polar Loss;

### 密集实例分割模型早期主要有两种，top-down apporach和bottom-up apporach
top-down apporach:先通过一些方法获取box区域，然后对区域内的像素进行mask提取
问题：1特征和mask之间的局部一致性会丢失；2冗余的特征提取，不同bbox会重新提取一侧mask；3由于使用了缩小特征图的卷积，位置信息会损失；
bottom-up apporach:逐像素预测，么个像素生成特征向量，然后通过一些方法对像素进行分组。
问题：1严重依赖逐像素预测的质量，容易导致非最优的分割；2由于mask在

## Attention:

