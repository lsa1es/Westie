#!/usr/bin/env python
# coding: utf-8

# Luiz Sales
# luiz@lsales.biz

import nmap
import sys

network = sys.argv[1]
nm = nmap.PortScanner()


nm.scan(hosts= network, arguments='-sTU -p 1-200 -sV ')
for host in nm.all_hosts():
        hst = host
        lst = []
        for proto in nm[host].all_protocols():
                for prts in nm[host][proto].keys():
                        print "%s  -  %s  -  %s" % (hst,proto,prts)
                        extrainfo = nm[host][proto][prts]['extrainfo']
                        print "%s %s " % (extrainfo,prts)
                        if prts == 22 and any("FreeBSD" in s for s in extrainfo):
                                print "%s if Appliance " % (hst)
                        if (proto == 'udp') and (prts == 161 or prts == 162):
                                print "%s is Netvork device" % (hst)
                        elif prts == 22:
                                print "%s is Linux" % (hst)
                        prds = nm[host][proto][prts]['product']
                        lst.append(prds)
                if any("Microsoft" in s for s in lst):
                        print "%s is Windows" % (hst)
