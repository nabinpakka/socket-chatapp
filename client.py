import socket
import time
import threading

def client(client_name,client_num):
    server_address = 'localhost'
    server_port = 5055

    print("Opening a TCP socket with the server...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_address, server_port))

    client_name = 'Client of ' + client_name
    client.send(bytes(client_name, 'utf-8'))
    time.sleep(1)
    client.send(bytes(str(client_num), 'utf-8'))

    server_name = client.recv(1024).decode()
    server_num = client.recv(1024).decode()
    print("The client name is:",client_name)
    print("The server name is:",server_name)
    print("The client chosen number is:",client_num)
    print("The server chosen number is:",server_num)
    if server_num == '' and server_name == '' and int(client_num) > 100:
        print("The server terminated as client num is greater than 100.")
        return
    server_num = int(server_num)
    client_num = int(client_num)
    Client_Sum = server_num + client_num
    print("Summation of their number on Client:",Client_Sum)
    client.close()

def run_clients_for_threading():
    thread_1= threading.Thread(target=client,args=("Nabin Pakka",10))
    thread_2= threading.Thread(target=client,args=("Nabin Pakka",20))

    thread_1.start()
    thread_2.start()

def run_clients_for_non_thread():
    client_name = input("Enter your name: ")
    client_num = input("Enter a number from 1 to 100: ")
    client(client_name, client_num)

if __name__ == '__main__':
    run_clients_for_non_thread()



