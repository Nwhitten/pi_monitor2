import subprocess
import re
import socket
import json
import psutil
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

class Monitor:

    def get_thermal_temperature(self):
        cmd ="cat /sys/class/thermal/thermal_zone0/temp"
        thermal = subprocess.check_output(cmd, shell=True).decode("utf8")
        #return float(thermal) / 1000.0
        return round(float(thermal) / 1000.0, 1)


    # returns the temperature of the SoC as measured by the on-board temperature sensor
    def get_soc_temperature(self):
        cmd = "vcgencmd measure_temp"
        temp = subprocess.check_output(cmd, shell=True).decode("utf8")
        return float(re.findall(r'\d+\.\d+', temp)[0])

    # uptime in seconds
    def get_uptime(self):
        uptime = subprocess.check_output("cat /proc/uptime", shell=True).decode("utf8")
        return float(uptime.split(" ")[0])
        
    def get_uptime_formatted(self):
        time = self.get_uptime()
        day = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        return "%dd %02dh %02dm %02ds" % (day, hour, minutes, seconds)

    # returns load averages for 1, 5, and 15 minutes
    def get_load_average(self):
        uptime = subprocess.check_output("uptime", shell=True).decode("utf8")
        load_average = uptime.split("load average:")[1].split(",")
        return list(map(float, load_average))
    
    def get_cpu_load(self):
        cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
        return subprocess.check_output(cmd, shell=True).decode("utf-8")
    
    def get_cpu_percent(self):
    	return str(psutil.cpu_percent())

    def get_kernel_release(self):
        return subprocess.check_output("uname -r", shell=True).decode("utf8").strip()
    
    def get_disk_usage(self):
        cmd = 'df -h | awk \'$NF=="/"{printf "%d/%d", $3,$2,$5}\''
        return subprocess.check_output(cmd, shell=True).decode("utf-8")
        
    def get_disk_percent(self):
        cmd = 'df -h | awk \'$NF=="/"{printf "%.1f\", $5}\''
        return subprocess.check_output(cmd, shell=True).decode("utf-8")
        
    def get_ipaddress(self):
        cmd = "hostname -I | cut -d' ' -f1"
        return subprocess.check_output(cmd, shell=True).decode("utf-8")

    
     #returns total, free and available memory in kB
    def get_memory_usage(self):
        meminfo = subprocess.check_output("cat /proc/meminfo", shell=True).decode("utf8").strip()        
        memory_usage = meminfo.split("\n")

        total_memory = [x for x in memory_usage if 'MemTotal' in x][0]
        free_memory = [x for x in memory_usage if 'MemFree' in x][0]
        available_memory = [x for x in memory_usage if 'MemAvailable' in x][0]

        total_memory = re.findall(r'\d+', total_memory)[0]
        free_memory = re.findall(r'\d+', free_memory)[0]
        available_memory = re.findall(r'\d+', available_memory)[0]

        data = {
            "total_memory": int(total_memory),
            "free_memory": int(free_memory),
            "available_memory": int(available_memory)
        }
        return data
    
    def get_memory_percent(self):
        cmd = "free -m | awk 'NR==2{printf \"%.1f\",$3*100/$2 }'"
        return subprocess.check_output(cmd, shell=True).decode("utf-8")




    def get_json(self):
        data = {
            "uptime": self.get_uptime(),
            "formatted_uptime": self.get_uptime_formatted(),
            "host_name": socket.gethostname(),
            "ip": self.get_ipaddress(),
            "kernel_release": self.get_kernel_release(),
            "soc_temp": self.get_soc_temperature(),
            "temp": self.get_thermal_temperature(),
            "load_avg": self.get_load_average(),
            "load_current": self.get_cpu_load(),
            "load_percent": self.get_cpu_percent(),
            "memory_usage": self.get_memory_usage(),
            "memory_percent": self.get_memory_percent(),
            "disk_usage": self.get_disk_usage(),
            "disk_percent": self.get_disk_percent()
        }
        return json.dumps(data)


class MonitorServer(BaseHTTPRequestHandler):

    def set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self.set_response()
        print(self.path)
        if self.path == "/monitor2.json" or self.path == "/monitor2":
            response = Monitor().get_json().encode()
            self.wfile.write(response)


port = 8089
port_argument = sys.argv[-1]
if port_argument.isdigit():
    port = int(port_argument)

server_address = ('', port)
httpd = HTTPServer(server_address, MonitorServer)
httpd.serve_forever()
