#!/bin/bash
#MySQL install
check_system()
{
#check system version
system=`cat /etc/issue | awk '{print $1}'`
if [ $system = "Ubuntu" ];then
return 0
else
return 1
fi
}
check_installOrNot()
{
#check mysql install or not
netstat -tap | grep mysql
if [ $? = 0 ];then
    return 0
else
    return 1
fi
}
main()
{
echo "#***********************************#"
echo "# 欢迎使用mysql集群安装脚本 #"
echo "# Copyright 2016 by LiQing #"
echo "#***********************************#"
sleep 1
check_system
if [ $? = 0 ];then
    echo "System is Ubuntu"
    check_installOrNot
    if [ $? = 0 ];then
        echo "MySql has installed"
    else
        echo "Now install mysql-server"
        sudo apt-get install mysql-server
        if [ $? = 0 ];then
            echo "Now install mysql-client"
            apt-get isntall mysql-client
            if [ $? = 0 ];then
                echo "Now install libmysqlclient-dev"
                sudo apt-get install libmysqlclient-dev
                if [ $? = 0 ];then
                    echo "Install MySQL is success"
                    sudo service mysql restart
                fi
            fi
        fi
    fi
else
    echo "System is not support"
fi
exit 0
}
main
