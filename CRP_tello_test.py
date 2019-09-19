from CRP_tello import Tello
import sys
from datetime import datetime
import time
import os

#start_time = str(datetime.now())
start_time = datetime.now().strftime("%H%M%S")
#print("date : ",datetime.now().strftime("%H%M%S"))
print("date : ", start_time)
print("repertoire : ", os.getcwd())
#file_name = "./command-Mission_Pad.txt"
#file_name = "./command-curve.txt"
file_name = "./command-deplace.txt"
#file_name = "./command-retour.txt"
#file_name = "./command-circuit_MP.txt"

f = open(file_name, "r")
commands = f.readlines()
print(commands)
tello = Tello()
for command in commands:
    if command != '' and command != '\n':
        command = command.rstrip()

        if command.find('delay') != -1:
            sec = float(command.partition('delay')[2])
            print ('delay %s' % sec)
            time.sleep(sec)
            pass
        else:
            tello.send_command(command)

log = tello.get_log()

out = open('./log/' + start_time + '.txt', 'w')
for stat in log:
    stat.print_stats()
    str = stat.return_stats()
    out.write(str)
