#!/usr/bin/env python3

import sys
import os
import subprocess

rootPath = '/home/picoPad/picopad-playground/picopad-sdk/'
buildPath = rootPath + 'picopad-gb/'

yellowText = "\033[1;33;40m "
greenText  = "\033[1;32;40m "
normalText = "\033[0;37;40m "

def convertFile(fileName):
    basePath = os.path.splitext(os.path.basename(fileName))[0]
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
    print(yellowText+' MAKE execution:\n'+normalText)
    subprocess.check_call(['make'], cwd=buildPath)

    binaryPath = rootPath + 'build/'
    
    head, tail = os.path.split(fileName)
    os.rename(binaryPath+'PICOPAD-GB.PP2', f"{head}/{basePath}.PP2")
    print(greenText+f" FINISHED {basePath}\n"+normalText)

print(yellowText+'CMAKE execution:\n'+normalText)
subprocess.check_call(['cmake', '.'], cwd=buildPath)

for subdir, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith(".gb") or filepath.endswith(".gbc"):
            convertFile (filepath)
