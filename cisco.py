#!/usr/bin/python

import sys, os, re, getpass
import CiscoTelnet

def main():
#  for ip in ["10.116.1.1", "10.100.140.254", "10.100.1.9"]:
  for ip in ["10.116.1.1"]:
    with CiscoTelnet.CiscoTelnet(ip, verbose = True) as cisco:
      cisco.set_debuglevel(0)
      if cisco.login(final_mode=CiscoTelnet.MODE_ENABLE):
        cisco.cmd("sh int status")
        cisco.conf(["interface fast0/1", "descr ----"])
        #cisco.wr()
        cisco.cmd("sh int status")
        #print cisco.cmd("sh version | inc uptime")
    print "="*10

if __name__ == "__main__":
  if not sys.version_info[0] == 2:
    sys.exit(1)
  main()

  