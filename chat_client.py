#!/usr/bin/python3
#
# COMP 332, Spring 2018
# Chat client
# Yuan Sun
# Example usage:
#
#   python3 chat_client.py <chat_host> <chat_port>
#

import socket
import sys
import threading


class ChatClient:

    def __init__(self, chat_host, chat_port):
        self.chat_host = chat_host
        self.chat_port = chat_port
        self.start()

    def start(self):

        # Open connection to chat
        try:
            chat_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            chat_sock.connect((self.chat_host, self.chat_port))
            print("Connected to socket")
        except OSError as e:
            print("Unable to connect to socket: ")
            if chat_sock:
                chat_sock.close()
            sys.exit(1)

        threading.Thread(target=self.write_sock, args=(chat_sock,)).start()
        threading.Thread(target=self.read_sock, args=(chat_sock,)).start()

    def write_sock(self, sock):

        # Fill this out
        print("In write sock")
        self.name = input("What's your name?")
        while True:
            message = input()
            length = len(message)
            complete_message = str(length) + ';' + self.name + ': ' + message
            bin_complete_message = complete_message.encode('utf-8')
            sock.send(bin_complete_message)
        sock.close()
        
    def read_sock(self, sock):

        # Fill this out
        print('\n'+"In read sock")
        bin_reply = b''
        while True:
            read_reply = sock.recv(4096)
            bin_reply += read_reply
            reply = bin_reply.decode('utf-8')
            length = int(reply.split(';')[0])
            who_says_what = reply.split(';')[1]
            words = who_says_what.split(': ')[1]
            if len(words) == length:
                print(who_says_what)
                bin_reply = b''
            else:
                continue
            if not read_reply:
                break
            
        
        
def main():

    print (sys.argv, len(sys.argv))
    chat_host = 'localhost'
    chat_port = 50007

    if len(sys.argv) > 1:
        chat_host = sys.argv[1]
        chat_port = int(sys.argv[2])

    chat_client = ChatClient(chat_host, chat_port)

if __name__ == '__main__':
    main()
