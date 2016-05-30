PID=`ps -ef | grep python | grep -v "grep" | awk '{print $2}'`
for pid in $PID
do
kill -9 $pid
echo "killed $pid"
done
echo "Kill all spider process"
exit 1