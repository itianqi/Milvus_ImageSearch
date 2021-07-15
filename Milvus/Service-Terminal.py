import socket
import threading
import json
from model import extract_feature, get_seresnet50


def main():
    # 模型创建
    model = get_seresnet50()
    pass

class ServerThreading(threading.Thread):
    def __init__(self, model, recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        self.model = model
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
