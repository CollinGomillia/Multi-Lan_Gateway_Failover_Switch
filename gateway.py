import re
import subprocess
import time

PRIMARY_IF = "eth0" #Set for main, in this project it is our ethernet cord
STANDBY_IF = "wlan0" #Set for our phone hotspot, or backup
PING_TARGETS = ["8.8.8.8", "8.8.4.4"] #Second address is our backup
PING_COUNT = 3
CHECK_INTERVAL_S = 15 #How many seconds it will take to check connections
DRY_RUN = True

#Helps find router address
gateways = {}


#Runs a command and the output will print
def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout

#Router address for interface
def gateway_for(dev):
    for gw, d in re.findall(r"default via (\S+) dev (\S+)", run(["ip", "route", "show", "default"])):
        gateways[d] = gw
    return gateways.get(dev)

#Current interface with the default route
def current_dev():
    m = re.search(r"default via \S+ dev (\S+)", run(["ip", "route", "show", "default"]))
    return m.group(1) if m else None

#Returns if a ping target is answered in this method
def link_up(dev):
    for target in PING_TARGETS:
        try:
            r = subprocess.run(["ping", "-c", str(PING_COUNT), "-W", "2", "-I", dev, target],
                               capture_output=True, timeout=20)
            if r.returncode == 0:
                return True
        except (subprocess.TimeoutExpired, OSError):
            pass
    return False

#Our switch method, true if default route fails
def switch_to(dev):
    gw = gateway_for(dev)
    if not gw:
        print(f"  {dev} no know route available, will switch when address is present")
        return
    cmd = ["sudo", "ip", "route", "replace", "default", "via", gw, "dev", dev]
    if DRY_RUN:
        print("  [dry run]", " ".join(cmd))
    else:
        subprocess.run(cmd)
        print(f"  default route is now {dev}")

#Will check primary connection first, then backup, printing which are running or down, and default route connected to
def main():
    print(f"Failover started. Primary: {PRIMARY_IF}, Standby: {STANDBY_IF}, DRY_RUN={DRY_RUN}")
    while True:
        primary_up = link_up(PRIMARY_IF)
        standby_up = link_up(STANDBY_IF)
        print(f"\n{time.strftime('%H:%M:%S')}  {PRIMARY_IF}: {'up' if primary_up else 'DOWN'}"
              f"  {STANDBY_IF}: {'up' if standby_up else 'DOWN'}")

        if primary_up:
            target = PRIMARY_IF
        elif standby_up:
            target = STANDBY_IF
        else:
            target = None

        if target is None:
            print("  no working link")
        elif target != current_dev():
            print(f"  switching to {target}")
            switch_to(target)
        else:
            print(f"  staying on {target}")

        time.sleep(CHECK_INTERVAL_S)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")