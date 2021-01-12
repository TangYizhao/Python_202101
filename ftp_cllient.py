"""

1.技术分析
    * 并发模型 (多进程，多线程）
    * 网络传输方法 ：tcp

2.功能分析（封装）

    搭建网络架构
    查看文件列表



    上传文件
    下载文件
    退出

3. 通信协议设计
                请求类型    请求参量
    查看文件列表  L
    上传文件     P
    下载文件     G
    退出        Q

4.功能具体分析
    搭建网络架构
    查看文件列表
    上传文件
    下载文件
    退出

5.具体细节优化

"""

from socket import *
from time import sleep
import sys

class FTPclient():
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b"L")

        data = self.sockfd.recv(128).decode()
        if data == "YES":
            data = self.sockfd.recv(8192)
            print(data.decode())
        else:
            print("获取文件列表失败")

    def get_file(self, filename):
        data = "G "+filename
        self.sockfd.send(data.encode())
        data = self.sockfd.recv(128).decode()
        if data == "YES":
            f = open(filename,"wb")
            while True:
                data = self.sockfd.recv(1024)
                if data ==b"##":
                    break
                f.write(data)
            f.close()
        else:
            print("没有这个文件")

    def do_put(self, filename):
        # 本地判断，看是否文件存在
        try:
            f = open(filename, 'rb')
        except:
            print("要上传的文件不存在")
            return
        # 提取真正的文件名 (原来的filename可能包含路径 ../xxxx.jpg)
        filename = filename.split('/')[-1]

        data = "P " + filename
        self.sockfd.send(data.encode())  # 发送请求
        # 等待回复
        result = self.sockfd.recv(128).decode()
        if result == 'YES':
            # 读取文件发送
            while True:
                data = f.read(1024)
                if not data:
                    sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print("该文件存在")

    # def put_file(self, filename):
    #     try:
    #         f = open(filename,"rb")
    #     except:
    #         print("要上传的文件不存在！")
    #         return
    #
    #     filename = filename.split('/')[-1]
    #
    #     data = "P " + filename
    #     self.sockfd.send(data.encode())
    #     data = self.sockfd.recv(128).decode()
    #     if data == "YES":
    #
    #         while True:
    #             data = f.read(1024)
    #             if not data:
    #                 sleep(0.1)
    #                 self.sockfd.send(b"##")
    #                 break
    #             self.sockfd.send(data)
    #         f.close()
    #
    #     else:
    #         print("文件已存在")

    def do_quit(self):
        self.sockfd.send(b"E")
        self.sockfd.close()
        sys.exit("谢谢使用")



ADDR = ("127.0.0.1",8888)

def main():
    s = socket()
    s.connect(ADDR)
    ftp = FTPclient(s)
    try:
        while True:
            print("=============命令选项=============")
            print("=========      list     =========")
            print("=========    get file   =========")
            print("=========    put file   =========")
            print("=========      quit     =========")
            print("==================================")

            cmd = input("请输入命令：")
            if cmd == "list":
                ftp.do_list()
            elif cmd[:3] == "get":
                filename = cmd.split(" ")[-1]
                ftp.get_file(filename)
            elif cmd[:3] == "put":
                filename = cmd.split(" ")[-1]
                ftp.do_put(filename)
            elif cmd == "quit":
                ftp.do_quit()
            else:
                print("请输入正确信息！")
    except KeyboardInterrupt:
        print("谢谢使用")
        return



if __name__ == '__main__':
    main()























