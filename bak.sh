#!/bin/bash

Backup_Home="/backup/" #备份目录
Backup_Dir=("/var/www/zdtshop/bullet") #网站目录
MYSQL_Dump="/usr/bin/mysqldump" #mysqldump目录位置
MYSQL_UserName="root" #数据库用户名
MYSQL_PassWord="4198261MOzhihang"	#数据库密码
Backup_Database=("information" "punishment") #要备份的数据库

#################################### Script start #############################
#mysqldump -uroot -p4198261MOzhihang --events -A > /root/databasebackup$(date +"%Y%m%d").sql #备份所有数据库
#tar zcf ${Backup_Home}www-$(date +"%Y%m%d").tar.gz -C /var/www/zdtshop/ ${Backup_Dir1} --exclude=${Exclude}

OldWWWBackup=www-*-$(date -d -3day +"%Y%m%d").tar.gz
OldDBBackup=db-*-$(date -d -7day +"%Y%m%d").sql

Backup_Dir(){
    Backup_Path=$1
    Dir_Name=`echo ${Backup_Path##*/}`
    Pre_Dir=`echo ${Backup_Path}|sed 's/'${Dir_Name}'//g'`
    tar zcf ${Backup_Home}www-${Dir_Name}-$(date +"%Y%m%d").tar.gz -C ${Pre_Dir} ${Dir_Name}
}


Backup_Sql(){
	${MYSQL_Dump} -u$MYSQL_UserName -p$MYSQL_PassWord --events $1 > ${Backup_Home}db-$1-$(date +"%Y%m%d").sql
}

if [ ! -f ${MySQL_Dump} ]; then  
    echo "mysqldump command not found.please check your setting."
    exit 1
fi

if [ ! -d ${Backup_Home} ]; then  
    mkdir -p ${Backup_Home}
fi

for dd in ${Backup_Dir[@]};do
    Backup_Dir ${dd}
done

for db in ${Backup_Database[@]};do
    Backup_Sql ${db}
done

rm -f ${Backup_Home}${OldWWWBackup}
rm -f ${Backup_Home}${OldDBBackup}