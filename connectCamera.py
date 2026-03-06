import socket
import cv2

################################################################
# Captures data from the USB camera connected to the picrawler #
# and sends it over UDP connection to a host. Call as a thread #
# In Main                                                      #
################################################################

def start_camera(SERVER_IP, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # USB Camera is named 1, not 0
    camera = cv2.VideoCapture(1, cv2.CAP_V4L2)

    if not camera.isOpened():
        print("Cannot open USB camera")
        exit()

    print(f"Sending video stream to {SERVER_IP}:{PORT}...")


    try:
        # infinite loop so just ctrl + C to kill the script. 
        while True:
            ret, frame = camera.read()
            if not ret:
                break

            # resizing to help with latency 
            frame = cv2.resize(frame, (640, 480))

            # encoding as jpg. Adjust the "80" to chnage quality
            result, encoded_img = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            
            if result:
                data = encoded_img.tobytes()
                
                # send to host if under udp limit (should never be over this)
                if len(data) < 65535:
                    client_socket.sendto(data, (SERVER_IP, PORT))
                else:
                    print("Frame too large to send")


    # Close socket when done
    finally:
        camera.release()
        client_socket.close()

