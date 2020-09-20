from proxy import proxy
from sys import argv, exit

try:
    p = proxy(argv[1], int(argv[2]), int(argv[3]))
except:
    print 'Use: main.py <Server IP> <Server Port> <Client Port>'
    exit(1)

p.initialize()

try:
    p.start()
except KeyboardInterrupt:
    print('Exiting peacfully')
    p.stop()
    exit(0)
