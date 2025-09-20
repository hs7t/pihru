import subprocess

def runCommand(command: list):
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result
