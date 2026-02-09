import os
import sys
import shutil
import subprocess 
from pathlib import Path

def run_cmd(command)-> tuple[str|bytes, str|bytes, int]:
    """
        Run a command and returns the stdout, stderr, retcode
        obtained as a result of running the provided command
    """
    retcode = 0
    stdout = None
    stderr = None
    with subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE) as proc:
        stdout, stderr = proc.communicate()
        retcode = proc.returncode

    return stdout.decode('utf-8'), stderr.decode('utf-8'), retcode

def run_cmd_check_file(cmd, files: list):
    """Check if a file is created after running a cmd, if not, throw an exception"""
    stdout, stderr, retcode = run_cmd(cmd)

    
    # Verify launcher has been added 
    for file in files:
        if not os.path.exists(file):
            print("[-] The following command failed:\t"+cmd)
            print(f"[-] Error Code::\t\t\t{retcode}")

            if stdout:
                print(f"[-] STDOUT:\n{stdout}")

            if stderr:
                print(f"[-] STDERR:\n{stderr}")

            raise Exception(f"Command `{cmd}` failed to produce `{file}`")
        
def copy_dir_contents(src, dst):
    src = Path(src)
    dst = Path(dst)

    dst.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)  # preserves metadata