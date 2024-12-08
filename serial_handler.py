import serial
import serial.tools.list_ports

class SerialHandler:
    def __init__(self, port, baudrate, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.buffer = ""  # Used to store incomplete messages
    
    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Connected to {self.port}")
        except serial.SerialException as e:
            print(e)

    def send_msg(self, msg):
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
    
    def close(self):
        if self.ser:
            self.ser.close()
    