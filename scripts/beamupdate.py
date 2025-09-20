import subprocess

def runOutputCommand(command: list):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result
    except subprocess.CalledProcessError as e: 
        return "oh no something happened idk"

print(runOutputCommand(['echo', 'hello, world']))