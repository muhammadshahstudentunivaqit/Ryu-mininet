# Software Defined Network using Mininet and Ryu controller 
The Project implements a Hybrid A redundant ring topology consisiting of Layer 2 and Layer 3 architecture with a STP and OSPF.

* **Controller:** Ryu (OpenFlow 1.3) with STP
* **Topology:**
  * **Core:** 3 Open vSwitch (OVS) connected in a Ring.
  * **Edge:** 3 FFR Routers running OSPF.
  * **Hosts:** 3 Hosts connected with the routers.
* **Protocols:**
  * **STP:** To prevent Layer 2 loops in the ring.
  * **OSPF:** Handles Layer 3 routing between areas.
* **Visualization:** FlowManager Web Dashboard.


**Required:**
* Ubuntu / Linux VM
* Python 3
* Mininet
* Ryu SDN Framework
* FRRouting (FRR)


<img width="1259" height="566" alt="{3FA878D0-5190-4584-ADFC-6003C5023ED4}" src="https://github.com/user-attachments/assets/5435f5b9-87aa-43ac-a353-04c21cc159e4" />


Terminal 1:
`ryu-manager simple_switch_stp_13.py flowmanager/flowmanager.py --observe-links --verbose`

Terminal 2:
`sudo python3 ospf_sdn_topo.py`

Terminal 3:
`sudo watch -n 1 ovs-ofctl dump-flows s1`

(To view flows/rules in realtime on the switch)

Browser:
http://localhost:8080/home/index.html

(In order for the routers to be visibile on the WebGUI, we need to run "pingall" command in mininet)

<img width="811" height="492" alt="image" src="https://github.com/user-attachments/assets/2eeb0883-0a0c-4e7e-84f1-011e64ef9b35" />

Since the RYU cannot see the host, so it is not visibile in the topology view. Instead it is shown as PC symbol.
Which can verified by the mac address of the interface of the router.

<img width="497" height="239" alt="image" src="https://github.com/user-attachments/assets/6931140a-021f-4b5a-9fb1-bdb421dbfb5b" />



In order to test the STP redundency, we can bring down the link connectivity between S1 and S2

<img width="951" height="349" alt="image" src="https://github.com/user-attachments/assets/e6e3d608-0089-4a10-bb8e-46ef7fa85f0b" />

As we can see for the S1-Eth1, the State is O, which means the link is still up. The Previous command didn't have any effect so we will be removing the port for the time being as it will simulate as link connectivity disconnection/failure.

`sh ovs-vsctl del-port s1 s1-eth1`

<img width="918" height="278" alt="image" src="https://github.com/user-attachments/assets/df6d125d-b74a-4429-a107-335560d94653" />

As we can see that some pings gets drop while STP re-calculates and activates the redundent path and the pings resumes/routed through s1-eth2 instead of s1-eth1

<img width="1113" height="584" alt="image" src="https://github.com/user-attachments/assets/9cf11487-cdc9-49a3-a044-c76667c229b0" />
