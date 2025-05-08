import fileinput
import subprocess
from time import sleep
import os


def compile_pyside_resources(bat_path):
    result = subprocess.run([bat_path], shell=True, check=True, capture_output=True, text=True)
    print("BAT file executed successfully.")
    print("Stdout:", result.stdout)
    print("Stderr:", result.stderr)

def fix_resources_import():
    file_path = os.path.join(os.path.dirname(__file__),'ui_main.py')
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            if line.strip() == "import resources_rc":
                print("from . import resources_rc")  # Replace with correct import
            else:
                print(line, end='')  # Preserve other lines


if __name__ == '__main__':
    #compile_pyside_resources(r"C:\Users\fruhd\OneDrive\CloudDesktop\Python\ibkr_tools\gui\pyside_compile.bat")
    fix_resources_import()
    print('Done')


