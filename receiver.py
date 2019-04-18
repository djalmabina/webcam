import socket
import numpy as np
import cv2 as cv


addr = ("127.0.0.1", 65534)
buf = 512
width = 640
height = 480
code = 'start'
l = width * height * 3

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    while True:
        byte_frame = bytearray()
        saw_start = False
        while (len(byte_frame) < l):
            data, _ = s.recvfrom(buf)
            if saw_start:
                byte_frame.extend(data)
            else:
                loc = data.find(code.encode('utf-8'))
                if loc == 0:
                    saw_start = True

        frame = np.frombuffer(
            byte_frame, dtype=np.uint8).reshape(height, width, 3)

        cv.imshow('recv', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            s.close()
            break

    cv.destroyAllWindows()
