import subprocess

def runCommand(command: list):
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result

def readTemperature():
    try: 
        commandOutput = runCommand(['vcgencmd', 'measure_temp']).stdout
    except subprocess.CalledProcessError as e:
        print("error running readTemperature: ", e)
    