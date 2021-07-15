package top.maolaoe.imgsearch.service;

import org.springframework.stereotype.Service;

import java.io.*;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;

/**
* 通过socket调用python获得图片的特征向量
*/
@Service
public class FeatureService {
private String HOST = "192.168.1.103";
private final int PORT = 12345;

public List<Float> remoteCall(String path){
// 访问服务进程的套接字
//        System.out.println("调用远程接口:host=>"+HOST+",port=>"+PORT);
try(Socket socket = new Socket(HOST, PORT)) {
// 初始化套接字，设置访问服务的主机和进程端口号，HOST是访问python进程的主机名称，可以是IP地址或者域名，PORT是python进程绑定的端口号
// 获取输出流对象
OutputStream os = socket.getOutputStream();
PrintStream out = new PrintStream(os);
// 发送内容
out.print(path);
// 告诉服务进程，内容发送完毕，可以开始处理
out.print("over");


// 获取服务进程的输入流
InputStream is = socket.getInputStream();
BufferedReader br = new BufferedReader(new InputStreamReader(is,"utf-8"));
String tmp = null;
StringBuilder sb = new StringBuilder();
// 读取内容
while((tmp=br.readLine())!=null)
sb.append(tmp).append('\n');
// 解析结果
tmp = sb.toString().substring(1, sb.length()-2);
String[] split = tmp.split(",");
List<Float> list = new ArrayList<Float>(split.length);
for (int i = 0; i < split.length; i++) {
    list.add(Float.valueOf(split[i]));
split[i] = null;
}
//            System.out.println(list);
//            System.out.println(list.size());
return list;
} catch (IOException e) {
e.printStackTrace();
}
return null;
}

public static void main(String[] args) throws IOException {
FeatureService featureService = new FeatureService();
featureService.remoteCall("E:\\data\\tx.jpg");

}

}
