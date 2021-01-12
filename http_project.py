import re
from socket import *
from  select import select


class HTTPServer:
    def __init__(self, host = "0.0.0.0",port = 8000, html=None):
        self.host = host
        self.port = port
        self.html = html
        self.creat_socket()
        self.bind()
        self.rlist = []
        self.wlist = []
        self.xlist = []

    def creat_socket(self):
        self.sockfd = socket()
        self.sockfd.setblocking(False)

    def bind(self):
        self.address = (self.host,self.port)
        self.sockfd.bind(self.address)

    def start(self):
        self.sockfd.listen(3)
        print("Listen the port:",self.port)

        self.rlist.append(self.sockfd)
        while True:
            rl, wl, xl = select(self.rlist, self.wlist, self.xlist)
            for r in rl:
                if r is self.sockfd:
                    connfd,addr = r.accept()
                    print("Connect from:", addr)
                    connfd.setblocking(False)
                    self.rlist.append(connfd)

                else:
                    self.handle(r)


    def handle(self, connfd):
        request = connfd.recv(1024).decode()
        pattern = r"[A-Z]+\s+(/\S*)"
        try :
            info = re.match(pattern,request).group(1)
        except:
            self.rlist.remove(connfd)
            connfd.close()
            return
        else:
            self.get_html(connfd,info)

    def get_html(self, connfd, info):
        if info =="/":
            filename = self.html + "/index.html"
        else:
            filename = self.html + info
        try:
            f = open(filename,"rb")
        except:
            response_headers = "HTTP/1.1 404 NOT FOUND\r\n"
            response_headers += "Content-Type:text/html\r\n"
            response_headers += "\r\n"
            response_content = "<h1>Sorry...PAGE NOT FOUND</h1>"
            response = (response_headers + response_content).encode()
        else:
            response_content = f.read()

            response_headers = "HTTP/1.1 200 OK\r\n"
            response_headers += "Content-Type:text/html\r\n"
            response_headers += "Content-Length:%d\r\n"%len(response_content)
            response_headers += "\r\n"

            response = response_headers.encode() + response_content
            f.close()

        # print("开始发送...")
        connfd.send(response)
        # print("发送完成...")

if __name__ == '__main__':
    """
    通过HTTPServer类快速搭建服务
    展示网页
    """
    host = "0.0.0.0"
    port = 8000
    dir = "./static"


    #实例化对象
    httpd = HTTPServer(host = host,port = port,html = dir)

    #调用方法启动服务
    httpd.start()

