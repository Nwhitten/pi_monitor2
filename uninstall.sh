#!/bin/bash
systemctl stop status-check-button.service
systemctl stop status-check-lights.service

echo ""

echo "Downloading files..."

wget https://raw.githubusercontent.com/nwhitten/Status_Check_Build/master/update.sh
wget https://raw.githubusercontent.com/nwhitten/Status_Check_Build/master/button.py
wget https://raw.githubusercontent.com/nwhitten/Status_Check_Build/master/inky_update.py
wget https://raw.githubusercontent.com/nwhitten/Status_Check_Build/master/status_lights.py
wget https://raw.githubusercontent.com/nwhitten/Status_Check_Build/master/pi-stats.py
wget https://raw.githubusercontent.com/nwhitten/Status_Check_Build/master/PiholeControl.py
wget https://raw.githubusercontent.com/nwhitten/Status_Check_Build/master/all_pi_stats.py


wget https://raw.githubusercontent.com/nwhitten/Status_Check_Build/master/status-check-button.service
wget https://raw.githubusercontent.com/nwhitten/Status_Check_Build/master/status-check-lights.service

wget https://raw.githubusercontent.com/nwhitten/Status_Check_Build/master/inky-hole_assets/logo0.png
wget https://raw.githubusercontent.com/nwhitten/Status_Check_Build/master/inky-hole_assets/logo1.png
wget https://raw.githubusercontent.com/nwhitten/Status_Check_Build/master/inky-hole_assets/logo2.png

echo ""

echo "Removing old files files..."
rm -r /usr/local/bin/status_check
rm /etc/systemd/system/status-check-button.service
rm /etc/systemd/system/status-check-lights.service

echo ""

mkdir /usr/local/bin/status_check/

echo "Moving files..."

mv update.sh /usr/local/bin/status_check/
mv button.py /usr/local/bin/status_check/
mv inky_update.py /usr/local/bin/status_check/
mv status_lights.py /usr/local/bin/status_check/
mv pi-stats.py /usr/local/bin/status_check/
mv PiholeControl.py /usr/local/bin/status_check/
mv all_pi_stats.py /usr/local/bin/status_check/

mv logo0.png /usr/local/bin/status_check/
mv logo1.png /usr/local/bin/status_check/
mv logo2.png /usr/local/bin/status_check/

mv status-check-button.service /etc/systemd/system/
mv status-check-lights.service /etc/systemd/system/

echo ""

echo "Starting services..."
systemctl daemon-reload
systemctl enable status-check-button.service
systemctl start status-check-button.service

systemctl enable status-check-lights.service
systemctl start status-check-lights.service

#echo ""
#echo "Installing crontab..."
#(crontab -l; echo "*/10 * * * * python3 /usr/local/bin/status_check/inky_update.py";) | crontab -
