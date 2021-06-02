import tkinter as tk
import os
import sys

class App(tk.Tk):
    def __init__(self, sm, lm):
        super().__init__()
        self.sm = sm
        self.lm = lm
        self.stenokey_on = tk.BooleanVar()
        self.liukey_on = tk.BooleanVar()
        
        
        # stenokey button
        self.stenokey_button = tk.Checkbutton(self, text='enable stenokey', 
                       variable=self.stenokey_on, onvalue=True, offvalue=False, 
                       command=self.enable_steno)
        self.stenokey_button.pack()
        self.stenokey_button.invoke() # so that once the program started, stenokey is on
        
        # liukey button
        self.liukey_button = tk.Checkbutton(self, text='enable liukey', 
                       variable=self.liukey_on, onvalue=True, offvalue=False, 
                       command=self.enable_liu)
        self.liukey_button.pack()
        self.liukey_button.invoke() # so that once the program started, liukey is on
        
        # view stenokey button
        # self.view_stenokey_button = tk.Button(self, text="view stenokeys", 
        #                                       command=self.open_text_file)
        # self.view_stenokey_button.pack()
        
        # edit custom combokey button
        self.custom_combokey_button = tk.Button(self, text="custom combokeys", 
                                              command=self.open_text_file)
        self.custom_combokey_button.pack()
    
        # reload button
        self.reload_button = tk.Button(self, text="reload",
                                        command=self.reload)
        self.reload_button.pack()
    
        self.window_setting()
        
    def reload(self):
        self.sm.load()
        self.lm.load()
        
    def enable_steno(self):
        if self.stenokey_on.get():
            self.sm.hook()
        else:
            self.sm.unhook()
            
    def enable_liu(self):
        if self.liukey_on.get():
            self.lm.hook()
        else:
            self.lm.unhook()
    
    def open_text_file(self):
        # TODO pop out a window to choose which file to view
        if sys.platform == 'win32':
            current = os.getcwd()
            os.chdir("..")
            os.chdir("abbrev")
            os.system("start notepad steno_custom.txt")
            # os.system("start notepad liu_cqosj.txt")
            os.chdir(current)
        else:
            print("os other than win32 is not supported yet")
        
        
    def window_setting(self):
        # TODO make it work on other OS
        if sys.platform == 'win32':
            self.attributes('-toolwindow', True)
            self.wm_attributes("-topmost", 1)
        else:
            print("os other than win32 is not supported yet. \
                  The window may not be on topmost")
        

if __name__ == "__main__":
    pass