for ((i=1;i<=1000000; i++));
do
	while true;
	do
	  process_count=$(ps aux|grep -c singlethread)
	  if [[ $process_count -le 100 ]];
	  then
		break
	  fi
	  sleep 1
	done
        python3.9 singlethread.py $i &
done
