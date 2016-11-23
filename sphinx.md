# SPhinx/coreseek安装步骤

- 下载coreseek软件包并解压

`tar -zxvf coreseek-4.1-beta.tar.gz`
- 安装依赖软件
`yum install make gcc g++ gcc-c++ libtool autoconf automake imake libxml2-devel expat-devel`

- 进入coreseekmmseg-3.2.14目录，执行

```
./bootstrap
./configure --prefix=/usr/local/mmseg3
make && make install
```

- 测试分词效果

```
./mmseg -d /usr/local/mmseg3/etc /usr/local/src/coreseek-4.1-beta/mmseg-3.2.14/src/t1.txt
```

- 安装coreseek，回到coreseek-4.1-beta目录，进入csft-4.1

```
sh buildconf.sh

./configure --prefix=/usr/local/coreseek --without-python --without-unixodbc --with-mmseg --with-mmseg-includes=/usr/local/mmseg3/include/mmseg/ --with-mmseg-libs=/usr/local/mmseg3/lib/ --with-mysql
```

如果出现undefined reference to `libiconv`

	首先configure，然后vim src/Makefile
	在其中搜索lexpat，在其后加上 -liconv
	修改后该行应该为：-lexpat -liconv -L/usr/local/lib
	然后再次make && make install

- 配置测试

`/usr/local/coreseek/bin/indexer -c /usr/local/coreseek/etc/sphinx-min.conf.dist`
返回`ERROR: nothing to do.`说明安装成功

- 开机自动运行

新建sh文件
`#!/bin/sh
/usr/local/coreseek/bin/searchd -c /usr/local/coreseek/etc/csft_mysql.conf
chmod +x csft.sh
vi /etc/rc.local
加入 ~/csft.sh
`


http://www.cnblogs.com/kudosharry/articles/3725683.html

## 使用方法

### 启动服务
`/usr/local/coreseek/bin/searchd -c /usr/local/coreseek/etc/csft_mysql.conf`

### 重建索引
`/usr/local/coreseek/bin/indexer -c /usr/local/coreseek/etc/csft_mysql.conf --all --rotate`

### 搜索分词
`/usr/local/coreseek/bin/search -c /usr/local/coreseek/etc/csft_mysql.conf apple`