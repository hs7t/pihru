import psutil
import requests
from datetime import datetime

ISO_8601_FORMAT = "%Y-%m-%d %H:%M:%S"
MAIN_THERMAL_SENSOR_ID = "cpu_thermal"
API_ADDRESS = "http://localhost:8000"

def readCPUUsage():
    psutilOutput = psutil.cpu_percent(interval=0.2)
    return {
        "percentage": psutilOutput
    }

def readRAMUsage():
    psutilOutput = psutil.virtual_memory()
    memoryUsage = psutilOutput
    return {
        "used": memoryUsage.used,
        "percentage": memoryUsage.percent,
        "available": memoryUsage.available,
        "total": memoryUsage.total,
    }

def readStorageUsage():
    psutilOutput = psutil.disk_usage('/')
    diskUsage = psutilOutput

    return {
        "used": diskUsage.used,
        "percentage": diskUsage.percent,
        "available": diskUsage.free,
        "total": diskUsage.total,
    }

def readTemperature():
    psutilOutput = psutil.sensors_temperatures() # pyright: ignore[reportAttributeAccessIssue]
    currentTemperature = psutilOutput[MAIN_THERMAL_SENSOR_ID][0].current

    return currentTemperature

def fetchStats():
    checks = [("CPUUsage", readCPUUsage), ("RAMUsage", readRAMUsage), ("storageUsage", readStorageUsage), ("temperature", readTemperature)]

    output = {}
    for checkName, function in checks:
        try: 
            output[checkName] = function()
        except Exception as e:
            print(f"oh no in {checkName}:", e)
            output[checkName] = None
    
    return output

def postBeam():
    beamStats = fetchStats()

    beam = {
        "stats": {
            "CPUUsage": beamStats["CPUUsage"],
            "RAMUsage": beamStats["RAMUsage"],
            "storageUsage": beamStats["storageUsage"],
            "temperature": beamStats["temperature"],
        },
        "time": datetime.now().strftime(ISO_8601_FORMAT)
    }

    response = requests.post((API_ADDRESS + "/beam/"), json=beam)
    print(response)

postBeam()