import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import Main
import sys
class App:
    def __init__(gui, root):
        gui.root = root
        gui.root.title("Nate's Mesh Reducer")
        
        gui.output_terminal = tk.Text(root, wrap=tk.WORD, height=15)
        gui.output_terminal.pack(fill="both", padx=10, pady=10)  
        
        gui.import_frame = ttk.Frame(root)
        gui.import_frame.pack(anchor="w", padx=10, pady=5)

        gui.import_file_button = ttk.Button(gui.import_frame, text="Select File", command=gui.import_file)
        gui.import_file_button.pack(side="left", padx=10, pady=5)

        gui.import_folder_button = ttk.Button(gui.import_frame, text="Select Folder", command=gui.import_folder)
        gui.import_folder_button.pack(side="left", padx=10, pady=5)

        gui.target_frame = ttk.Frame(root)
        gui.target_frame.pack(anchor="w", padx=10, pady=5)

        gui.target_label = ttk.Label(gui.target_frame, text="Target face number:")
        gui.target_label.pack(side="left")

        gui.target_var = tk.StringVar()
        gui.target_entry = ttk.Entry(gui.target_frame, textvariable=gui.target_var)
        gui.target_entry.pack(side="left")
        gui.target_entry.insert(0, "500000")  # Placeholder

        gui.smoothing_var = tk.IntVar()
        gui.smoothing_checkbox = ttk.Checkbutton(root, text="Smoothing", variable=gui.smoothing_var, command=gui.toggle_smoothing)
        gui.smoothing_checkbox.pack(anchor="w", padx=10, pady=5)

        gui.smoothing_frame = ttk.Frame(root)
        gui.smoothing_frame.pack(anchor="w", padx=10, pady=5)
        gui.smoothing_frame.pack_forget()

        gui.iterations_label = ttk.Label(gui.smoothing_frame, text="Iterations:")
        gui.iterations_label.pack(anchor="w", padx=10, pady=(10, 0))

        gui.iterations_var = tk.StringVar()
        gui.iterations_entry = ttk.Entry(gui.smoothing_frame, textvariable=gui.iterations_var)
        gui.iterations_entry.pack(fill="x", padx=10, pady=5)
        gui.iterations_entry.insert(0, "10")  # Placeholder

        gui.alpha_label = ttk.Label(gui.smoothing_frame, text="Alpha:")
        gui.alpha_label.pack(anchor="w", padx=10, pady=(10, 0))

        gui.alpha_var = tk.StringVar()
        gui.alpha_entry = ttk.Entry(gui.smoothing_frame, textvariable=gui.alpha_var)
        gui.alpha_entry.pack(fill="x", padx=10, pady=5)
        gui.alpha_entry.insert(0, "0.5")  # Placeholder

        gui.advanced_var = tk.IntVar()
        gui.advanced_checkbox = ttk.Checkbutton(root, text="Show advanced options", variable=gui.advanced_var, command=gui.toggle_advanced)
        gui.advanced_checkbox.pack(anchor="w", padx=10, pady=5)

        gui.advanced_frame = ttk.Frame(root)
        gui.advanced_frame.pack(anchor="w", padx=10, pady=5)
        gui.advanced_frame.pack_forget()

        gui.aggressiveness_label = ttk.Label(gui.advanced_frame, text="Aggressiveness:")
        gui.aggressiveness_label.pack(anchor="w", padx=10, pady=(10, 0))

        gui.aggressiveness_var = tk.StringVar()
        gui.aggressiveness_entry = ttk.Entry(gui.advanced_frame, textvariable=gui.aggressiveness_var)
        gui.aggressiveness_entry.pack(fill="x", padx=10, pady=5)
        gui.aggressiveness_entry.insert(0, "10")  # Placeholder

        gui.preserve_border_var = tk.IntVar(value=1)  # Checked by default
        gui.preserve_border_checkbox = ttk.Checkbutton(gui.advanced_frame, text="Preserve Border", variable=gui.preserve_border_var)
        gui.preserve_border_checkbox.pack(anchor="w", padx=10, pady=5)

        gui.lossless_var = tk.IntVar()
        gui.lossless_checkbox = ttk.Checkbutton(gui.advanced_frame, text="Lossless", variable=gui.lossless_var)
        gui.lossless_checkbox.pack(anchor="w", padx=10, pady=(5, 10))

        gui.run_button = ttk.Button(root, text="Run", command=lambda:[gui.runterminal(), Main.runtime(gui)])
        gui.run_button.pack(side="right", padx=10, pady=5)

        # Variables to store user inputs
        gui.selected_file_folder = tk.StringVar()
        gui.aggressiveness_value = tk.StringVar()
        gui.iterations_value = tk.StringVar()  # For smoothing iterations
        gui.alpha_value = tk.StringVar()  # For smoothing alpha
        
    def import_file(gui):
        file_path = filedialog.askopenfilename()
        gui.selected_file_folder.set(file_path)
        gui.add_output(f"Selected File: {file_path}")

    def import_folder(gui):
        folder_path = filedialog.askdirectory()
        gui.selected_file_folder.set(folder_path)
        gui.add_output(f"Selected Folder: {folder_path}")

    def toggle_advanced(gui):
        if gui.advanced_var.get():
            gui.advanced_frame.pack(anchor="w", padx=10, pady=5)
        else:
            gui.advanced_frame.pack_forget()

    def toggle_smoothing(gui):
        if gui.smoothing_var.get():
            gui.smoothing_frame.pack(anchor="w", padx=10, pady=5)
        else:
            gui.smoothing_frame.pack_forget()
    
    def redirect_output(self):
        self.stdout_orig = sys.stdout  # Store the original stdout stream
        sys.stdout = self  # Redirect stdout to this object
    
    def write(self, message):
        self.output_terminal.insert(tk.END, message)  # Append the message to the Text widget
        self.output_terminal.see(tk.END)  # Scroll to the end of the Text widget

    def restore_output(self):
        sys.stdout = self.stdout_orig  # Restore the original stdout stream

    def runterminal(gui):

        aggressiveness_value = gui.aggressiveness_var.get()  # Corrected this line
        target_value = gui.target_var.get()  # Corrected this line
        selected_file_folder = gui.selected_file_folder.get()
        iterations_value = gui.iterations_var.get()  # Corrected this line
        alpha_value = gui.alpha_var.get()  # Corrected this line
        
        preserve_border_value = "Yes" if gui.preserve_border_var.get() == 1 else "No"
        lossless_value = "Yes" if gui.lossless_var.get() == 1 else "No"
        smoothing_value = "Yes" if gui.smoothing_var.get() == 1 else "No"

        output_message = f"Running with the following inputs:\n"
        output_message += f"Aggressiveness: {aggressiveness_value}\n"
        output_message += f"Target face number: {target_value}\n"
        output_message += f"Selected File/Folder: {selected_file_folder}\n"
        output_message += f"Preserve Border: {preserve_border_value}\n"
        output_message += f"Lossless: {lossless_value}\n"
        output_message += f"Smoothing: {smoothing_value}\n"
        if smoothing_value == "Yes":
            output_message += f"Smoothing Iterations: {iterations_value}\n"
            output_message += f"Smoothing Alpha: {alpha_value}\n"

        gui.add_output(output_message)
        gui.redirect_output()
    def add_output(gui, message):
        gui.output_terminal.insert(tk.END, message + "\n")
        gui.output_terminal.see(tk.END)
def main():
    root = tk.Tk()
    gui = App(root)
    root.mainloop()
  
if __name__ == "__main__":
    main()