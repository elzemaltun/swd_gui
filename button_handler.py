import time
import threading

class MessageHandler:
    def __init__(self, serial_handler):
        self.serial_handler = serial_handler
        self.empty_waste_flag = False
        self.fix_flag = False
        self.lock = threading.Lock()
        self.running = True  # Controls the message-sending thread
        threading.Thread(target=self._send_continuous_message, daemon=True).start()

    def _send_continuous_message(self):
        while self.running:
            with self.lock:
                message = f"{{REQ,{int(self.empty_waste_flag)},{int(self.fix_flag)}}}"
                self.serial_handler.send_msg_str(message)
            time.sleep(1)  # Send message every second

    def empty_waste_button_clicked(self):
        with self.lock:
            self.empty_waste_flag = True
        
        # Wait briefly, then set the flag back to false
        threading.Thread(target=self._reset_empty_flag).start()

    def fix_button_clicked(self):
        with self.lock:
            self.fix_flag = True
        
        # Reset the flag back to false after 2 seconds
        threading.Thread(target=self._reset_fix_flag).start()

    def _reset_empty_flag(self):
        time.sleep(2)  # Keep "true" for 2 seconds
        with self.lock:
            self.empty_waste_flag = False

    def _reset_fix_flag(self):
        time.sleep(2)  # Keep "true" for 2 seconds
        with self.lock:
            self.fix_flag = False

    def stop(self):
        """Stop the continuous message-sending thread."""
        self.running = False
