import subprocess

cc_lock = {"name":"cc_lock  ", "nr":0, "time":list()}
spin_lock = {"name":"spin_lock", "nr":0, "time":list()}

def print_stat(target):
    avg = sum(target["time"]) / target["nr"]
    print("[{0}] average time: {1}, nr: {2}".format(target["name"], 
            avg, target["nr"]))
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

        target["nr"] += 1
        target["time"].append(int(line[line.rfind("[")+1:-1]))

    cc_avg = print_stat(cc_lock)
    spin_avg = print_stat(spin_lock)

    print("improvment: {0:.3f}%".format((spin_avg-cc_avg)/spin_avg*100))

