#!/usr/bin/python

import sys
import netaddr
import ciscotelnet

def main():
  
  try:
    ip_range_start = sys.argv[1]
  except IndexError:
    print "usage: %s <START IP> [<STOP IP>]"%(sys.argv[0])
    sys.exit(1)

  try:  
    ip_range_stop = sys.argv[2]
  except IndexError:
    ip_range_stop = ip_range_start

  for ip in netaddr.iter_iprange(ip_range_start, ip_range_stop, step=1):
    host = str(ip)
    #
    # Create cisco object. Using "verbose = True" will echo all receiving data to STDOUT. Use "with" statement for autologout and proper socket closure.
    #
    with ciscotelnet.CiscoTelnet(host, verbose = False) as cisco:
      #
      # Specify "user", "user_pass" or "line_pass" for auto logging, or use default "interactive=True" for keyboard inputs.
      # Specify "final_mode=ciscotelnet.MODE_EXEC" for staying in user exec mode or rely on default "MODE_ENABLE" and specify "enable_password" (or use keyboard inputs again) 
      #
      # if cisco.login(final_mode=CiscoTelnet.MODE_ENABLE, user="john", user_pass="12345678", enable_pass="cisco"):
      # if cisco.login(final_mode=CiscoTelnet.MODE_ENABLE, line_pass="abcdef", enable_pass="cisco"):
      if cisco.login(final_mode=ciscotelnet.MODE_ENABLE):
        print cisco.cmd("sh int status | inc Fa0/1") # execute any command on cisco device
        print cisco.conf(["interface fast0/1", "descr %s"%("-"*10), "load-interval 300"])  # IMPORTANT: do not use "conf t" and/or "end" cli commands here
        print cisco.wr() # saving
        print cisco.cmd("sh int status | inc Fa0/1")
      # That's all. Pretty simple and handy for network automation scripts.
    print "="*20

if __name__ == "__main__":
  if not sys.version_info[0] == 2:
    sys.exit(1)
  main()

  