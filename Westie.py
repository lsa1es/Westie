#!/usr/bin/env python
# coding: utf-8

# Luiz Sales
# luiz@lsales.biz

import getpass
import nmap
import sys
import re
import paramiko
import netsnmp
#from snmp_helper import snmp_get_oid,snmp_extract



# SNMP version device
#COMMUNITY_STRING = 'public'
#SNMP_PORT = 161
#snmp_device = ('8.8.8.8', COMMUNITY_STRING, SNMP_PORT) 
#snmp_data = snmp_get_oid(a_device, oid='.1.3.6.1.2.1.1.1.0', display_errors=True)
#output = snmp_extract(snmp_data)
#print output


network  = sys.argv[1]

nm = nmap.PortScanner()
nm.scan(hosts= network, arguments='-sTU -p 22-161 ')
for host in nm.all_hosts():
	hst = host
	for proto in nm[host].all_protocols():
		prdslst = []
		extralst= []
		for prts in nm[host][proto].keys():
#			print "%s  -  %s  -  %s" % (hst,proto,prts)
			extralst.append(nm[host][proto][prts]['extrainfo'])
#			print "%s %s " % (extralst,prts)
			if prts == 22 and any("FreeBSD" in s for s in extralst):
				SO = 'Appliance'
				#sys.stdout.write("%s is %s " % (hst,SO))
				print ""
				print "%s is %s " % (hst,SO)
                        if (proto == 'udp') and (prts == 161):
				SO = 'Network Device'
                                #sys.stdout.write("%s is Netvork device" % (hst))
				print ""
				print "%s is %s" % (hst,SO)
				oid = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.2.1.1.1.0'))
				res = netsnmp.snmpwalk(oid, Version = 2, DestHost=hst, Community='public')
				print res	
			elif prts == 22:
				SO = 'Linux'
				print ""
				print "%s is %s" % (hst,SO)
				try:
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        				ssh.connect(hst, username=user, password=pass, timeout=10)
					stdin,stdout,stderr = ssh.exec_command("uname -a")
        	                        type(stdin)
					print stdout.readlines()
					ssh.close()
				except paramiko.SSHException:
        				print "Connection Failed"
        				ssh.close()
				except paramiko.AuthenticationException:
    					print "Authentication Failed"
					ssh.close()
				except:
    					print "Unknown error"
					ssh.close()

			prds = nm[host][proto][prts]['product']
			prdslst.append(prds)
			if any("Microsoft" in s for s in prdslst):
				SO = 'Windows'
				#sys.atdout.write("%s is Windows" % (hst))
				print ""
				print "%s is %s" % (hst,SO)
						


