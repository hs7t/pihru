import psutil

def readCPUUsage():
    return psutil.cpu_percent(interval=0.2)
