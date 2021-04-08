for ((i=1;i<=1000000; i++));
do
	status="$(redis-cli -e hget $i STATUS)"
	if [[ $status != "1" ]]; then
		while true;
	
		do
	  
			process_count=$(ps aux|grep -c error_retry)
	  
			if [[ $process_count -le 30 ]];
	  
			then
		
				break
	  
			fi
	  
			sleep 1
	
		done
        
		python3.9 error_retry.py $i &
	fi
done
