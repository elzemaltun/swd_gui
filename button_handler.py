import time
import threading

class MessageHandler:
    def __init__(self, serial_handler):
        self.serial_handler = serial_handler
        self.empty_waste_flag = False
        self.lock = threading.Lock()
        self.running = True  # Controls the message-sending thread
        threading.Thread(target=self._send_continuous_message, daemon=True).start()

    def _send_continuous_message(self):
        """Continuously send the current state of the empty waste message."""
        while self.running:
            with self.lock:
                message = f"empty_waste:{str(self.empty_waste_flag).lower()}"
                self.serial_handler.send_msg_str(message)
            time.sleep(1)  # Send message every second

    def empty_waste_button_clicked(self):
        """Handle the button click to set 'true' temporarily."""
        with self.lock:
            self.empty_waste_flag = True
        
        # Wait briefly, then set the flag back to false
        threading.Thread(target=self._reset_to_false).start()

    def _reset_to_false(self):
        time.sleep(2)  # Keep "true" for 2 seconds
        with self.lock:
            self.empty_waste_flag = False

    def stop(self):
        """Stop the continuous message-sending thread."""
        self.running = False
