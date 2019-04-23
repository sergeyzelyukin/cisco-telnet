#!/usr/bin/python

from setuptools import setup

setup( name='ciscotelnet',
  version='0.1.4',
  description='handy remote access to Cisco devices via telnet',
  maintainer_email='sergey.zelyukin@gmail.com',
  keywords='cisco telnet',
  license='Apache License, Version 2.0',
  classifiers=[
  'Programming Language :: Python',
  'Programming Language :: Python :: 2',
  'Programming Language :: Python :: 2.7',
  'Topic :: System :: Networking',
  'Topic :: Software Development :: Libraries',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: Apache Software License',
  'Development Status :: 4 - Beta'],
  py_modules=['ciscotelnet'])
