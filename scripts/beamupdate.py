import psutil

MAIN_THERMAL_SENSOR_ID = "cpu_thermal"

def readCPUUsage():
    psutilOutput = psutil.cpu_percent(interval=0.2)
    return {
        "percentage": psutilOutput
    }

def readRAMUsage():
    psutilOutput = psutil.virtual_memory()
    return {
        "used": psutilOutput.used,
        "available": psutilOutput.available,
        "percentage": psutilOutput.percent,
    }

def readTemperature():
    psutilOutput = psutil.sensors_temperatures() # pyright: ignore[reportAttributeAccessIssue]
    currentTemperature = psutilOutput[MAIN_THERMAL_SENSOR_ID][0].current

    return currentTemperature