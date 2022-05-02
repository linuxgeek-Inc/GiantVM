import subprocess

cc_lock = {"name":"cc_lock", "nr":0, "time":list()}
spin_lock = {"name":"spin_lock", "nr":0, "time":list()}

def print_stat(target):
    print("[{0}] average time: {1}, nr: {2}".format(target["name"], 
            sum(target["time"]) / target["nr"], target["nr"]))

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

        target["nr"] += 1
        target["time"].append(int(line[line.rfind("[")+1:-1]))

    print_stat(cc_lock)
    print_stat(spin_lock)

