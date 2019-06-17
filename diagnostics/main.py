import datetime
import time
import os
from send_mail import smtp_main as mail

def round2(val):
    return str(round(float(val), 2))

try:
    while (True):
        time.sleep(5)
        diagnostics = ""

        ip = "IP address: " + os.popen('hostname -I').readline().strip()
        ping = "Network status: " + "Active" if os.system("ping -c 1 8.8.8.8 >/dev/null 2>&1") == 0 else "Inactive"
        tot_mem, used_mem, free_mem = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
        ram = "RAM Usage: " + round2(100 * used_mem / tot_mem) + "%"
        cpu = "CPU Usage: " + round2(os.popen("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }'").readline()) + "%"
        timestamp = datetime.datetime.now().strftime("%A, %d %B %Y %I:%M%p")
        diagnostics = timestamp + '\n' + ip + '\n' + ping + '\n' + ram + '\n' + cpu + '\n'

        print(diagnostics + '\n')
except KeyboardInterrupt:
    print("Exited normally.")
except Exception as e:
    print("Exiting...")
    mail("Abnormal exit | Diagnostics", str(e))
