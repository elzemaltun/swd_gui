from serial_handler import SerialHandler
import time

def main():
    port = 'COM8'
    serial_handler = SerialHandler(port, baudrate=9600)

    try:
        while True:
            if serial_handler.ser.in_waiting > 0:
                serial_handler.send_msg("this is python")
                time.sleep(1)
                serial_handler.read_update()
                time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        serial_handler.close()

if __name__ == "__main__":
    main()
