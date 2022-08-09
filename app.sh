if [ "$1" == "start" ]; then
    nohup python3 run.py > autotest.log  2>&1  &
    echo "Application is starting."
else if [ "$1" == "stop" ]; then
    PID=$(ps -ef | grep run.py | grep -v grep | awk '{ print $1 }')
    if [ -z "$PID" ]; then
        echo Application is already stopped
    else
        echo kill $PID
        kill $PID
    fi
else if [ "$1" == "status" ]; then
    PID=$(ps -ef | grep run.py | grep -v grep | awk '{ print $1 }')
    if [ -z "$PID" ]; then
        echo Application is stopped
    else
        echo Application is running
        echo $PID
    fi
fi
fi
fi
