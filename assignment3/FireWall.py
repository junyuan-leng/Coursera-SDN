'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

import csv
from itertools import islice


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

def readPolicyFile():
    policyTuple = namedtuple('Policy', 'seq, mac_0, mac_1')
    policyList = []
    with open(policyFile) as firewallPolicies:
        reader = csv.reader(firewallPolicies)
        for seq, mac_0, mac_1 in islice(reader, 1, None):
            policyList.append(policyTuple(seq=seq, mac_0=mac_0, mac_1=mac_1))
    return policyList


class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):

        def buildFirewallRule(dl_src, dl_dst):
            msg = of.ofp_flow_mod()
            msg.match.dl_src = EthAddr(dl_src)
            msg.match.dl_dst = EthAddr(dl_dst)
            msg.idle_timeout = 0
            msg.hard_timeout = 0
            msg.priority = 10 #high priority
            msg.buffer_id = None
            return msg
        
        policyList = readPolicyFile()
        for policy in policyList:
            ruleOne = buildFirewallRule(policy.mac_0, policy.mac_1)
            ruleTwo = buildFirewallRule(policy.mac_1, policy.mac_0)
            self.connection.send(ruleOne)
            self.connection.send(ruleTwo)
            log.debug("Firewall rules drop traffic between MAC pair %s <-> %s", policy.mac_0, policy.mac_1)
        
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
