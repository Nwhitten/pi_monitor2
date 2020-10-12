#!/bin/bash
systemctl stop pi-monitor2.service

echo ""

echo "Downloading files..."

wget https://raw.githubusercontent.com/nwhitten/pi_monitor/master/pi-monitor2.py
wget https://raw.githubusercontent.com/nwhitten/pi_monitor/master/pi-monitor2.service

echo ""

echo "Removing old files files..."
rm /usr/local/bin/pi-monitor2.py
rm /etc/systemd/system/pi-monitor2.service

echo ""

echo "Moving files..."
mv pi-monitor.py /usr/local/bin/
mv pi-monitor.service /etc/systemd/system/

echo ""

echo "Starting pi-monitor service..."
systemctl daemon-reload
systemctl enable pi-monitor2.service 
systemctl start pi-monitor2.service