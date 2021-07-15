import socket
import threading
import json
from model import extract_feature, get_seresnet50


def main():
    # 创建服务器套接字
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名称
    host = socket.gethostname()
    # 设置一个端口
    port = 12345
    # 将套接字与本地主机和端口绑定
    serversocket.bind((host, port))
    # 设置监听最大连接数
    serversocket.listen(10)
    # 模型创建
    model = get_seresnet50()
    print("等待连接")
    while True:
        # 获取一个客户端连接
        clientsocket, addr = serversocket.accept()
        print("连接地址:%s" % str(addr))
        try:
            t = ServerThreading(model, clientsocket)  # 为每一个请求开启一个处理线程
            t.start()
        except Exception as identifier:
            print(identifier)
        pass
    serversocket.close()
    pass


class ServerThreading(threading.Thread):
    def __init__(self, model, clientsocket, recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        self.model = model
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding
        pass

    def run(self):
        print("开启线程.....")
        try:
            # 接受数据
            msg = ''
            while True:
                # 读取recvsize个字节
                rec = self._socket.recv(self._recvsize)
                # 解码
                msg += rec.decode(self._encoding)
                # 文本接受是否完毕，因为python socket不能自己判断接收数据是否完毕，
                # 所以需要自定义协议标志数据接受完毕
                if msg.strip().endswith('over'):
                    msg = msg[:-4]
                    break
            # 解析json格式的数据
            # 调用神经网络模型处理请求
            res = extract_feature(self.model, msg)
            sendmsg = json.dumps(res)
            print(sendmsg)
            # 发送数据
            self._socket.send(("%s" % sendmsg).encode(self._encoding))

        except Exception as identifier:
            self._socket.send("500".encode(self._encoding))
            print(identifier)
            pass
        finally:
            self._socket.close()
        print("任务结束.....")


if __name__ == "__main__":
    main()
