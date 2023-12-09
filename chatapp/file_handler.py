import os
import tqdm

TRANSFER_SIZE = 1024
class FileHandler:
    def __init__(self, socket):
        self.socket = socket
    def send_file(self, filepath, receiver_socket=None):
        filesize = os.path.getsize(filepath)

        if receiver_socket is None:
            socket = self.socket
        else:
            socket = receiver_socket
        progress = tqdm.tqdm(range(filesize), f"Sending {filepath}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filepath, 'rb') as file:
            # Read and send the file data in chunks
            data = file.read(TRANSFER_SIZE)
            datasize = len(data)
            while data:
                if(datasize > filesize):
                    break
                socket.send(data)
                data = file.read(TRANSFER_SIZE)
                datasize += len(data)
                progress.update(len(data))
        print("File sent successfully.")

    def receive_and_save_file(self, filepath, filesize):
        progress = tqdm.tqdm(range(filesize), f"Receiving {filepath}", unit="B", unit_scale=True, unit_divisor=1024)
        # Receive the file data
        with open(filepath, 'wb') as file:
            data = self.socket.recv(TRANSFER_SIZE)
            while data:
                file.write(data)
                data = self.socket.recv(TRANSFER_SIZE)
                progress.update(len(data))
        print("File received successfully.")