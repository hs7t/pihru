import psutil

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
        "percent": psutilOutput.percent,
    }