#!/usr/bin/env python3
import time
import sys
import socket

try:
  # split cmd line arguments into pairs, then put in dictionary:
  # ex: ['server.py', 'a', 'aval', 'b', 'bval'] => {'a':'aval', 'b':'bval'}
  args = dict([(sys.argv[i], sys.argv[i+1]) for i in range(1, len(sys.argv), 2)])
  if not args:
    raise Exception("You must provide parameters!")
except:
  print(f'could not make dictionnary from {sys.argv[1:]}')
  sys.exit(-1)


print('program arguments:', args)

config = {
  'port' : 60000,
  'host' : '0.0.0.0'
}

def process(values, client_cmd):
  return values.get(client_cmd)


if __name__ == "__main__":
  print(f'starting server: {config}')
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((config['host'], config['port']))
    print('listening...')
    s.listen()
    conn, address = s.accept()
    count = 0
    with conn:
      print(f'connection from {address}')
      while True:
        data = conn.recv(2048)
        if not data:
          print('no data')
          time.sleep(0.1)
          break
        # remove the \n from the data and convert bytes to str
        cmd = data.decode().strip()
        response = process(args, cmd)
        if not response:
          print(f'unknown cmd: "{cmd}"')
          break
        print(f'{count} "{cmd}" => "{response}"')
        count += 1
        conn.sendall(response.encode())

