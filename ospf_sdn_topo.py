devunivaq@devunivaq-VM:~/sdn-project/Project-N$ cat ospf_sdn_topo.py 
#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

class LinuxRouter(Node):
    """
    A Node with IP forwarding enabled and Private Directories for FRR.
    """
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

def run():
    # 1. Initialize Mininet
    # We requested private directories for FRR to ensure isolation
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)

    # Add the Ryu Controller
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    info( '*** Adding Area 0 (SDN Backbone) Switches\n' )
    s1 = net.addSwitch('s1', dpid='0000000000000001')
    s2 = net.addSwitch('s2', dpid='0000000000000002')
    s3 = net.addSwitch('s3', dpid='0000000000000003')

    info( '*** Adding Area Routers (ABRs)\n' )
    # Note: We use privateDirs to give each router its own config/run folder
    frr_dirs = ['/etc/frr', '/var/run/frr']
    
    r1 = net.addHost('r1', cls=LinuxRouter, ip='10.0.0.1/24', privateDirs=frr_dirs)
    r2 = net.addHost('r2', cls=LinuxRouter, ip='10.0.0.2/24', privateDirs=frr_dirs)
    r3 = net.addHost('r3', cls=LinuxRouter, ip='10.0.0.3/24', privateDirs=frr_dirs)

    info( '*** Adding End Hosts\n' )
    h1 = net.addHost('h1', ip='192.168.1.2/24', defaultRoute='via 192.168.1.1')
    h2 = net.addHost('h2', ip='192.168.2.2/24', defaultRoute='via 192.168.2.1')
    h3 = net.addHost('h3', ip='192.168.3.2/24', defaultRoute='via 192.168.3.1')

    info( '*** Creating Links\n' )
    # Backbone Ring
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, s1)

    # Routers to Backbone
    net.addLink(r1, s1, intfName1='r1-eth0') 
    net.addLink(r2, s2, intfName1='r2-eth0')
    net.addLink(r3, s3, intfName1='r3-eth0')

    # Hosts to Routers
    net.addLink(h1, r1, intfName2='r1-eth1')
    net.addLink(h2, r2, intfName2='r2-eth1')
    net.addLink(h3, r3, intfName2='r3-eth1')

    info( '*** Starting Network\n' )
    net.start()

    info( '*** Configuring Interfaces & FRR\n' )
    
    # Helper function to start FRR on a router
    def start_frr(r, router_id, area_net):
        # 1. Configure Interfaces
        r.cmd('ifconfig {}-eth0 10.0.0.{} netmask 255.255.255.0 up'.format(r.name, router_id.split('.')[-1]))
        r.cmd('ifconfig {}-eth1 192.168.{}.1 netmask 255.255.255.0 up'.format(r.name, router_id.split('.')[-1]))
        
        # 2. Create Zebra Config
        r.cmd('echo "hostname {}" > /etc/frr/zebra.conf'.format(r.name))
        r.cmd('echo "password zebra" >> /etc/frr/zebra.conf')
        r.cmd('echo "log file /var/run/frr/zebra.log" >> /etc/frr/zebra.conf')
        
        # 3. Create OSPF Config
        r.cmd('echo "hostname {}" > /etc/frr/ospfd.conf'.format(r.name))
        r.cmd('echo "password zebra" >> /etc/frr/ospfd.conf')
        r.cmd('echo "router ospf" >> /etc/frr/ospfd.conf')
        r.cmd('echo "  ospf router-id {}" >> /etc/frr/ospfd.conf'.format(router_id))
        r.cmd('echo "  network 10.0.0.0/24 area 0" >> /etc/frr/ospfd.conf')
        r.cmd('echo "  network {} area {}" >> /etc/frr/ospfd.conf'.format(area_net, router_id.split('.')[-1]))
        r.cmd('echo "log file /var/run/frr/ospfd.log" >> /etc/frr/ospfd.conf')

        # 4. Set Permissions and Start Daemons
        r.cmd('chown frr:frr /etc/frr/*.conf')
        r.cmd('chown frr:frr /var/run/frr')
        # Start Zebra (Kernel manager)
        r.cmd('/usr/lib/frr/zebra -d -f /etc/frr/zebra.conf')
        time.sleep(1)
        # Start OSPF
        r.cmd('/usr/lib/frr/ospfd -d -f /etc/frr/ospfd.conf')

    # Apply configuration to all routers
    start_frr(r1, '1.1.1.1', '192.168.1.0/24')
    start_frr(r2, '2.2.2.2', '192.168.2.0/24')
    start_frr(r3, '3.3.3.3', '192.168.3.0/24')

    info( '*** Waiting for OSPF Convergence (10s)...\n' )
    time.sleep(10)

    info( '*** Verifying Connectivity (Ping)\n' )
    # Test ping from H1 to H3 automatically
    print("Ping Result H1 -> H3:", h1.cmd('ping -c 3 192.168.3.2'))

    info( '*** Running CLI\n' )
    CLI(net)

    info( '*** Stopping Network\n' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
devunivaq@devunivaq-VM:~/sdn-project/Project-N$ 

