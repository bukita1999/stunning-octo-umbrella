#-*- coding: utf-8 -*-
import os
import sys
import socketserver
import csv


class CommandListener(socketserver.BaseRequestHandler):
    
    def handle(self): 
        
        connection = self.request
        connection.sendall('Welcome'.encode('ascii'))
        while True: 
            data = connection.recv(1024).decode('ascii')
            if data == 'exit': 
                print('Ask for out {0}'.format(self.client_address))
            else: 
                print('收到来自{0}的客户端向你发来信息:{1}'.format(self.client_address, data))
                #connection.sendall(('Receive your message {0}'.format(data)).encode('ascii'))
                csvSearcher = CsvSearcher('data.csv')
                replydata = csvSearcher.readValueFromCsv(data)
                print(replydata)
                connection.sendall(replydata.encode('ascii'))
    
    
class CsvSearcher:
    def __init__(self, filename):
        self.filename = filename
        self.key = None 
        self.value = None 
    
    def readValueFromCsv(self, key): 
        self.key = key 
        
        with open(self.filename, mode='r',encoding='utf-8-sig') as input: 
            reader = csv.reader(input)
            dict_from_csv = {rows[0]:rows[1] for rows in reader}
        
        print(dict_from_csv)
        try:
            self.value = dict_from_csv[self.key]
        except KeyError:
            self.value = 'No Value'
        finally:
            return self.value
    
 

if __name__ == '__main__':
    # 主函数入口
    host = '127.0.0.1'
    port = 10086
    listener = socketserver.ThreadingTCPServer((host, port), CommandListener)
    listener.serve_forever()
    #csvSearcher = CsvSearcher('data.csv')
    #print(csvSearcher.readValueFromCsv('4'))
    print('over')