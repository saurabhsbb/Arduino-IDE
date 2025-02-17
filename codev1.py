import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

class ATMega328IDE:
    def __init__(self, root):
        self.root = root
        self.root.title("ATMega328 IDE")
        
        #Code Editor
        self.editor = tk.Text(self.root, wrap='word')
        self.editor.pack(fill='both', expand=True, padx=5, pady=5)
        
        #Toolbar
        toolbar = tk.Frame(self.root)
        toolbar.pack(fill='x')
        
        open_button = tk.Button(toolbar, text="Open", command=self.open_file)
        open_button.pack(side='left', padx=2)
        
        save_button = tk.Button(toolbar, text="Save", command=self.save_file)
        save_button.pack(side='left', padx=2)
        
        compile_button = tk.Button(toolbar, text="Compile", command=self.compile_code)
        compile_button.pack(side='left', padx=2)
        
        upload_button = tk.Button(toolbar, text="Upload", command=self.upload_code)
        upload_button.pack(side='left', padx=2)
    
        self.filename = None
        
    def open_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("C/C++ Files", "*.c *.cpp")])
        if self.filename:
            with open(self.filename, 'r') as file:
                self.editor.delete(1.0, tk.END)
                self.editor.insert(1.0, file.read())
                
    def save_file(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(defaultextension=".c", filetypes=[("C Files", "*.c"), ("C++ Files", "*.cpp")])
        if self.filename:
            with open(self.filename, 'w') as file:
                file.write(self.editor.get(1.0, tk.END))
                
    def compile_code(self):
        if not self.filename:
            messagebox.showerror("Error", "Save the file before compiling")
            return
        output_file = os.path.splitext(self.filename)[0] +".elf"
        try:
            compile_command = ["avr-gcc","-O2", "-mmcu=atmega328p", "-DF_CPU=16000000UL", "-o", output_file, self.filename]
            subprocess.run(compile_command, check=True)
            messagebox.showinfo("Success", f"Compiled Successfully! Output:{output_file}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Compilation failed: {e}")
            
    def upload_code(self):
        if not self.filename:
            messagebox.showerror("Error", "Compile the file before uploading")
            return
            
        elf_file = os.path.splitext(self.filename)[0] + ".elf"
        hex_file = os.path.splitext(self.filename)[0] + ".hex"
        if not os.path.exists(elf_file):
            messagebox.showerror("Error", "Compile the file before uploading")
            return
        try:
            convert_command = ["avr-objcopy", "-O", "ihex", elf_file, hex_file]
            subprocess.run(convert_command, check=True)
            messagebox.showinfo("Success", "Converted successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Conversion failed: {e}")    
          
        try:
            upload_command = ["avrdude", "-v", "-c", "arduino", "-p", "m328p", "-P", "/dev/ttyACM0", "-b", "115200", "-U", f"flash:w:{hex_file}:i"]
            subprocess.run(upload_command, check=True)
            messagebox.showinfo("Success", "Code uploaded successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Upload failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMega328IDE(root)
    root.mainloop()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
                
                
                
                
                
                
                
                
                
                
                
                
                
    
