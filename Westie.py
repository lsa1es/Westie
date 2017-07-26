#!/usr/bin/env python
# coding: utf-8

# Luiz Sales
# luiz@lsales.biz

import os
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

def ws_snmp(self):
	oid = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.2.1.1.1.0'))
	res = netsnmp.snmpwalk(oid, Version = 2, DestHost=hst, Community='public')
	print res



def ws_linux():
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hst, username='user', password='pass', timeout=10)
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

def ws_windows():
	conn = SMBConnection("user user", pass, myname, hst, use_ntlm_v2 = True)
	conn.connect(hst, port=139)
	file2transfer = open(filename,"r")
	conn.storeFile(share,path + filename, file2transfer, timeout=30 )

nm = nmap.PortScanner()
nm.scan(hosts= network, arguments='-sTUV -p1-500 ')
print nm.all_hosts()
for hst in nm.all_hosts():
	print "1o for %s %s" % (hst,nm.all_hosts())
	for proto in nm[hst].all_protocols():
		print "2o for %s %s %s" % (hst,proto,nm[hst].all_protocols())
		prdslst = []
		extralst= []
		for prts in nm[hst][proto].keys():
			print "3o for %s %s %s %s " % (hst,proto,prts,nm[hst][proto].keys())
			extralst.append(nm[hst][proto][prts]['extrainfo'])
#			print "%s %s " % (extralst,prts)
			state = nm[hst][proto][prts]['state']
			if (prts == 22) and (proto == 'tcp') and (state == 'open') and any("FreeBSD" in s for s in extralst):
				SO = 'Appliance'
				print ""
				print "%s is %s " % (hst,SO)
                        if (proto == 'udp') and (prts == 161) and (state == 'open'):
				SO = 'Network Device'
                                #sys.stdout.write("%s is Netvork device" % (hst))
				print ""
				#ws_snmp
				print "%s is %s" % (hst,SO)
			elif (prts == 22) and (proto == 'tcp') and (state == 'tcp'):
				SO = 'Linux'
				print ""
				print "%s is %s" % (hst,SO)
				#ws_linux()
			prds = nm[hst][proto][prts]['product']
			prdslst.append(prds)
			if (prts == 139) or (prts == 445) and (proto == 'tcp') and (state == 'open'):
			#if any("Microsoft" in s for s in prdslst) or (prts == 139) or (prts == 445):
				SO = 'Windows'
				print ""
				print "%s is %s" % (hst,SO)
			#	ws_windows()
			#	os.system("psexec.py \"user\":pass@" + hst + " whoami ")
			#	os.system("sudo mount -t cifs -o username=\"user\",password=pass //" + hst + "/c$ winc/ ")
			#	os.system("echo \"funcionou\" > winc/WestieOK.txt ") 
			#	os.system("sudo umount winc/ ")



