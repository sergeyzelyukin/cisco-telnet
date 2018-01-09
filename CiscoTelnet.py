#!/usr/bin/python

import sys, os, re, getpass
from telnetlib import Telnet

MODE_INIT        = "INIT"
MODE_CONNECTED   = "CONNECTED"
MODE_USER        = "USER"
MODE_USER_PASS   = "USER PASS"
MODE_LINE_PASS   = "LINE PASS"
MODE_EXEC        = "EXEC"
MODE_ENABLE_PASS = "ENABLE PASS"
MODE_ENABLE      = "ENABLE"

WAIT_TIMEOUT     = 3
WR_WAIT_TIMEOUT  = 10


class CiscoTelnet(Telnet):
  def __init__(self, host, verbose = False):
    self._host = host
    self._verbose = verbose
    self._mode = MODE_INIT

    Telnet.__init__(self, host)

    self._mode = MODE_CONNECTED

  def __enter__(self):
    return self

  def __exit__(self, *args):
    if self._mode == MODE_EXEC or self._mode == MODE_ENABLE:
      self.logout()
    self.close()

  def login(self, interactive = True, final_mode = MODE_ENABLE, user = None, user_pass = None, line_pass = None, enable_pass = None, max_steps = 10):
    if not self._mode == MODE_CONNECTED:
      return False

    step = 0
    while True:
      step += 1
      if step>max_steps:
        return False

      username_pattern = re.compile("username:", re.IGNORECASE)
      password_pattern = re.compile("password:", re.IGNORECASE)
      exec_pattern = re.compile(">$", re.IGNORECASE)
      enable_pattern = re.compile("#$", re.IGNORECASE)

      answer = self.expect([username_pattern, password_pattern, exec_pattern, enable_pattern], WAIT_TIMEOUT)
      if self._verbose: 
        print answer[2]

      if not answer[1]:
        return False

      if answer[0] == 0:
        self._mode = MODE_USER

        if user:
          username = user
        else:
          if not interactive:
            return False
          username = raw_input("[%s] username: "%(self._host))

        self.write("{0}\n".format(username))
      elif answer[0] == 1:
        if self._mode == MODE_CONNECTED:
          self._mode = MODE_LINE_PASS
        elif self._mode == MODE_USER:
          self._mode = MODE_USER_PASS
        elif self._mode == MODE_EXEC:
          self._mode = MODE_ENABLE_PASS
        else:
          pass

        if self._mode == MODE_USER_PASS:
          if user_pass:
            password = user_pass
          else:
            if not interactive:
              return False
            password = getpass.getpass(prompt="[%s] %s's password: "%(self._host, username))
        elif self._mode == MODE_LINE_PASS:
          if line_pass:
            password = line_pass
          else:
            if not interactive:
              return False
            password = getpass.getpass(prompt="[%s] line password: "%(self._host))
        elif self._mode == MODE_ENABLE_PASS:
          if enable_pass:
            password = enable_pass
          else:
            if not interactive:
              return False
            password = getpass.getpass(prompt="[%s] enable password: "%(self._host))
  
        self.write("{0}\n".format(password))
      elif answer[0] == 2:
        self._mode = MODE_EXEC

        if self._mode == final_mode:
          self._stop_pattern = exec_pattern
          self.write("terminal length 0\n")
          self.expect([self._stop_pattern], WAIT_TIMEOUT)
          return True
        self.write("en\n")
      elif answer[0] == 3:
        self._mode = MODE_ENABLE

        if self._mode == final_mode:
          self._stop_pattern = enable_pattern
          self.write("terminal length 0\n")
          self.expect([self._stop_pattern], WAIT_TIMEOUT)
          return True

  def logout(self):
    self.write("\x1A")
    self.write("logout\n")

  def cmd(self, command):
    self.read_lazy()

    self.write(command+"\n")
    answer = self.expect([self._stop_pattern], WAIT_TIMEOUT)

    if not answer[1]:
      return None
    else:
      if self._verbose:
        print answer[2]
      
      return answer[2]

  def conf(self, config_lines):
    self.read_lazy()

    read_buffer = ""
    conf_pattern = re.compile("\)#$", re.IGNORECASE)

    for line in ["conf t\n"]+config_lines+["end"]:
      self.write(line+"\n")
      answer = self.expect([conf_pattern], WAIT_TIMEOUT)
      if answer[1]:
        read_buffer += answer[2]     

    answer = self.expect([self._stop_pattern], WAIT_TIMEOUT)
    if answer[1]:
      read_buffer += answer[2]

    if self._verbose:
      print read_buffer

    return read_buffer


  def wr(self):
    self.read_lazy()

    self.write("wr\n")
    answer = self.expect([self._stop_pattern], WR_WAIT_TIMEOUT)

    if not answer[1]:
      return None
    else:
      if self._verbose:
        print answer[2]
      
      return answer[2]


