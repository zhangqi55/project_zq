"""
http sever v2.0
* IO并发处理
* 基本的request解析
* 使用类封装
"""
from socket import *
from select import select
import os


# 将具体http sever功能封装
class HTTPSever:

    # 添加属性
    def __init__(self, sever_address, static_dir):
        self.sever_address = sever_address
        self.static_dir = static_dir
        self.create_socket()
        self.bind()
        self.rlist = []
        self.wlist = []
        self.xlist = []

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # 服务启动函数
    def serve_forever(self):
        self.sockfd.listen(5)
        print('Listen the port: ', self.port)

        # 设置关注的IO
        self.rlist.append(self.sockfd)
        # self.wlist = []变成了全局属性
        # self.xlist = []

        # 循环监听客户端的链接
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sockfd:
                    connfd, addr = r.accept()
                    print("Connect from", addr)
                    # self.handle(connfd)  # 不在这里处理请求
                    self.rlist.append(connfd)
                else:
                    # 处理客户端请求
                    self.handle(r)
                    # data = r.recv(1024)
                    # if not data:
                    #     self.rlist.remove(r)
                    #     r.close()
                    #     continue
                    # print(data)
                    # self.wlist.append(r)
            for w in ws:
                # w.send(b'OK,thanks')
                # self.wlist.remove(w)
                pass
            for x in xs:
                pass

    # 处理连接
    def bind(self):
        # 可以灵活的自己添加属性
        self.sockfd.bind(self.sever_address)
        self.ip = self.sever_address[0]
        self.port = self.sever_address[1]

    # 处理请求
    def handle(self, connfd):
        # 接收http请求
        request = connfd.recv(4096)
        print(request)
        # 防止浏览器异常断开，如果断开的话会返回空
        if not request:
            self.rlist.remove(connfd)  # 最好能把监听的对象删除
            connfd.close()
            return

        # 请求解析
        request_line = request.splitlines()[0].decode()
        print(request_line)
        info = request_line.split(' ')[1]
        print(connfd.getpeername(),':',info)

        # info分为访问网页和其他
        if info == '/' or info[-5:] == '.html':
            self.get_html(connfd, info)
        else:
            self.get_data(connfd, info)
        self.rlist.remove(connfd)
        connfd.close()

    # 处理网页
    def get_html(self,connfd,info):
        # 查看文件列表
        list_fd = os.listdir("./static")  #其实不用遍历了
        # 判断具体要访问谁
        if info == '/':
            dir = self.static_dir + '/' + 'index.html'
            fd = open(dir)
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += fd.read()
            connfd.send(response.encode())
        else:
            dir = self.static_dir + info
            try:
                fd = open(dir)
            except Exception:
                response = "HTTP/1.1 404 Not Found\r\n"
                response += "Content-Type:text/html\r\n"
                response += "\r\n"
                response += "<h1>Sorry...</h1>"
            else:
                response = "HTTP/1.1 200 OK\r\n"
                response += "Content-Type:text/html\r\n"
                response += "\r\n"
                response += fd.read()
            finally:
                connfd.send(response.encode())

    # 处理其他内容，暂时不做处理了。。。下个版本再说吧
    def get_data(self,connfd,info):
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        response += "<h1>Waiting httpserver 3.0...</h1>"
        connfd.send(response.encode())


# 如何使用HTTPServer类
if __name__ == '__main__':
    # 用户自己决定的：地址，内容
    # 通过浏览器可以访问static里面的网页
    sever_addr = ('0.0.0.0', 8000)  # 服务器地址
    static_dir = "./static"  # 网页存放位置


    httpd = HTTPSever(sever_addr, static_dir)  # 生成实例化对象
    httpd.serve_forever()  # 启动服务,等待客户端请求
