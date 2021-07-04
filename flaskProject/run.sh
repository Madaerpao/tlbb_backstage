#!/bin/bash
#Author : Ataier QQ3284809656
#安装Docker
cd /root/flaskProject

function docker_install()
{
	echo "检查Docker......"
	docker -v
    if [ $? -eq  0 ]; then
        echo "检查到Docker已安装!"
    else
    	echo "安装docker环境..."
        curl -sSL https://get.daocloud.io/docker | sh
        echo "安装docker环境...安装完成!"
    fi
    # 创建公用网络==bridge模式
    #docker network create share_network
}

#Docker Build And Run
function docker_run()
{
	docker build -t "tlbb_backstage" .
	docker run -d -p 8881:8881 --name "tl_backstage" "tlbb_backstage"
	echo " HTTP://你的IP:8881 即可访问！！！"
}
# 执行函数
docker_install
sudo systemctl start docker
cd /root/flaskProject
docker_run
