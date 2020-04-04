## docker hub地址
<!-- https://hub.docker.com/ -->

docker pull 
docker run




## docker 删除container image
docker  ps  -a
docker  rm containerID
docker stop $(docker  ps  -a -q)
docker images
docker rmi imageID


docker run -it  --rm --name 'deyu-ai-v1' -u 1001 -v /home/deyu/tianchi_buildings:/data  --gpus all pytorch/pytorch:1.4-cuda10.1-cudnn7-devel