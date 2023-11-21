import random
import socket
import time
import threading
import random

def client_thread(client,thread_number):
    client_name = client.recv(1024).decode()
    print(client_name)
    client_num = client.recv(1024).decode()
    client_num = int(client_num)

    print("Starting the client in thread: " + str(thread_number) + "\n\n")
    
    if client_num>100:
        print("Client chosen number is out of range")
        print("Terminate the connection")
        client.close()
        
    else:
        print("The client name is:",client_name)
        print("The server name is:",server_name)

        server_num= random.randint(1,100)
        print("The server chosen number is:",server_num)
        print("The client chosen number is:",client_num)
        Server_Sum = server_num+client_num
        print("Summation of their number on Server:",Server_Sum)
        client.send(bytes(server_name, 'utf-8'))
        time.sleep(1)
        client.send(bytes(str(server_num), 'utf-8'))
        client.close()
    pass

def start_server_with_thread():
    while True:

        client, address = server.accept()
        _client_thread = threading.Thread(target=client_thread,args=(client,address))
        _client_thread.start()

def start_server_without_thread():
        while True:
            client, address = server.accept()

            client_name = client.recv(1024).decode()
            print(client_name)
            client_num = client.recv(1024).decode()
            client_num = int(client_num)

            if client_num>100:
                print("Client chosen number is out of range")
                print("Terminating the connection...")
                client.close()
            else:
                print("The client name is:",client_name)
                print("The server name is:",server_name)

                server_num= random.randint(1, 100)
                print("The server chosen number is:",server_num)
                print("The client chosen number is:",client_num)

                Server_Sum = server_num+client_num
                print("Sum of client and server number on Server:",Server_Sum)
                client.send(bytes(server_name, 'utf-8'))
                time.sleep(1)
                client.send(bytes(str(server_num), 'utf-8'))
                client.close()


if __name__ == '__main__':
    server_address = 'localhost'
    server_port = 5055
    server_name = 'Server of Nabin Pakka'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_address, server_port))
    server.listen(5)
    print("Waiting for connections...")
    start_server_without_thread()