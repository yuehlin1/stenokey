import tkinter as tk
import os
import sys

from manager import CombokeyToggleManager
import keyboard

class GUI(tk.Tk):
    def __init__(self, mng, how_to_hide='ctrl+space'):
        
        self.is_revealed = True
        
        super().__init__()
        self.mng: CombokeyToggleManager = mng
        
        
        # vimium button
        self.vimium_button = tk.Checkbutton(self, text="enable vimium", 
                                              command=mng.toggle_vimium)
        self.vimium_button.pack()
        self.vimium_button.invoke()
        
        # stenokey button
        self.stenokey_button = tk.Checkbutton(self, text="enable stenokey", 
                                              command=mng.toggle_steno)
        self.stenokey_button.pack()
        # self.stenokey_button.invoke() 
        # mng.toggle_steno will be called, 
        # so that once the program started, stenokey is on
        
        tk.Label(self, text='stenokey sensitivity').pack()
        
        self.sensitivity_scale = tk.Scale(self, orient="horizontal", 
                                          command=self.set_sensitivity_with_scale)
        self.sensitivity_scale.set(20)
        self.sensitivity_scale.pack()
        
        # liukey button
        self.liukey_button = tk.Checkbutton(self, text="enable liukey", 
                                              command=mng.toggle_liu)
        self.liukey_button.pack()
        # self.liukey_button.invoke() 
        # mng.toggle_liu will be called
        # so that once the program started, liukey is on
             
        # edit custom combokey button
        self.custom_combokey_button = tk.Button(self, text="custom combokeys", 
                                              command=self.open_text_file)
        self.custom_combokey_button.pack()
    
        # reload button
        self.reload_button = tk.Button(self, text="reload",
                                        command=mng.reload)
        self.reload_button.pack()
    
        self.window_setting()
        
    def set_sensitivity(self):
        try:
            sensitivity_number = int(self.sensitivity_entry.get())
        except ValueError:
            # TODO make it a message window
            print("Sensitivity should be an integer")
            return None
        self.mng.set_sensitivity(sensitivity_number)
        
    def set_sensitivity_with_scale(self, sensitivity_number):
        self.mng.set_sensitivity(int(sensitivity_number))
        # self.sensitivity_label.config(text=f"sensitivity={sensitivity_number}")
        
        
        

    
    def open_text_file(self):
        # TODO pop out a window to choose which file to view
        if sys.platform == 'win32':
            current = os.getcwd()
            os.chdir("..")
            os.chdir("abbrev")
            os.system("start .")
            # os.system("start notepad liu_cqosj.txt")
            os.chdir(current)
        else:
            print("os other than win32 is not supported yet")
    
    def hide(self):
        if self.is_revealed:
            self.toggle_show_gui()
            self.is_revealed = False
    
    def reveal(self):
        if not self.is_revealed:
            self.toggle_show_gui()
            self.is_revealed = True

    def toggle_show_gui(self):
        """change topmost attributes, determinating whether the gui 
        should be always on top of other os apps
        iconify and deiconify do the trick of showing or hiding the app
        When the gui is hidden, steno and liukey should be deactivated
        When the gui is shown again, they should be reactivated
        """
        value_to_set = not self.wm_attributes("-topmost")      
        if value_to_set == 0: # should be the case in the first call
            self.wm_attributes("-topmost", 0)
            self.iconify()
            self.mng.deactivate()
        else:
            self.wm_attributes("-topmost", 1)
            self.deiconify()
            self.mng.reactivate()
        
    def window_setting(self):
        # TODO make it work on other OS
        if sys.platform == 'win32':
            self.attributes('-toolwindow', True)
            self.wm_attributes("-topmost", 1)
        else:
            print("os other than win32 is not supported yet. \
                  The window may not be on topmost")
            
    def toggle_show_gui_hotkey_set(self, hotkey="ctrl+space"):
        keyboard.add_hotkey(hotkey, self.toggle_show_gui)

        

if __name__ == "__main__":
    pass