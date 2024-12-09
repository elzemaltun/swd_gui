import customtkinter
import tkinter
import tkinter.messagebox
from threading import Thread
from button_handler import MessageHandler
from serial_handler import SerialHandler
from tkinter.ttk import Progressbar

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # SerialHandler setup
        self.serial_handler = SerialHandler(port="COM8", baudrate=9600)  
        self.message_handler = MessageHandler(self.serial_handler)
        self.serial_handler.start_receiving(self.process_message)

        # configure window
        self.title("Smart Waste Disposal Operational Board")
        self.geometry("700x450") 

        # configure grid layout (4x4)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # navigation menu
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.waste_level_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Waste Level",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.waste_level_button_event)
        self.waste_level_button.grid(row=1, column=0, sticky="ew")

        self.temperature_level_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Temperature Level",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.temperature_level_button_event)
        self.temperature_level_button.grid(row=2, column=0, sticky="ew")

        self.history_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="History",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.history_button_event)
        self.history_button.grid(row=3, column=0, sticky="ew")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)  # Center content horizontally
        self.home_frame.grid_rowconfigure(0, weight=1)  # Add vertical centering
        self.home_frame.grid_rowconfigure(1, weight=1)
        self.home_frame.grid_rowconfigure(2, weight=1)

        self.home_frame_label = customtkinter.CTkLabel(self.home_frame, text="")
        self.home_frame_label.grid(row=0, column=0, padx=20, pady=10)

        self.progress_bar = customtkinter.CTkProgressBar(self.home_frame, orientation="horizontal", width=400, height=25)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=20, sticky="n")
        self.progress_bar.set(0)  # Initialize to 0%
        
        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="EMPTY WASTE", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.message_handler.empty_waste_button_clicked)
        self.home_frame_button_1.grid(row=2, column=0, padx=20, pady=20, sticky="n")
        
        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.second_frame_label = customtkinter.CTkLabel(self.second_frame, text="")
        self.second_frame_label.grid(row=0, column=0, padx=20, pady=10)

        self.progress_bar_temp = customtkinter.CTkProgressBar(self.second_frame, orientation="vertical", height=200, width=30)
        self.progress_bar_temp.grid(row=1, column=0, padx=20, pady=10)
        self.progress_bar_temp.set(0)

        self.second_frame_button_1 = customtkinter.CTkButton(self.second_frame, text="FIX TEMP", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.message_handler.fix_button_clicked)
        self.second_frame_button_1.grid(row=2, column=0, padx=20, pady=10)

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("Waste Level")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.waste_level_button.configure(fg_color=("gray75", "gray25") if name == "Waste Level" else "transparent")
        self.temperature_level_button.configure(fg_color=("gray75", "gray25") if name == "Temperature Level" else "transparent")
        self.history_button.configure(fg_color=("gray75", "gray25") if name == "History" else "transparent")

        # show selected frame
        if name == "Waste Level":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "Temperature Level":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "History":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def waste_level_button_event(self):
        self.select_frame_by_name("Waste Level")

    def temperature_level_button_event(self):
        self.select_frame_by_name("Temperature Level")

    def history_button_event(self):
        self.select_frame_by_name("History")

    def process_message(self, message):
        try:
            # Remove any whitespace and ensure the message is in expected format
            message = message.strip()

            # Check if the message is in curly braces
            if message.startswith("{") and message.endswith("}"):
                # Remove curly braces and split the content
                content = message[1:-1].split(",")

                if len(content) == 5:
                    # Extract the fields based on the expected message format
                    ack, waste_level, temperature, door_state, status_code = content

                    # Update the waste level progress bar
                    waste_level = float(waste_level)
                    if 0 <= waste_level <= 100:
                        self.progress_bar.set(waste_level / 100.0)
                        print(f"Waste Level: {waste_level}%")

                    # Update the temperature progress bar
                    temperature = float(temperature)
                    self.progress_bar_temp.set(temperature / 100.0)
                    print(f"Temperature: {temperature}°C")

                    # Print other message parts for debugging
                    door_state = int(door_state)
                    status_code = int(status_code)
                    print(f"Door State: {door_state}, Status Code: {status_code}")
                else:
                    print("Error: Message does not have the correct number of fields.")
            else:
                print("Error: Message format is incorrect.")
        except Exception as e:
            print(f"Error processing message: {e}")


    def on_closing(self):
        print("Stopping message handler and closing application...")
        self.serial_handler.stop()  # Stop receiving messages
        self.message_handler.stop()  # Stop sending messages
        self.destroy()              # Close the GUI


root = Gui()
root.mainloop()