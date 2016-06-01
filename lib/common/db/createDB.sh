#!/bin/bash
#MySQL install
check_system()
{
#check system version

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
create_user()
{
#create user of root permissions

}