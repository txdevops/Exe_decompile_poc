import glob, os, time, difflib, re
import pandas as pd
from subprocess import check_output


def exe_scanner_creation(filename):
    global exe_files_list
    exe_files_list = []
    if glob.glob("dist/{}.exe".format(filename)):
        for fn in glob.glob("dist/{}.exe".format(filename)):
            exe_files_list.append(fn.split('\\')[-1])
    else:
        print("\n\n there is no exe file in the folder \n\n  \
        So we're creating executable for {}".format(filename + ".py"))
        check_output("pyinstaller --onefile {}".format(filename + ".py"), shell=True)
        exe_scanner_creation(filename)
        

def extraction(filename):
    exe_scanner_creation(filename)
    global exe_file_1
    exe_file_1 = exe_files_list[0]
    os.system('python pyinstxtractor.py {}'.format(exe_file_1))

def uncompile_exe():
    up_exe_file_1 = exe_file_1.split("/")[-1]
    pyc_file_location = str(up_exe_file_1) + "_" + "extracted/{}".format(up_exe_file_1.replace(".exe", ".pyc"))
    print("Uncompyle Successful for {}".format(up_exe_file_1))
    os.system("uncompyle6 {} > {}".format(pyc_file_location, "uncompiled" + "_" + up_exe_file_1.replace(".exe", ".py")))

def diff_fn(file1, file2):  
    with open(file1) as file_1:
        file_1_text = file_1.readlines()
    
    with open(file2) as file_2:
        file_2_text = file_2.readlines()
    
    # Find and print the diff:
    class_name_list = []
    for line in difflib.unified_diff(
            file_1_text, file_2_text, fromfile="file_1_tex.py", 
            tofile="file_2_text.py", n=5):
        class_name_list.append((re.findall(r'class (\w+)', str(line))))
    return class_name_list

def main():
    input("Press Enter to continue...")
    extraction("Sahyog_1.1")
    print("\n", "Uncompyling the pyc file", "\n")
    uncompile_exe()
    input("make some changes to Sahyog_1.2.py & Press enter to create Exe")
    extraction("Sahyog_1.2")
    print("\n", "Uncompyling the pyc file", "\n")
    uncompile_exe()
    
    class_list =[ clsname[0] for clsname in diff_fn("uncompiled_Sahyog_1.1.py", "uncompiled_Sahyog_1.2.py") if  clsname!=[]]
    print(class_list)
    df = pd.DataFrame(class_list, columns=["class"])
    df.to_excel("output.xlsx")
    print("\n\n","the end", "\n\n")
if __name__ == '__main__':
    main()

