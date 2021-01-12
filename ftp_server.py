"""
客户端发起请求:
    服务端：接受请求进行初步处理
        根据请求回复YES/NO
        如果为YES则处理请求



"""

from socket import *
from threading import Thread
import sys
from signal import *
import os
from time import *

HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST,PORT)
FTP = r"/home/python/File/"

class FTPserver(Thread):
    def __init__(self,connfd):
        super(FTPserver, self).__init__()
        self.connfd = connfd

    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            if not data or data == b"E":
                return
            elif data == "L":
                self.do_list()
            elif data[0]=="G":
                filename = data.split(' ')[-1]
                self.do_get(filename)
            elif data[0]=="P":
                filename = data.split(' ')[-1]
                self.do_put(filename)



    def do_list(self):
        file_list = os.listdir(FTP)
        if not file_list:
            self.connfd.send(b"NO")
            return
        else:
            self.connfd.send(b"YES")
            sleep(0.1)
            data = "\n".join(file_list)
            self.connfd.send(data.encode())

    def do_get(self, filename):
        try:
            f = open(FTP+filename,"rb")
        except:
            self.connfd.send(b"NO")
            return
        else:
            self.connfd.send(b"YES")
            sleep(0.1)
        while True:

            data = f.read(1024)
            if not data:
                sleep(0.1)
                self.connfd.send(b"##")
                break
            self.connfd.send(data)
        f.close()

    def do_put(self, filename):
        if os.path.exists(FTP+filename):
            self.connfd.send(b"NO")
            return
        else:
            self.connfd.send(b"YES")
            f = open(filename, "wb")
            while True:
                data = self.connfd.recv(1024)
                print(data)
                if data == b"##":
                    break
                f.write(data)
            f.close()


def main():
    sock = socket()
    sock.bind(ADDR)
    sock.listen(3)
    signal(SIGCHLD,SIG_IGN)

    while True:
        try:
            connfd,addr = sock.accept()
            print("客户端地址：",addr)
        except:
            sys.exit("服务退出")

        t = FTPserver(connfd)

        t.start()

if __name__ == '__main__':
    main()
























