import os
import re
from string import Template
from pathlib import Path

def run(): 
    current_dir = os.path.dirname(__file__)
    day = max([int(d.replace("day", "")) for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d)) and re.match("^day[0-9]+$", d)]) + 1
    day_dir = os.path.join(current_dir, f"day{day}")    
    os.mkdir(day_dir)
    create_from_template(day, day_dir, "day.py.template", f"day{day}.py")
    create_from_template(day, day_dir, "day_test.py.template", f"day{day}_test.py")
    Path(os.path.join(day_dir, '__init__.py')).touch()
    

def create_from_template(day, dest_dir, src_file, dest_file):
    current_dir = os.path.dirname(__file__)    
    with open(os.path.join(current_dir, "day_template", src_file)) as f:
        template = Template(f.read())
        res = template.substitute({'day': day})
        with open(os.path.join(dest_dir, dest_file), 'w') as out:
            out.write(res)

if __name__ == '__main__':    
    run()