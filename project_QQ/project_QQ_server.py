from multiprocessing import Process,Queue,Pool
from socket import *


HOST = "0.0.0.0"
PORT = 8888

ADDR = (HOST,PORT)

user = {}

def do_login(udp_socket, name, address):
    if name in user or "管理" in name:
        udp_socket.sendto("该用户名已存在！".encode(), address)
        return
    else:
        udp_socket.sendto(b"OK", address)
        msg = "欢迎{}进入聊天室".format(name)
        for i in user:
            udp_socket.sendto(msg.encode(),user[i])
        user[name] = address


def do_chat(udp_socket, name, msg):
    msg = "%s : %s"%(name,msg)
    for i in user:
        if i !=name:
            udp_socket.sendto(msg.encode(),user[i])


def do_quit(udp_socket, name):
    del user[name]
    msg = "%s 退出聊天室"%name
    for i in user:
        udp_socket.sendto(msg.encode(),user[i])


def request(udp_socket):
    while True:
        data,addr = udp_socket.recvfrom(8192)
        tmp = data.decode().split(" ",2)
        if tmp[0] =="L":
            do_login(udp_socket,tmp[1],addr)
        elif tmp[0] == "C":
            do_chat(udp_socket,tmp[1],tmp[2])
        elif tmp[0] == "Q":
            do_quit(udp_socket,tmp[1])


def manager(udp_socket):
    while True:
        text = input("管理员消息：")
        msg = "C 管理员 "+text
        udp_socket.sendto(msg.encode(),ADDR)


def main():
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind(ADDR)

    p = Process(target=request,args=(udp_socket,))
    p.start()

    manager(udp_socket)

if __name__ == '__main__':
    main()


