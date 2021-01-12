from multiprocessing import Process,Queue,Pool
from socket import *
import sys


HOST = "127.0.0.1"
PORT = 8888


ADDR = (HOST,PORT)

def send_msg(udp_socket, name):
    while True:
        try:
            text = input("发言：")
        except KeyboardInterrupt:
            text = "quit"
        if text == "quit":
            msg = "Q " + name
            udp_socket.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s"%(name,text)
        udp_socket.sendto(msg.encode(),ADDR)

def recv_msg(udp_socket):
    try:
        while True:
            data,addr = udp_socket.recvfrom(8192)
            print("\n"+data.decode() + "\n发言：",end = "")
    except KeyboardInterrupt:
        pass


def main():
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("请输入姓名：")
        msg = "L "+name
        udp_socket.sendto(msg.encode(),ADDR)
        data,addr = udp_socket.recvfrom(512)
        if data.decode() =="OK":
            print("您已进入群聊！")
            break
        else:
            print(data.decode())

    p = Process(target=recv_msg,args =(udp_socket,))
    p.daemon = True
    p.start()

    send_msg(udp_socket,name)


if __name__ == '__main__':
    main()

