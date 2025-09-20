import subprocess

def readEcho():
    try:
        result = subprocess.run(['echo', 'hello world'], capture_output=True, text=True, check=True, shell=True)
        return result
    except subprocess.CalledProcessError as e: 
        return "oh no something happened idk"

print(readEcho())