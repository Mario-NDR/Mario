#!/bin/bash
# iptables -I INPUT -j NFQUEUE --queue-balance 0:3
# iptables -I FORWARD -j NFQUEUE --queue-balance 0:3
# iptables -I OUTPUT -j NFQUEUE --queue-balance 0:3
# nohup suricata -c /opt/marioips/marioips.yaml -q 0 -q 1 -q 2 -q 3 &
iptables -I INPUT -j NFQUEUE
iptables -I FORWARD -j NFQUEUE
iptables -I OUTPUT -j NFQUEUE
nohup suricata -c /opt/marioips/marioips.yaml -q 0 > /opt/marioips/log/marioips.log &
