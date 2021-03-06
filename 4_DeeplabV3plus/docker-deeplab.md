# 安装docker
以及nvidia-docker toolkits

# 修改docker国内源
在阿里云开放云原生平台找到对应系统
您可以通过修改daemon配置文件/etc/docker/daemon.json来使用加速器
```
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://gcz02461.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

# 拉取tf 1.14 GPU版本的docker官方镜像
`deyu@AIStation:/home/hncg$ sudo docker pull tensorflow/tensorflow:1.14.0-gpu-py3-jupyter`

# 创建镜像

WARNING: You are running this container as root, which can cause new files in
mounted volumes to be created as the root user on your host machine.

To avoid this, run the container by specifying your user's userid:

`$ docker run -u $(id -u):$(id -g) args...`


`sudo docker run -it  --rm --name 'deeplab' -u 1001 -v /home/deyu/tianchi_buildings:/data  --gpus all tensorflow/tensorflow:1.14.0-gpu-py3-jupyter`

docker run -it --rm --name 'deep-ai-v1' --net host -v /volumes/massdata2/wxy:/data --shm-size 10g --gpus all pytorch/pytorch:1.5-cuda10.1-cudnn7-devel

https://github.com/docker/cli/issues/1278

docker start tf1.14
`sudo docker exec -it --user root tf1.14 /bin/bash`

# 测试GPU可用性
```
import tensorflow as tf
print('GPU',tf.test.is_gpu_available())
```

# 更新阿里apt镜像安装vim，gdal
cp /etc/apt/sources.list /etc/apt/sources.list.20200617
vim /etc/apt/sources.list
参考 https://www.jianshu.com/p/16502ed02e29

deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse

deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse


apt update
apt install vim
apt install gdal-bin python-gdal python3-gdal libgdal-dev

# 构建anaconda镜像源
vim ~/.condarc



# 构建anaconda虚拟环境
conda create -n deeplab
conda activate deeplab
conda install tensorflow-gpu==1.14
conda install gdal
conda install pillow

# 新样本的制作过程
将shp转换为栅格后裁剪
然后栅格计算器Con(IsNull("Subject01.tif"),0,"Subject01.tif")
python gdal_edit.py Subject01_building_footprints.tif -unsetnodata

# datasets数据更新
构建样本数据
/data/datasets/Image_process# bash 1clip_sampleimg.sh
for i in *;do echo $i; gdalinfo $i|grep ^Size|cut -d' ' -f3-4|sed -e 's/ //g'|cut -d',' -f1;done 数据检查

/data/datasets/allimage#  
python 2split_index.py 1168 80 (总数 验证数)数据切分代码 360 40
mv train.txt trainval.txt val.txt phindex/

vi /data/models-master/research/deeplab/datasets/data_generator.py 105 修改对应数据数量
vi /data/models-master/research/deeplab/deprecated/segmentation_dataset.py 116
vi train_utils.py  206 exclude_list = ['global_step','logits']

# 生成tfrecord数据集
python /data/models-master/research/deeplab/datasets/build_voc2012_data.py  --image_folder="/data/datasets/allimage"   --semantic_segmentation_folder="/data/datasets/alllabel"   --list_folder="/data/datasets/allindex"   --image_format="png"   --output_dir="/data/datasets/alltfrecord"


python /data/models-master/research/deeplab/datasets/build_voc2012_data.py  --image_folder="/data/datasets/rs2019/image"   --semantic_segmentation_folder="/data/datasets/rs2019/label"   --list_folder="/data/datasets/rs2019/index"   --image_format="png"   --output_dir="/data/datasets/rs2019/tfrecord"

# 模型训练

将deeplab及下面的slim包加入环境变量，但是这种方式会在下次打开时候失效：  
`export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim`

screen -L -t name -S name ./name      screen -r 回归 ctrl+a+d
第一个name是记录日志的名字，第二个name是screen -ls 列表展示出来的名字，第三个name是需要运行的程序。

/data/models-master/research/deeplab/exp
mkdir train vis eval

screen -L python /data/models-master/research/deeplab/train.py   --logtostderr   --num_clones=4   --training_number_of_steps=500   --train_split="train"   --model_variant="xception_71"   --atrous_rates=4   --atrous_rates=12   --atrous_rates=18   --output_stride=16   --decoder_output_stride=4   --train_crop_size="513,513"   --train_batch_size=12   --dataset="rs2019"   --initialize_last_layer=False   --last_layers_contain_logits_only=True   --fine_tune_batch_norm=True   --tf_initial_checkpoint='/data/models-master/research/deeplab/backbone/train_fine/model.ckpt'   --train_logdir='/data/datasets/rs2019/train/'   --dataset_dir='/data/datasets/rs2019/tfrecord'

screen -L python /data/models-master/research/deeplab/train.py   --logtostderr   --num_clones=4   --training_number_of_steps=5000   --train_split="train"   --model_variant="xception_71"   --atrous_rates=4   --atrous_rates=12   --atrous_rates=18   --output_stride=16   --decoder_output_stride=4   --train_crop_size="513,513"   --train_batch_size=12   --dataset="mydata"   --initialize_last_layer=False   --last_layers_contain_logits_only=True   --fine_tune_batch_norm=True   --tf_initial_checkpoint='/data/models-master/research/deeplab/backbone/train_fine/model.ckpt'   --train_logdir='/data/models-master/research/deeplab/exp/alldata_train/train/'   --dataset_dir='/data/datasets/alltfrecord'

python /data/models-master/research/deeplab/eval.py  --logtostderr --eval_split="val"     --model_variant="xception_71"     --atrous_rates=4    --atrous_rates=12    --atrous_rates=18    --output_stride=16    --decoder_output_stride=4    --eval_crop_size="513,513"     --dataset="rs2019"     --initialize_last_layer=False    --last_layers_contain_logits_only=True    --checkpoint_dir='/data/datasets/rs2019/train/'   --eval_logdir='/data/datasets/rs2019/eval/'     --dataset_dir='/data/datasets/rs2019/tfrecord'

python /data/models-master/research/deeplab/eval.py  --logtostderr --eval_split="val"     --model_variant="xception_71"     --atrous_rates=4    --atrous_rates=12    --atrous_rates=18    --output_stride=16    --decoder_output_stride=4    --eval_crop_size="513,513"     --dataset="mydata"     --initialize_last_layer=False    --last_layers_contain_logits_only=True    --checkpoint_dir='/data/models-master/research/deeplab/exp/alldata_train/train/'   --eval_logdir='/data/models-master/research/deeplab/exp/alldata_train/eval/'     --dataset_dir='/data/datasets/alltfrecord'

python /data/models-master/research/deeplab/vis.py     --logtostderr     --vis_split="val"     --model_variant="xception_71"     --atrous_rates=6     --atrous_rates=12     --atrous_rates=18     --output_stride=16     --decoder_output_stride=4     --vis_crop_size="513,513"     --dataset="rs2019"     --colormap_type="pascal"     --checkpoint_dir='/data/datasets/rs2019/train/'     --vis_logdir='/data/datasets/rs2019/vis/'    --dataset_dir='/data/datasets/rs2019/tfrecord'

python /data/models-master/research/deeplab/export_model.py  --logtostderr  --checkpoint_path="/data/models-master/research/deeplab/exp/alldata_train/train/model.ckpt-10000"   --atrous_rates=4  --atrous_rates=12  --atrous_rates=18  --output_stride=16  --decoder_output_stride=4  --export_path="/data/datasets/model/frozen_inference_graph.pb"    --model_variant="xception_71"  --num_classes=2   --crop_size=513  --crop_size=513  --initialize_last_layer=False  --last_layers_contain_logits_only=True  --fine_tune_batch_norm=True   --inference_scales=1.0

tar -zcvf model.tar.gz frozen_inference_graph.pb
tar -zxvf model.tar.gz