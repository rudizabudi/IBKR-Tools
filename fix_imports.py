import fileinput

def fix_resources_import(file_path):
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            if line.strip() == "import resources_rc":
                print("from . import resources_rc")  # Replace with correct import
            else:
                print(line, end='')  # Preserve other lines

if __name__ == '__main__':
    fix_resources_import("gui/modules/ui_main.py")


