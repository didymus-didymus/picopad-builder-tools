#!/usr/bin/env python3

import os
import subprocess

rootPath = os.path.normpath(f'{os.environ["PICOPAD_BASE_PATH"]}../../..')

normalText = "\033[0;37;40m"
redText    = "\033[0;31;40m"

def refreshDirectory(repoPath):
    try:
        subprocess.check_output(['git','pull',repoPath], cwd=repoPath, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        errInfo=e.output.decode()
        reportError(repoPath, errInfo)
        return

def updateSubmodules(repoPath):
    try:
        subprocess.check_output(['git','submodule', 'update', '--init', repoPath], cwd=repoPath, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        errInfo=e.output.decode()
        reportError(repoPath, errInfo)
        return

def reportError(fileName, ex):
    print(f"{redText}Error in {fileName}{normalText}\n{ex}\n")
    basePath = os.path.splitext(fileName)[0]
    f = open(f"{basePath}.errorInfo.txt", "w+")
    f.write(ex)
    f.close()

refreshDirectory(f'{rootPath}/pico-sdk/')
updateSubmodules(f'{rootPath}/pico-sdk/')
refreshDirectory(f'{rootPath}/picopad-builder-tools/')
refreshDirectory(f'{rootPath}/pico-examples/')
refreshDirectory(f'{rootPath}/picopad-playground/')