import tkinter as tk


def submit_pin():
    pin = pin_entry.get()
    # Perform the necessary actions with the PIN, such as sending it to EPFO

    # Clear the entry field after submitting
    pin_entry.delete(0, tk.END)


# Create the main application window
window = tk.Tk()
window.title("EPFO Digital PIN Entry")

# Create a label
label = tk.Label(window, text="12345678")
label.pack()

# Create an entry field
pin_entry = tk.Entry(window, show="*")
pin_entry.pack()

# Create a submit button
submit_button = tk.Button(window, text="Submit", command=submit_pin)
submit_button.pack()

# Run the application
window.mainloop()
