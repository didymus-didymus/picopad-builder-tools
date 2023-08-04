#!/usr/bin/env python3

import sys
import os
import subprocess
import shutil
import traceback


rootPath = os.path.normpath(f'{os.environ["PICOPAD_BASE_PATH"]}..')

yellowText = "\033[1;33;40m"
greenText  = "\033[1;32;40m"
normalText = "\033[0;37;40m"
redText    = "\033[0;31;40m"

def convertFile(fileName):
    basePath = os.path.splitext(os.path.basename(fileName))[0]
    buildPath = rootPath + '/picopad-gb/'
    if fileName.endswith(".gbc"):
        buildPath = rootPath + '/picopad-gbc/'

    print(greenText+f"Starting: {basePath}")

    tempFile = 'temp.c'
    subprocess.check_call(['xxd','-i', fileName, tempFile])
    with open(tempFile, 'r') as rom_file:
        rom_file.readline()
        with open(buildPath + 'src/rom.c', 'w') as rom_c:
            rom_c.write('#include <pico/platform.h>\n')
            rom_c.write('const unsigned char __in_flash("rom") gameRom[] = {\n')
            while True:
                line = rom_file.readline()
                if not line:
                    break
                rom_c.write(line)
    os.remove(tempFile)
    print(yellowText+'MAKE execution:\n'+normalText)
    try:
        subprocess.check_output(['make'], cwd=buildPath, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        errInfo=e.output.decode()
        reportError(fileName, errInfo)
        return

    binaryPath = rootPath + '/build/'
    
    head, tail = os.path.split(fileName)
    squeezedFileName = basePath.replace(" ", "").replace(")","").replace("(","").replace("-","").replace(",","")
    shutil.copyfile(binaryPath+'PICOPAD-GB.PP2', f"{head}/{squeezedFileName}.PP2")
    os.remove(binaryPath+'PICOPAD-GB.PP2')
    print(yellowText+f"FINISHED as {squeezedFileName}.PP2\n"+normalText)

def reportError(fileName, ex):
    print(f"{redText}Error in {fileName}{normalText}\n{ex}\n")
    basePath = os.path.splitext(fileName)[0]
    f = open(f"{basePath}.errorInfo.txt", "w+")
    f.write(ex)
    f.close()

for subdir, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith(".gb") or filepath.endswith(".gbc"):
            try:
                convertFile (filepath)
            except:
                var = traceback.format_exc()
                reportError (filepath, var)