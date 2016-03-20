import os
import urllib3

http = urllib3.PoolManager()
w = http.request('GET', 'http://canucks.nhl.com/club/standings.htm?type=LEA')
code = w.read()
w.close()

print("This is TankBot 1.0, your friendly tank supporter. Any issues, please message /u/schlaBAM. \n")

print("Please wait a moment while a version check is run.\n")

if os.path.exists('tankbot.py'):
    f = open('tankbot.py', 'r')

    if f.read(22).strip() != code[0: 22].strip():
        f.close()
        print('Downloading new version...\n')
        f = open ('tankbot.py', 'wb')
        f.write(code)
        f.close()
    else:
        print('Version check passed.\n')
        f.close()
else:
    print('Downloading script...\n')
    f = open('tankbot.py', 'wb')
    f.write(code)
    f.close()

exec(open("tankbot.py").read())
