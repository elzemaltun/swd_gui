import serial
import serial.tools.list_ports
import threading

class SerialHandler:
    def __init__(self, port, baudrate, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.buffer = ""  # Used to store incomplete messages
        self.running = True
    
    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Connected to {self.port}")
        except serial.SerialException as e:
            print(e)

    def start_receiving(self, callback):
        def receive_loop():
            while self.running:
                try:
                    if self.ser.in_waiting > 0:
                        message = self.ser.readline().decode('utf-8').strip()
                        callback(message)  # Send the message to the callback
                except Exception as e:
                    print(f"Error reading from serial: {e}")

        self.receiver_thread = threading.Thread(target=receive_loop, daemon=True)
        self.receiver_thread.start()

    def send_msg_str(self, msg):
        if self.ser:
            self.ser.write((msg + "\n").encode('utf-8'))
            print(f"Sent: {msg}")
        else:
            raise OSError("Not connected to Arduino")
    
    def read_update(self):
        if self.ser.in_waiting > 0:  # Use self.ser.in_waiting to check for available data
            data = self.ser.readline().decode('utf-8', errors='replace').strip()
            print(f"Received: {data}")
        return None  # No complete message yet
    
    def stop(self):
        self.running = False
        if self.ser.is_open:
            self.ser.close()    
    
    def close(self):
        if self.ser:
            self.ser.close()
    