import json
import time

LOG_FILE = "tab_history.log"
JSON_OUTPUT_FILE = "n_tabs.json"

def sum_change(ls):
    count = 0
    for l in ls:
        if l[0] == '-':
            count -= 1
        elif l[0] == '+':
            count += 1
    return count

def line_sets(lines):
    start = 0
    while start < len(lines):
        stop = start+1
        while stop < len(lines) and lines[stop][0] != "=":
            stop += 1
        yield lines[start:stop]
        start = stop

def run():
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()

    data = []
    prev_count = 0
    for ls in line_sets(lines):
        new_count = prev_count + sum_change(ls[1:])
        data.append([int(ls[0][1:]), new_count])
        prev_count = new_count

    with open(JSON_OUTPUT_FILE, 'w') as f:
        json.dump(data, f, separators=(',', ':'))  # make it compact
        
def main():
    print("Running tabdiff -> JSON converter...")
    while True:
        try:
            run()
            print("[%s] Finished conversion" % time.strftime("%H:%M:%S"))
        except e:
            print(e)
        time.sleep(60)

if __name__ == "__main__":
    main()
