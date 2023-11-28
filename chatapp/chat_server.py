import pickle
import socket
import select # gives OS level monitoring operations for things
from message_model import Message


HEADER_LENGTH = 10
HEADERSIZE=10

IP = "127.0.0.1"
PORT = 5555
# create the socket
# AF_INET == ipv4
# SOCK_STREAM == TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

server_socket.bind((IP, PORT))
server_socket.listen()

socket_list = [server_socket]
clients = {}
usernames = []

print(f"The server is listening for connections on {IP}:{PORT}...")
def receive_message(client_socket, msg_type = "connection"):
    try:
        if msg_type == "connection":
            message_header = client_socket.recv(HEADER_LENGTH)

            # if a client closes a connection gracefully, the header will be empty
            if not len(message_header):
                return False
            message_length = int(message_header.decode("utf-8").strip())
            msg = client_socket.recv(message_length)

            return {"header": message_header, "data": msg}
        else:
            message_header = client_socket.recv(HEADER_LENGTH)

            # if a client closes a connection gracefully, the header will be empty
            if not len(message_header):
                return False
            message_length = int(message_header.decode("utf-8").strip())
            msg = client_socket.recv(message_length)
            msg = pickle.loads(msg)
            print("Message ", msg)

            return {"header": message_header, "data": msg}

    except:
        # if the client closes the connection violently or just connection is lost
        return False


def get_socket_using_username(username):
    for client_socket, data in clients.items():
        if data["data"].decode("utf-8") == username:
            return client_socket

def send_msg_to_client(msg, client_socket):
    msg = bytes(f"{len(msg):<{HEADER_LENGTH}}", 'utf-8') + msg
    client_socket.send(msg)
def handle_personal_msg(data, sender_socket):
    # getting user who sent the message
    user = clients[sender_socket]
    # check if client is available
    if data.receiver not in usernames:
        error = f"User {data.receiver} is not connected to the server."
        error_msg = Message("server", user["data"], error,"error")
        send_msg_to_client(error_msg, sender_socket)
        print("ERROR: ",f"User {data.receiver} is not connected to the server.")
        return

    preview_length = 20
    print(f"Message received from {data.sender} for {data.receiver} with msg {data.msg[:preview_length]}")
    receiver = data.receiver
    receiver_socket = get_socket_using_username(receiver)
    msg = pickle.dumps(data)
    send_msg_to_client(msg, receiver_socket)

if __name__ == '__main__':

    while True:
        # Calls Unix select() system call or Windows select() WinSock call with three parameters:
        #   - rlist - sockets to be monitored for incoming data
        #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
        #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
        # Returns lists:
        #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
        #   - writing - sockets ready for data to be send thru them
        #   - errors  - sockets with some exceptions
        # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
        read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

        # iterate over the read sockets
        for socket in read_sockets:

            # if the socket is server socket, a new connection has arrived
            if socket == server_socket:
                client_socket, client_address = server_socket.accept()

                # getting username which should be sent right away
                user = receive_message(client_socket)

                # the client disconnected before sending username
                if not user:
                    continue

                socket_list.append(client_socket)
                clients[client_socket] = user
                usernames.append(user['data'].decode('utf-8'))
                print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
                client_socket.send(('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'])).encode("utf-8"))
            else:
                # an existing user is sending a message
                message = receive_message(socket, "user")

                if message is False:
                    print('Closed connection from: {}'.format(clients[socket]['data'].decode('utf-8')))
                    socket_list.remove(socket)
                    del clients[socket]
                    continue

                data = message["data"]

                # getting user who sent the message
                user = clients[socket]

                if data.type == "personal":
                    handle_personal_msg(data, socket)
                elif data.type == "group":
                    pass
                elif data.type == "file_transfer":
                    pass

                # # send message to all other users/clients
                # for client in clients:
                #     # not sending message to sender client
                #     if client != socket:
                #         client.send(user['header'] + user['data'] + message['header'] + message['data'])

        # handling sockets which encountered exception
        for socket in exception_sockets:
            socket_list.remove(socket)
            del clients[socket]
