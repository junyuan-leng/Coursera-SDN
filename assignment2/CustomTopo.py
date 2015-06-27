'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.util import irange

def splitList(originalList, n):
    splittedList = []
    for i in range(0, len(originalList), n):
        splittedList.append(originalList[i:i+n])
    return splittedList

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        coreSwitches = []
        aggrSwitches = []
        edgeSwitches = []
        hosts = []

        coreSwitch = self.addSwitch('c%s' % 1)
        coreSwitches.append(coreSwitch)

        for i in irange(1, fanout):
            aggrSwitch = self.addSwitch('a%s' % i)
            aggrSwitches.append(aggrSwitch)

        for i in irange(1, fanout**2):
            edgeSwitch = self.addSwitch('e%s' % i)
            edgeSwitches.append(edgeSwitch)

        for i in irange(1, fanout**3):
            host = self.addHost('h%s' % i)
            hosts.append(host)

        splittedCoreSwitches = splitList(coreSwitches, fanout)
        splittedAggrSwitches = splitList(aggrSwitches, fanout)
        splittedEdgeSwitches = splitList(edgeSwitches, fanout)
        splittedHosts = splitList(hosts, fanout)

        for i in range(len(coreSwitches)):
            for switch in splittedAggrSwitches[i]:
                self.addLink(coreSwitches[i], switch, **linkopts1)

        for i in range(len(aggrSwitches)):
            for switch in splittedEdgeSwitches[i]:
                self.addLink(aggrSwitches[i], switch, **linkopts2)

        for i in range(len(edgeSwitches)):
            for host in splittedHosts[i]:
                self.addLink(edgeSwitches[i], host, **linkopts3)

topos = { 'custom': ( lambda: CustomTopo() ) }
