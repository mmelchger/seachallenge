#!/bin/ksh
file="/home/m/aislog_20190302.txt"
while IFS= read line
do
        # display $line or do somthing with $line
	echo "$line"
	#echo "$line" | netcat localhost 10999
	nc -b -u localhost 10999 | "$line"
	#echo "$line" > nc -b -u localhost 10999
	#echo -n '!AIVDM,1,1,,A,33u7M`001SPfc3jO7ig`1VTB0000,0*40' | nc -b -u localhost 10999
	sleep 0.1s
done <"$file"
