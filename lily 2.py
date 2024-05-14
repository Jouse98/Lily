import tkinter as tk
import re

window = tk.Tk()
input_text = tk.Text(window)
input_text.pack()
output = tk.Text(window)
output.config(state=tk.DISABLED)  # Make output non-editable

# Dictionary to store user-defined variables
variables = {}

def findprint():
    output.config(state=tk.NORMAL)  # Enable editing to clear the content
    output.delete("1.0", tk.END)  # Delete current output content
    output.config(state=tk.DISABLED)  # Disable editing again
    text_content = input_text.get("1.0", "end")
    
    global variables  # Access the global variables dictionary
    
    # Process each line of input
    for line in text_content.split('\n'):
        line = line.strip()
        if line.startswith("write"):
            process_write(line)
        elif '=' in line:
            process_assignment(line)

def process_write(line):
    # Extract expression inside write function
    expression = re.search(r'write\((.*?)\)', line).group(1)
    try:
        result = eval(expression, variables)
        output.config(state=tk.NORMAL)  # Enable editing to insert content
        output.insert(tk.END, str(result) + '\n')
        output.config(state=tk.DISABLED)  # Disable editing again
    except Exception as e:
        output.config(state=tk.NORMAL)  # Enable editing to insert content
        output.insert(tk.END, f"Error: {e}\n")
        output.config(state=tk.DISABLED)  # Disable editing again

def process_assignment(line):
    # Split line by '=' to get variable name and value
    variable_name, value = map(str.strip, line.split('='))
    
    try:
        # Try to evaluate value using existing variables
        evaluated_value = eval(value, variables)
    except NameError:
        # If the value contains undefined variables, leave it as is
        evaluated_value = value
    
    variables[variable_name] = evaluated_value

writeBTN = tk.Button(window, text="Write", command=findprint)
writeBTN.pack()
output.pack()

if __name__ == "__main__":
    tk.mainloop()
