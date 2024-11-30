from serial_handler import SerialHandler


try:
    port = SerialHandler.find_arduino_port()
    print(f"Arduino detected on port: {port}")

    serial_handler = SerialHandler(port, 115200)
    state = serial_handler.receive_update()
    print(f"State received: {state}")
    
    serial_handler.close()
except OSError as e:
    print(e)