
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
在coserver端的服务器上安装即可

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
$ virtualenv .whois
$ source .whois/bin/activate
$ pip install -r requirements.txt
```

  
在coserver服务器上，运行如下命令


以下命令生成数据库相关内容
```
$ python manage.py migrate
```

按照下文中测试数据的获取方式，得到一个top-1m.csv文件，使用
```
$ python manage.py import_top1m top-1m.csv
```
可以将需要进行whois查询的数据导入到server端的数据库

启动coserver上的http服务，用于work获取域名信息：

```
$ python manage.py runserver 0.0.0.0:8000
```


在work服务器上，进入代码目录，执行
```
$ python manage.py set_coserver_ip ***.*.*.***
```
设定coserver服务器使用的ip

执行
```
$ python manage.py get_names_whois
```
开始获取域名并执行业务功能。

在coserver服务器上，进入代码目录，执行
```
$ python manage.py set_coserver_ip 127.0.0.1
```
设定coserver服务器使用的ip（本机）

执行
```
$ python manage.py collect_whois_kafka
```
此时程序从kafka中获取数据并将结果保存到数据库中。（缺省sqlte3）

##测试数据说明：
我们使用免费域名列表数据来进行测试。  

最早提供1百万域名列表服务的是alexa，曾经停止过文件下载，后来又恢复，只是排名不是最新：
http://s3.amazonaws.com/alexa-static/top-1m.csv.zip

statvoo提供的1百万域名列表：  
https://statvoo.com/dl/top-1million-sites.csv.zip 

opendns提供的1百万域名列表：
http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip

##测试辅助命令
查看kafka的队列内容：
```apple js
kafka-console-consumer.sh --zookeeper 127.0.0.1:2181 --topic results --from-beginning
```

##ToDo
1. 针对运维的说明需要补充，如在aws上的部署方法。
2. 数据结果的格式，数据内容中的字符集，域名格式的转换，数据结果检查和重新查询... 需要进一步细化和完善
3. 数据库调整为mysql
4. 客户端使用pythonwhois，效率不高，应对所有TLD对应的whois server分别设定超时时间，不要每条查询都休眠5秒，此处需要有自己的whois实现。
5. 更多异常控制。