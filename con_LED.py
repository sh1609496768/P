from machine import Pin
import network
from socket import *
import ntptime
import time

def creat_udp_socket():
  # 1. 创建一个UDP套接字对象
  udp_socket = socket(AF_INET, SOCK_DGRAM)
  # 2. 为ESP8266绑定一个固定的ip地址和端口，方便其它设备找到ESP8266
  udp_socket.bind(("0.0.0.0",626))
  return udp_socket
  
def Test_of_connecting(udp_socket):
  dest_addr = ('192.168.138.142', 8080)
  send_data = "Communication is normal!"
  udp_socket.sendto(send_data.encode('utf-8'), dest_addr)
  

def main():
  led = Pin(16,Pin.OUT,value=1)
  udp_socket = creat_udp_socket()
  Test_of_connecting(udp_socket)
  
  while 1:
    # udp_socket.recvfrom(1024)的返回值为一个元组，可以拆包
    recv_data, sender_info = udp_socket.recvfrom(1024)
    # 解码
    recv_data = recv_data.decode("utf-8")
    print("The message from %s is: %r" %(sender_info,recv_data))

    if recv_data == 'light on':
      led.value(0)
    elif recv_data == 'light off':
      led.value(1)

  udp_socket.close()


if __name__ == "__main__":
  main()
