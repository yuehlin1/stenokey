import tkinter as tk
import os

class App(tk.Tk):
    def __init__(self, sm):
        super().__init__()
        self.sm = sm
        self.stenokey_on = tk.BooleanVar()
        
        
        # stenokey button
        self.stenokey_button = tk.Checkbutton(self, text='enable stenokey', 
                       variable=self.stenokey_on, onvalue=True, offvalue=False, 
                       command=self.enable_steno)
        self.stenokey_button.pack()
        self.stenokey_button.invoke() # so that once the program started, stenokey is on
        
        # view stenokey button
        # self.view_stenokey_button = tk.Button(self, text="view stenokeys", 
        #                                       command=self.open_text_file)
        # self.view_stenokey_button.pack()
        
        # edit custom stenokey button
        self.custom_stenokey_button = tk.Button(self, text="custom stenokeys", 
                                              command=self.open_text_file)
        self.custom_stenokey_button.pack()
    
        # reload button
        self.reload_button = tk.Button(self, text="reload",
                                        command=self.reload)
        self.reload_button.pack()
    
        self.window_setting()
        
    def reload(self):
        self.sm.load()
        
    def enable_steno(self):
        if self.stenokey_on.get():
            self.sm.hook()
        else:
            self.sm.unhook()
    
    def open_text_file(self):
        # TODO pop out a window to choose which file to view
        current = os.getcwd()
        os.chdir("..")
        os.chdir("abbrev")
        os.system("start notepad steno_custom.txt")
        os.chdir(current)
        
        
    def window_setting(self):
        # TODO make it work on other OS
        self.attributes('-toolwindow', True)
        self.wm_attributes("-topmost", 1)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()