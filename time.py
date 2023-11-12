import os
import subprocess
import time

current_directory = os.getcwd()

while True:
    subprocess.call([f'{current_directory}/script.sh'])
    time.sleep(5)
