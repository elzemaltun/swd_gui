from serial_handler import SerialHandler
import time

def main():
    port = 'COM8'
    serial_handler = SerialHandler(port, baudrate=9600)

    try:
        serial_handler.connect()

        while True:
    
            # Send a command to Arduino
            serial_handler.send_msg("EMPTY")

            time.sleep(0.5)

            # Read messages from Arduino
            messages = serial_handler.read_update()
            for message in messages:
                print(f"Received: {message}")
            else:
                print("No message received")

            time.sleep(1.0)
            
    finally:
        serial_handler.close()

if __name__ == "__main__":
    main()
