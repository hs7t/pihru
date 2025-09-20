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
        "total": psutilOutput.total,
        "used": psutilOutput.used,
        "available": psutilOutput.available,
        "percentage": psutilOutput.percent,
    }

def readStorageUsage():
    psutilOutput = psutil.disk_usage('/')
    diskUsage = psutilOutput

    return {
        "used": diskUsage.used,
        "available": diskUsage.free,
        "total": diskUsage.total,
    }

def readTemperature():
    psutilOutput = psutil.sensors_temperatures() # pyright: ignore[reportAttributeAccessIssue]
    currentTemperature = psutilOutput[MAIN_THERMAL_SENSOR_ID][0].current

    return currentTemperature