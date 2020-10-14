# Pi Monitor

Python utility to get Raspberry Pi metrics. This is an experimental utility, use at your own risk :)

This is just a very simple Python script using a http server to provide some Raspberry Pi metrics via REST calls, like temperature, load average and more.

## Usage

The server will make a single endpoint available on the default port `8089`:
`http://YOUR_IP:8089/monitor2.json` that will return a JSON like this:

```json
{

	"uptime": 174896.66, 
	"ip": "192.168.11.105", 
	"formatted_uptime": "2d 01h 08m 44s",
	"kernel_release": "4.19.118-v7+", 
	"soc_temp": 50.5, 
	"temp": 49.9, 
	"load_avg": [0.11, 0.26, 0.37], 
	"load_current": "0.11", 
	"load_percent": "9.9", 
	"memory_usage": {
		"total_memory": 441160, 
		"free_memory": 83300, 
		"available_memory": 187832
	}, 
	"memory_percent": "40.9", 
	"disk_usage": "3/14", 
	"disk_percent": "23.0"
}
```

## Installation

### Automatic

`wget -O - https://raw.githubusercontent.com/nwhitten/pi_monitor/master/install2.sh | sudo bash`

### Manual

You can download the files manually and run it the way you like. If you don't want Pi Monitor to run as a service you can just run as `python3 pi_monitor2.py`

## Configuration

If you're running it using the automatic installation you can change the username and default port in which Pi Monitor is running by changing the following settings on your `pi-monitor2.service`

```
[Service]
ExecStart=/usr/bin/python3 -u /usr/local/bin/pi-monitor2.py 8089
User=pi
```

Before doing so, make sure to stop the service with
`sudo systemctl stop pi-monitor2.service`
and then start it again after your changes with
`sudo systemctl start pi-monitor2.service`

If you're running it manually you can just change the default port by sending it as a parameter like:
`python3 pi_monitor2.py 8181`

Kill it all by using the following:
`sudo systemctl stop pi-monitor2.service | sudo rm /usr/local/bin/pi-monitor2.py | sudo rm /etc/systemd/system/pi-monitor2.service |sudo systemctl daemon-reload`

## Compatibility

This was tested on Raspberry Pi OS (32 bit), kernel 5.4.51-v7+
