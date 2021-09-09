import glob, os, time
from subprocess import check_output


def exe_scanner():
    print("exe_scanner")
    global exe_files_list
    exe_files_list = []
    if glob.glob("dist/*.exe"):
        for fn in glob.glob("dist/*.exe"):
            exe_files_list.append(fn.split('\\')[-1])
    else:
        print("\n\n there is no exe file in the folder \n\n  \
        So we're creating executable for hello_world.py")
        check_output("pyinstaller --onefile hello_world.py", shell=True)
        exe_scanner()
        

def extraction():
    exe_scanner()
    print("exe_files", exe_files_list)
    global exe_file_1
    exe_file_1 = exe_files_list[0]
    os.system('python pyinstxtractor.py dist/{}'.format(exe_file_1))

def uncompile_exe():
    pyc_file_location = str(exe_file_1) + "_" + "extracted/{}".format(exe_file_1.replace(".exe", ".pyc"))
    print("pyc_file_location", pyc_file_location)
    os.system("uncompyle6 {}".format(pyc_file_location))


def main():
    extraction()
    print("\n", "Uncompyling the pyc file", "\n")
   
    time.sleep(5)
    uncompile_exe()
if __name__ == '__main__':
    main()












# # exe_file=$(where *.exe)

# # echo $exe_file
# # python pyinstxtractor.py $exe_file
# pyc_file_name=$(findstr /R [\][A-Z_0]\w+.exe)
# echo $pyc_file_name 
# uncompyle6 "pyc_file_name"