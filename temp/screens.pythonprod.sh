#! /bin/sh
sudo mitmproxy -s pkt-ingestion/mitmproxy/pktBuilder.py -P http://54.165.144.31:80 -p 80
