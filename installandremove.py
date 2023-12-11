import subprocess
import sys

print('您输入的密码是', sys.argv[1])
print('内核：', sys.argv[2])
print('头文件：', sys.argv[3])
print('安装', sys.argv[4])
echo = subprocess.Popen(['echo',sys.argv[1]],
                        stdout=subprocess.PIPE,
                        )
if sys.argv[4] == 'install':
    sudo = subprocess.Popen(['sudo','-S','apt','install',sys.argv[2],sys.argv[3],'-y'],
                        stdin=echo.stdout,
                        stdout=subprocess.PIPE,
                        )
else:
    sudo = subprocess.Popen(['sudo','-S','apt','purge',sys.argv[2],sys.argv[3],'-y'],
                        stdin=echo.stdout,
                        stdout=subprocess.PIPE,
                        )

for line in iter(sudo.stdout.readline, b''):
    line = line.decode('utf-8')
    sys.stdout.write(line)
    sys.stdout.flush()
    
sudo.wait()