# cisco-telnet
Handy remote access to Cisco devices via telnet

Quick Example:

<pre>
import ciscotelnet
with ciscotelnet.CiscoTelnet(host, verbose = False) as cisco:
  #
  # Specify "user", "user_pass" or "line_pass" for auto logging, or use default "interactive=True" for keyboard inputs.
  # Specify "final_mode=ciscotelnet.MODE_EXEC" for staying in user exec mode or rely on default "MODE_ENABLE" and specify "enable_password" (or use keyboard inputs again) 
  # i.e.:
  #
  # if cisco.login(final_mode=CiscoTelnet.MODE_EXEC, user="peter", user_pass="secret"):
  # or
  # if cisco.login(final_mode=CiscoTelnet.MODE_ENABLE, user="john", user_pass="12345678", enable_pass="cisco"):
  # or
  # if cisco.login(final_mode=CiscoTelnet.MODE_ENABLE, line_pass="abcdef", enable_pass="cisco"):
  # or
  if cisco.login(final_mode=ciscotelnet.MODE_ENABLE):  # keyboard interactive
    print cisco.cmd("sh int status | inc Fa0/1") # execute any command on cisco device
    print cisco.conf(["interface fast0/1", "descr blank", "load-interval 300"])  # IMPORTANT: do not use "conf t" and/or "end" cli commands here
    print cisco.wr() # saving
    print cisco.cmd("sh int status | inc Fa0/1")
</pre>
