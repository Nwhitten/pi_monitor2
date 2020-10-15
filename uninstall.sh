#!/bin/bash
systemctl stop pi-monitor2.service

echo ""

echo "Removing old files files..."
rm /usr/local/bin/pi-monitor2.py
rm /etc/systemd/system/pi-monitor2.service

echo ""