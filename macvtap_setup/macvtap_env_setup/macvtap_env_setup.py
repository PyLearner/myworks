# Draft

##################                           ##################
#                # eno4                 eno4 #                #
#      HOST      #---------------------------#     Gateway    #
#                #                           #                #
##################                           ##################


# Note:
# 1. Please Install the python package pexpect before your run.
# 2. The parameters is hardcoded and only applies to the 2 machines,if the port changes,you
#    should modify it before run.so please do check before running.

# How to run:
# 1.There are 2 files, macvtap_env_setup.py and gateway-iptables
# 2.Copy them to your dir and just run python macvtap_env_setup.py
# Todo: Can use argparser to receive some parameters.

# In Host,just configure The static Ip address for eno4,and then start the interface
# In Gateway:
# 1. Configure Ip address for eno4,and then start the interface
# 2. Configure Dhcp using libvirt dnsmasq,
# 3. Configure Iptables,then reload it.
# 4. Open the forward function


import pexpect
import sys
import time


host = "hp-dl385pg8-09.qe.lab.eng.nay.redhat.com"
gateway = "hp-dl385pg8-10.qe.lab.eng.nay.redhat.com"
host_password = "kvmautotest"
gateway_password = "kvmautotest"

cfg_name = "/etc/sysconfig/network-scripts/ifcfg-eno4"

host_eno4 = """
DEVICE="eno4" \\
NAME="eno4" \\
ONBOOT="yes" \\
TYPE=Ethernet \\
BOOTPROTO="static" \\
IPADDR="192.168.122.3" \\
NETMASK="255.255.255.0" \\ \\
NM_CONTROL="no" \\
"""
gateway_eno4 = """
DEVICE="eno4" \\
NAME="eno4" \\
ONBOOT="yes" \\
TYPE=Ethernet \\
BOOTPROTO="static" \\
IPADDR="192.168.122.1" \\
NETMASK="255.255.255.0" \\
NM_CONTROL="no" \\
"""

########################### Configure Host ####################################

cmd = "sed -i 'a\%s' %s" % (host_eno4, cfg_name)

child = pexpect.spawn('ssh root@%s' % host)
child.logfile=sys.stdout

try:
    i = child.expect(['(yes/no?)', 'password:'])
    if i == 0:
        child.sendline('yes')
        child.expect('password:', timeout=10)
        child.sendline(host_password)
    else:
        child.sendline(host_password)

    child.expect('#')
    child.sendline('echo > %s' % cfg_name)
    child.expect('#')
    child.sendline(cmd)
    child.expect('#')
    child.sendline('sed -i /^$/d %s' % cfg_name)
    child.expect('#')
    child.sendline('ifconfig virbr0 down')
    child.expect('#')
    child.sendline('ifdown eno4')
    child.expect('#')
    child.sendline('ifup eno4')
    child.expect('#')
except pexpect.EOF:
    print "#" * 100
    print "Host SetUp Completed."
    print "#" * 100

#
time.sleep(5)

########################### Configure Gateway ####################################

child = pexpect.spawn('ssh root@%s' % gateway)

# write the log to screen
child.logfile = sys.stdout
cmd1 = "sed -i 'a\%s' %s" % (gateway_eno4, cfg_name)

# This file exists when you installed the RHEL,so just use its default configuration
dnsmasq_conf = "/var/lib/libvirt/dnsmasq/default.conf"
change_dnsmasq = "sed -i 's/virbr0/eno4/g' %s " % dnsmasq_conf

with open('gateway-iptables','r') as f:
    content = f.read()
iptables_conf = "/etc/sysconfig/iptables"
write_to_iptables_cmd = 'echo \"%s\" > %s' % (content, iptables_conf)

try:
    i = child.expect(['(yes/no?)', 'password:'])
    if i == 0:
        child.sendline('yes')
        child.expect('password:', timeout=10)
        child.sendline(gateway_password)
    else:
        child.sendline(gateway_password)

    # Configure the interface and bring it up
    child.expect('#')
    child.sendline('echo > %s' % cfg_name)
    child.expect('#')
    child.sendline(cmd1)
    child.expect('#')
    child.sendline('sed -i /^$/d %s' % cfg_name)
    child.expect('#')
    child.sendline('ifconfig virbr0 down')
    child.expect('#')
    child.sendline('ifdown eno4')
    child.expect('#')
    time.sleep(1)
    child.sendline('ifup eno4')
    child.expect('#')
    time.sleep(1)
    # Configure the iptables and reload it
    #child.sendline('yum -y install iptables-services')
    #child.expect('#')
    child.sendline('service iptables stop')
    child.sendline('echo > %s' % iptables_conf)
    child.expect('#')
    child.sendline(write_to_iptables_cmd)
    child.expect('#')
    child.sendline('service iptables start')
    child.expect('#')

    # Modify the dnsmasq conf file and reload it
    child.sendline(change_dnsmasq)
    child.expect('#')
    child.sendline('killall -9 /sbin/dnsmasq')
    child.expect('#')
    child.sendline('/sbin/dnsmasq --conf-file=/var/lib/libvirt/dnsmasq/default.conf --dhcp-script=/usr/libexec/libvirt_leaseshelper')

    # Open the forward function
    child.sendline('echo 1 > /proc/sys/net/ipv4/ip_forward')
    child.expect('#')
except pexpect.EOF:
    print "#" * 100
    print "Host SetUp Completed."
    print "#" * 100
