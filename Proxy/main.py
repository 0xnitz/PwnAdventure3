from proxy import proxy
from sys import argv, exit

try:
    p = proxy(argv[1], int(argv[2]), argv[3], int(argv[4]))
except:
    print 'Use: main.py <Server IP> <Server Port> <Client IP> <Client Port>'
    exit(1)

p.initialize()
p.start()
