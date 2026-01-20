# Software Defined Network using Mininet and Ryu controller 
A redundant ring topology consisiting of Layer 2 and Layer 3 architecture with a STP and OSPF.

Controller: Ryu(OpenFlow 1.3) with STP
# Topology:
Core: 3 Open vSwitch(OVS) connected in a Ring.
Edge: 3 FFR Routers running OSPF.
Hosts: 3 Hosts connected with the routers.
# Protocols:
STP: To prevents Layer 2 loops in the ring.
OSPF: Handles Layer 3 routing between areas.
Visualization: FlowManager Web Dashboard.

# Required:
Ubuntu / Linux VM
Python 3
Mininet
Ryu SDN Framework
FRRouting (FRR) installed on the VM

# Terminal 1:
ryu-manager simple_switch_stp_13.py flowmanager/flowmanager.py --observe-links --verbose

# Terminal 2:
sudo python3 ospf_sdn_topo.py

# Terminal 3:
sudo watch -n 1 ovs-ofctl dump-flows s1
(To view flows/rules in realtime on the switch)

# Browser:
http://localhost:8080/home/index.html
(In order for the routers to be visibile on the WebGUI, we need to run "pingall" command in mininet)

<img width="811" height="492" alt="image" src="https://github.com/user-attachments/assets/2eeb0883-0a0c-4e7e-84f1-011e64ef9b35" />

Since the RYU cannot see the host, so it is not visibile in the topology view. Instead it is shown as PC symbol.
Which can verified by the mac address of the interface of the router.

<img width="497" height="239" alt="image" src="https://github.com/user-attachments/assets/6931140a-021f-4b5a-9fb1-bdb421dbfb5b" />
