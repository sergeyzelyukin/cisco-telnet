#!/usr/bin/python

import sys
import netaddr
import CiscoTelnet

def main():
  
  try:
    ip_range_start = sys.argv[1]
    ip_range_stop = sys.argv[2]
  except IndexError:
    print "usage: %s <IP-RANGE START> <IP-RANGE STOP>"%(sys.argv[0])
    sys.exit(1)
  

  for ip in netaddr.iter_iprange(ip_range_start, ip_range_stop, step=1):
    host = str(ip)
    with CiscoTelnet.CiscoTelnet(host, verbose = False) as cisco:
      #if cisco.login(final_mode=CiscoTelnet.MODE_ENABLE, user="john", user_pass="12345678", enable_pass="cisco"):
      #if cisco.login(final_mode=CiscoTelnet.MODE_ENABLE, line_pass="abcdef", enable_pass="cisco"):
      if cisco.login(final_mode=CiscoTelnet.MODE_ENABLE):
        print cisco.cmd("sh int status | inc Fa0/1")
        print cisco.conf(["interface fast0/1", "descr %s"%("-"*10), "load-interval 300"])
        print cisco.wr()
        print cisco.cmd("sh int status | inc Fa0/1")
    print "="*20

if __name__ == "__main__":
  if not sys.version_info[0] == 2:
    sys.exit(1)
  main()

  