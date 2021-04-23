for ((i=1;i<=1000000; i++));
do
	TLS1_3="$(redis-cli -e hget $i TLS1_3)"
	rem=$(($i%500))
	if [ $rem -eq 0 ]; then
		sleep 5
	fi
	if [ ! -z "$TLS1_3" ]; then
		while true;
	
		do
	  
			process_count=$(ps aux|grep -c earlydata)
	  
			if [[ $process_count -le 30 ]];
	  
			then
		
				break
	  
			fi
	  
			sleep 1
	
		done
        
		python3.9 earlydata.py $i &
	fi
done
