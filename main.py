################################################################
# Main controller for the picrawler, using multiprocessing     #
# to ensure the camera and controller run on separate cores    #
################################################################

import multiprocessing
import time
import connectCamera
import controller

# update as needed 
SERVER_IP = "172.17.10.219"
PORT = 5005

def main():
    print("Starting Multi-Process Controller...")

    # Setup camera process
    # Note: args must be a tuple, so we use (SERVER_IP, PORT)
    camera_process = multiprocessing.Process(
        target=connectCamera.start_camera,
        args=(SERVER_IP, PORT),
        name="CameraProcess"
    )

    # Setup controller process
    controller_process = multiprocessing.Process(
        target=controller.connect_controller,
        name="ControllerProcess"
    )

    # Start the camera first
    camera_process.start()
    
    # Give the camera hardware a moment to warm up before starting movement logic
    print("Waiting for camera to stabilize...")
    time.sleep(7)

    # Start the controller
    controller_process.start()
    print("All systems active.")

    try:
        # Keep the main process alive
        while True:
            # Check if processes are still running; if one crashes, you'll know
            if not camera_process.is_alive() or not controller_process.is_alive():
                print("One of the processes has stopped. Exiting...")
                break
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nManual shutdown initiated...")

    finally:
        # Clean up: Forcefully close processes so they don't hang in the background
        print("Cleaning up processes...")
        camera_process.terminate()
        controller_process.terminate()
        
        # Wait for them to exit cleanly
        camera_process.join()
        controller_process.join()
        print("Done. Goodbye!")

if __name__ == "__main__":
    main()
