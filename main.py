################################################################
# Main controller for the picrawler, make sure to run each     #
# file as a thread so they dont block eachother                #
################################################################

import threading
import time
import connectCamera

# update as needed 
SERVER_IP = "172.17.10.203"
PORT = 5005

def main():

    # setup camera thread
    camera_thread = threading.Thread(
        target=connectCamera.start_camera,
        args=(SERVER_IP, PORT),
        # Kills this thread when we quit the main process
        daemon=True
    )

    # setup controller thread



    # start all threads
    camera_thread.start()


    try:
        # keeping the main process alive
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Exiting Main Process")






if __name__ == "__main__":
    main()
