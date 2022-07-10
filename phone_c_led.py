#!/usr/bin/env python
# coding=utf-8

# 在ESP8266上搭建HTTP服务器
from machine import Pin
import network
from socket import *
import ntptime
import re



def connect_WIFI():
  sta_if = network.WLAN(network.STA_IF)
  if not sta_if.isconnected():
    print("connecting the network...")
    sta_if.active(1)
    sta_if.connect('Kkkkkk40','15071507')
    while not sta_if.isconnected():
      print("Failure!")
      time.sleep_ms(500)
  print("network ipconfig : ",sta_if.ifconfig())
  return sta_if.ifconfig()[0]
  
def handle_request(client_socket,led):
  #处理浏览器发送的请求，并回送相对应的数据(html, css, js, img...)
  # 1. 接收
  recv_content = client_socket.recv(1024)
  recv_content = recv_content.decode("utf-8")
  print(recv_content)
  print(type(recv_content))
  lines = recv_content.split("\r\n")
  #for line in lines:
  #  print("---")
  #  print(line)
  # 2. 处理请求
    # 提取出/index.html 或者 /
  request_file_path = re.match(r"[^/]+(/[^ ]*)", lines[0]).group(1)

  print("----提出来的请求路径是：----")
  print(request_file_path)
  # 3. 整理要回送的数据
  #response_headers = "HTTP/1.1 200 OK\r\n"
  #response_headers += "Content-Type:text/html;charset=utf-8\r\n"
  #response_headers += "\r\n"
  
  #response_boy = "Hello Vistor!"
  #response = response_headers + response_boy
  # "/"代表浏览器想请求的是主页
  if request_file_path == "/":
    if led.value():
        request_file_path = "led_off.html"
    else:
        request_file_path = "led_on.html"

  try:
      # 以二进制取出对应的文件的数据内容
    with open(request_file_path, "rb") as f:
      content = f.read()
  except Exception as ret:
    # 如果要是有异常，那么就认为：找不到那个对应的文件，此时就应该对浏览器404
    print(ret)
    # 响应头
    response_headers = "HTTP/1.1 404 Not Found\r\n"
    response_headers += "Content-Type:text/html;charset=utf-8\r\n"
    response_headers += "\r\n"
    # 响应体
    response_body = "----sorry，the file you need not found-------"
    response = response_headers + response_body
    # 3.2 给浏览器回送对应的数据
    client_socket.send(response.encode("utf-8"))
  else:
    # 如果要是没有异常，那么就认为：找到了指定的文件，将其数据回送给浏览器即可
    # 响应头
    response_headers = "HTTP/1.1 200 OK\r\n"
    response_headers += "Content-Type:text/html;charset=utf-8\r\n"
    response_headers += "\r\n"
    # 响应体
    response_body = content
    response = response_headers.encode("utf-8") + response_body
    # 3.2 给浏览器回送对应的数据
    client_socket.send(response)
  
  # 4. 给浏览器回送对应的数据
  #client_socket.send(response.encode("utf-8"))
  # 5. 关闭客户端的套接字
  client_socket.close()

  
def tcp_server(led):
  # 1. 创建服务器套接字
  tcp_server_socket = socket(AF_INET,SOCK_STREAM)
  # 2. 释放先前可能占用的端口资源
  tcp_server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
  # 3. 绑定本地信息
  tcp_server_socket.bind(("",80))
  # 4. 建立监听套接字
  tcp_server_socket.listen(128)
  
  while 1:
    # 5. 等待设备连接
    print("Wait for connecting...")
    client_socket, client_info = tcp_server_socket.accept()
    print("client_info",client_info)
    # 6. 为客户端的请求服务
    handle_request(client_socket,led)
  # 7. 关闭套接字
  tcp_server_socket.close()  

#===============================================================#
def main():
  led = Pin(16,Pin.OUT,value=1)
  ip_addr = connect_WIFI()
  print("IP_address is : %s" %ip_addr)
  print("Server_address is : http://%s" %ip_addr)

  tcp_server(led)
  

if __name__ == "__main__":
  main()
  
  
  

