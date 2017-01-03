
##基础软件安装

#####Debian系统中，安装软件：
```bash
$ sudo apt-get update
$ sudo apt-get install -y \
    default-jre \
    jq \
    python-dev \
    python-pip \
    python-virtualenv \
    redis-server \
    zip \
    zookeeperd
```
确认已自动启动redis和zookeeperd。
  
#####安装一个公认的稳定版kafka：

```
$ cd /tmp
$ curl -O http://mirrors.hust.edu.cn/apache/kafka/0.8.2.1/kafka_2.11-0.8.2.1.tgz
$ tar -xzf kafka_2.11-0.8.2.1.tgz
$ cd kafka_2.11-0.8.2.1/
$ nohup bin/kafka-server-start.sh \
    config/server.properties \
    > ~/kafka.log 2>&1 &
$ export PATH="`pwd`/bin:$PATH"
```
在高版本的（>=1.9）的jre环境，启动参数异常会导致java启动失败，此时最简单的方法是使用1.8版本的jre：

```
$ update-alternatives --display java
$ update-alternatives --config java
$ java -version

```

启动2个topic，分别用于数据采集和状态监控：
```bash
$ kafka-topics.sh \
    --zookeeper 127.0.0.1:2181 \
    --create \
    --partitions 1 \
    --replication-factor 1 \
    --topic results
  
$ kafka-topics.sh \
    --zookeeper 127.0.0.1:2181 \
    --create \
    --partitions 1 \
    --replication-factor 1 \
    --topic metrics
```

##应用软件部署：

#####python环境

使用virtualenv来构建python环境
```bash
$ virtualenv .ips
$ source .ips/bin/activate
$ pip install -r requirements.txt requirements-dev.txt
```

##测试数据说明：
我们使用免费域名列表数据来进行测试。  

最早提供1百万域名列表服务的是alexa，曾经停止过文件下载，后来又恢复，只是排名不是最新：
http://s3.amazonaws.com/alexa-static/top-1m.csv.zip

statvoo提供的1百万域名列表：  
https://statvoo.com/dl/top-1million-sites.csv.zip 

opendns提供的1百万域名列表：
http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip

