#!/usr/bin/python3
#
# COMP 332, Spring 2018
# Chat server
# Yuan Sun
# Usage:
#   python3 chat_server.py <host> <port>
#

import socket
import sys
import threading

class ChatProxy():

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.server_backlog = 1
        self.chat_list = {}
        self.chat_id = 0
        self.lock = threading.Lock()
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.server_host, self.server_port))
            server_sock.listen(self.server_backlog)
        except OSError as e:
            print ("Unable to open server socket")
            if server_sock:
                server_sock.close()
            sys.exit(1)

        # Wait for user connection
        while True:
            conn, addr = server_sock.accept()
            self.add_user(conn, addr)
            thread = threading.Thread(target = self.serve_user,
                    args = (conn, addr, self.chat_id))
            thread.start()

    def add_user(self, conn, addr):
        print ('User has connected', addr)
        self.chat_id = self.chat_id + 1
        self.lock.acquire()
        self.chat_list[self.chat_id] = (conn, addr)
        self.lock.release()

    def read_data(self, conn):

        # Fill this out
        print("In read data")
        bin_message = b''
        while True:
            read_message = conn.recv(4096)
            bin_message += read_message
            message = bin_message.decode('utf-8')
            
            data = message.split(';')[1]
            words = data.split(': ')[1]
            length = int(message.split(';')[0])
            if length == len(words):
                return message
                bin_message = b''
                ### check here
            """
            if not read_message:
                
                break
            """

    def send_data(self, user, data):
        self.lock.acquire()

        # Fill this out
        print("In send data")
        for i in self.chat_list:
            if i != user:
                (conn, addr) = self.chat_list[i]
                bin_data = data.encode('utf-8')
                conn.send(bin_data)
            else:
                continue
            
            
        self.lock.release()

    def cleanup(self, user):
        self.lock.acquire()

        # Fill this out
        print("In cleanup")
    
        del self.chat_list[user]
        self.lock.release()

    def serve_user(self, conn, addr, user): 
        # Fill this out
        print("In serve user")
        message = ''
        while True:
            read_message = self.read_data(conn)
            if not read_message:
                self.cleanup(user)
                return
            message += read_message
            self.send_data(user, message)
            message = ''

def main():

    print (sys.argv, len(sys.argv))
    server_host = 'localhost'
    server_port = 50007

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    chat_server = ChatProxy(server_host, server_port)

if __name__ == '__main__':
    main()
