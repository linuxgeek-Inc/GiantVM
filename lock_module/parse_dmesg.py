import subprocess
import psutil
import math

clk = 1 / (psutil.cpu_freq().current / 1000)
cc_lock = {"name":"cc_lock  ", "nr":0, "time":list()}
spin_lock = {"name":"spin_lock", "nr":0, "time":list()}

def print_stat(target):
    avg = sum(target["time"])*1000 / target["nr"]
    print(target["time"])
    var = sum([(avg-i)**2 for i in target["time"]]) / len(target["time"])
    print("[{0}] average clock: {1:15.5f} co: {2:15.5f}, nr: {3}".format(target["name"],
            avg, math.sqrt(var), target["nr"]))
    return avg

if __name__ == "__main__":
    lines = subprocess.check_output(["sudo", "dmesg"]).decode()
    lines = lines.split("\n")
    for line in lines:
        if "cc-lock" in line:
            target = cc_lock
        elif "spinlock" in line:
            target = spin_lock
        else:
            target = None
        if target is None:
            continue

        target["nr"] += 1000
        target["time"].append(int(line[line.rfind("[")+1:-1])/(clk*1000))

    cc_avg = print_stat(cc_lock)
    spin_avg = print_stat(spin_lock)

    print("improvment: {0:10.5f}%".format((spin_avg-cc_avg)/spin_avg*100))

