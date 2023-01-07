#!/usr/bin/env python3

import sys
import socket


config = {
  'host': 'localhost',
  'port': 30001
}

if __name__ == "__main__":
  print('yo', sys.argv)
  cmd = sys.argv[1]
  print(f'config: {config}')
  print(f'cmd: {cmd}')


  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((config['host'], config['port']))
    s.send((f'{cmd}\n').encode('utf8'))
    data = s.recv(1024)
    if not data:
      print('no data!')
    else:
      print('!!', data, '\n=====\n', len(data),  type(data))
      result = data.decode('ascii').strip()
      print('{cmd} => "{result}"')


