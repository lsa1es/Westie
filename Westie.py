#!/usr/bin/env python
# coding: utf-8

# Luiz Sales
# luiz@lsales.biz

import nmap
import sys
import re
from pexpect import pxssh
#from snmp_helper import snmp_get_oid,snmp_extract



# SNMP version device
#COMMUNITY_STRING = 'public'
#SNMP_PORT = 161
#snmp_device = ('8.8.8.8', COMMUNITY_STRING, SNMP_PORT) 
#snmp_data = snmp_get_oid(a_device, oid='.1.3.6.1.2.1.1.1.0', display_errors=True)
#output = snmp_extract(snmp_data)
#print output


nm = nmap.PortScanner()

network  = sys.argv[1]
nm.scan(hosts= network, arguments='-sTU -p 1-200 ')
for host in nm.all_hosts():
	hst = host
	lst = []
	for proto in nm[host].all_protocols():
		extralst= []
		for prts in nm[host][proto].keys():
			print "%s  -  %s  -  %s" % (hst,proto,prts)
			extralst.append(nm[host][proto][prts]['extrainfo'])
			print "%s %s " % (extralst,prts)
			if prts == 22 and any("FreeBSD" in s for s in extralst):
				print "%s if Appliance " % (hst)
                        if (proto == 'udp') and (prts == 161 or prts == 162):
                                print "%s is Netvork device" % (hst)
			elif prts == 22:
                                print "%s is Linux" % (hst)
			prds = nm[host][proto][prts]['product']
			lst.append(prds)
		if any("Microsoft" in s for s in lst):
			print "%s is Windows" % (hst)
			
		


