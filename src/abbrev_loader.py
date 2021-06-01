import os


class AbbrevLoader():
    "load abbrev files in the directory called abbrev"
    # TODO decide whether stock every word into a dictionary(memory burden), 
    # or return an iterable(I/O cost)
    
    def __init__(self):
        self.liu_dict = dict()
        self.steno_dict = dict()

    def load(self, file_dir='..\\abbrev'):
        current_dir = os.getcwd()
        os.chdir(file_dir)
        files = os.listdir()
        for file in files:
            if file.startswith("steno"):
                abbrev_type = "steno"
            elif file.startswith("liu"):
                abbrev_type = "liu"
            else:
               print("file abbrev_type not understood")
               continue
            with open(file, "r", encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith("#"): # this is a comment line, ignore it.
                        continue
                    self.add_abbrev(line, abbrev_type)
        os.chdir(current_dir)
    
    def add_abbrev(self, line:str, abbrev_type):
        line = line.replace('\n', '')
        pos = line.find(' ')
        if pos == -1:
            return None
        abbrev = line[:pos]
        full_form = line[pos+1:]
        abbrev = abbrev.lower()
        if abbrev_type == "steno":
            abbrev = ''.join(sorted(list(abbrev)))
            self.steno_dict[abbrev] = full_form
        elif abbrev_type == "liu":
            self.liu_dict[abbrev] = full_form
        else:
            raise Exception("abbrev type not understood")
