import socket
import numpy
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import buffer
import cv2


class Server:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        self.port = 3000

        self.sock.bind(('', self.port))
        self.sock.listen(1)
        self.end = 'halo'.encode()
        self.key = ""

    def handshake(self, client):
        halfkey = client.recv(16)
        print("Received partial key...")
        self.key = get_random_bytes(16)
        print("Built full key...")
        self.key = halfkey + self.key
        print("Sending key...")
        client.sendall(self.key)

    def receiveframes(self, client, buff):
        total_data = []
        data = ''

        fsize = client.recv(1024)
        print(fsize.decode())
        count = 8192

        frame_size = int(fsize.decode)

        while frame_size:
            if frame_size < count:
                count = frame_size

            newbuff = client.recv(count)
            if not data: return None
            data += newbuff
            frame_size -= len(newbuff)

        buff.encrypted_frames.append(data)

        # while True:
        #     data = client.recv(8192)
        #     if self.end in data:
        #         total_data.append(data[:data.find(self.end)])
        #         break
        #     total_data.append(data)
        #     if len(total_data) > 1:
        #         # check if end_of_data was split
        #         last_pair = total_data[-2] + total_data[-1]
        #         if self.end in last_pair:
        #             total_data[-2] = last_pair[:last_pair.find(self.end)]
        #             total_data.pop()
        #             break
        #
        # frame = total_data[0]
        # for part in total_data[1:]:
        #     frame += part
        #
        # print("Frame size: " + str(len(frame)))
        # print(frame)
        # buff.encrypted_frames.append(frame)

    def decryptframes(self, buff, i):
        frame = buff.encrypted_frames[-1]
        nounce = frame[:8]
        print(len(nounce))
        ciphertext = frame[8:]
        cipher = ChaCha20.new(key=self.key, nonce=nounce)
        decoded = cipher.decrypt(ciphertext)
        print("Decoded size " + str(len(decoded)))
        frame2 = cv2.imdecode(numpy.frombuffer(decoded, numpy.uint8), -1)
        outname = "decoded_" + str(i+1) + ".jpg"
        print("Frame2 size: " + str(len(frame2)))
        cv2.imwrite(outname, frame2)
        buff.frames.append(frame2)


if __name__ == "__main__":
    s = Server()
    buff = buffer.Buffer()
    while True:
        print("Waiting for client")
        client, addr = s.sock.accept()
        print("Client connected from " + str(addr))
        s.handshake(client)
        for i in range(150):
            s.receiveframes(client, buff)
            print("Received frame " + str(i+1))
            # print("Writing picture to file...")
            # frame = buff.encrypted_frames[0]
            # print(frame)
            # cv2.imwrite("unencrypted.jpg", frame)
            print("Decrypting frame " + str(i+1))
            s.decryptframes(buff, i)
            client.sendall("halo".encode())
        client.close()
