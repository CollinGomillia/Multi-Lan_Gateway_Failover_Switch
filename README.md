# Multi-Lan_Gateway_Failover_Switch


#This project is meant to be a Multi-LAN Gateway with a failover switch, the source code is being added to currently.

#Some source code was referenced, I will cite their work below, I only used those with licenses stating that the code
is free to use and look at, code was just needed to see where I needed to be and how
the tests are supposed to work.

#Citations:
GitHub - gitbls/internet-monitor: Monitors internet connectivity. (2026). GitHub. https://github.com/gitbls/internet-monitor
GitHub - gitbls/IMON: Multi-function multi-threaded internet monitor. (2022). GitHub. https://github.com/gitbls/imon


#-----------------------------------------------------------------------------------------------------
#Setting up the failover switch on command line

#Set up the second internet link, in this case I used my phone hotspot
sudo nmcli device wifi connect "HOTSPOT_NAME" password "PASSWORDforHOTSPOT"

#Start the loop to test failover
python3 "main_class_name".py --interval 30






#-----------------------------------------------------------------------------------------------------
#Set-Up on command line to active systemd automatic startup when booting or a crash

Within Gateway class add this function:

def sigterm_stop(signum,frame):
    raise KeyboardInterrupt

signal.signal(signal.SIGTERM, sigterm_stop)

#Next we need to create a file for the service, for this purpose on the command line we will name it the "main class name".service

sudo nano /etc/systemd/system/"main_class_name".service

#inside the file we will enter this:

[Unit]
Description=Multi-link internet gateway failover
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/pi/"project_name"
ExecStart=/usr/bin/python3 /home/pi/"project_name"/"service name" --interfaces eth0,wlan0 --interval 30 --apply-routes
KillSignal=SIGINT
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target

#Save and exit then on the command line use cat and file path to see if this exists

#Next we will load and start it

sudo systemctl daemon-reload
sudo systemctl enable "main_class_name".service
sudo systemctl start "main_class_name".service
systemctl status "main_class_name".service

#That is all you need for it, to stop the service use this on the command line
sudo systemctl stop "main_class_name".service