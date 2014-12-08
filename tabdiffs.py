import json
import time

import to_json

SESSION_STORE_PATH = r"C:\Users\bozak\AppData\Roaming\Mozilla\Firefox\Profiles\0i7y7gr6.default\sessionstore.js"
OUTPUT_PATH = "tab_history.log"


class TabSet:
    def __init__(self, init_set=set()):
        self.items = init_set
        
    def add_diff(self, differences):
        """ Should be given an iterable of strings where the string is expected to start with '-' or '+' """
        for d in differences:
            if d[0] == "-":
                if not d[1:] in self.items:
                    raise RuntimeError("Diff said to remove an item that wasn't there!")
                self.items.remove(d[1:])
            elif d[0] == "+":
                self.items.add(d[1:])
            else:
                raise RuntimeError("Diff string didn't start with '+' or '-'")
    
    def diff_with(self, other_set):
        plus_set = other_set - self.items
        minus_set = self.items - other_set
        output = []
        for addme in plus_set:
            output.append("+"+addme)
        for removeme in minus_set:
            output.append("-"+removeme)
        return output
        
class TabDiffLoader:
    def __init__(self, filename):
        self.filename = filename
    
    def load(self):
        """ Returns the current TabSet """
        touch = open(self.filename, 'a')
        touch.close()
        with open(self.filename, 'r') as f:
            lines = f.readlines()
        start = 0
        ts = TabSet()
        while start < len(lines):
            stop = start
            while stop < len(lines) and lines[stop][0] != "=":
                stop += 1
            ts.add_diff(l[:-1] for l in lines[start:stop])  # remove trailing newline
            start = stop + 1
        return ts
        
class TabDiffWriter:
    def __init__(self, filename):
        self.filename = filename
    
    def write(self, tab_set, other_set):
        """ Writes the differences between the two tab sets to the file """
        lines_to_write = [diff_line+"\n" for diff_line in tab_set.diff_with(other_set)]
        if not len(lines_to_write):
            return
        with open(self.filename, 'a') as f:
            f.write("=%d\n" % time.time())
            f.writelines(lines_to_write)
            
class SessionStoreLoader:
    def __init__(self, path_to_session_store):
        self.path = path_to_session_store
        
    def get_open_tab_ids(self):
        jObj = json.load(open(self.path, 'r'))
        for window in jObj["windows"]:
            for tab in window["tabs"]:
                yield tab["extData"]["treestyletab-id"]
        
def update_with_current_tabs():
    ssl = SessionStoreLoader(SESSION_STORE_PATH)
    curr_tabs = set(ssl.get_open_tab_ids())
    
    loader = TabDiffLoader(OUTPUT_PATH)
    ts = loader.load()
    
    writer = TabDiffWriter(OUTPUT_PATH)
    writer.write(ts, curr_tabs)

def main():
    try:
        print("Running tabdiff...")
        while True:
            update_with_current_tabs()
            to_json.run()
            print("[%s] Finished diffing and converting to JSON" % time.strftime("%H:%M:%S"))
            time.sleep(15)  # the session store is written to every 15 seconds
    except e:
        print(e)
        main()
        
if __name__ == "__main__":
    main()
