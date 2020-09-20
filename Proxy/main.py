from proxy import proxy
from sys import argv, exit
import threading

def do_shit(server_ip, port):
	p = proxy(server_ip, port, port)
	p.initialize()
	try:
		p.start()
	except KeyboardInterrupt:
		print('Fuck this shit im out')
		p.stop()
		exit(0)

ports = [3333, 3000, 3001, 3002, 3003, 3004, 3005]

try:
    for port in ports:
    	threading.Thread(target=do_shit, args=(argv[1], port)).start()
except:
    print('Use: main.py <Server IP>')
    exit(1)
