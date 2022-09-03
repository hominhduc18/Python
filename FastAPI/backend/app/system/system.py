# import psutil
# import time
# from subprocess import call
# import platform
# import cpuinfo
# from pydantic import BaseModel
# from typing import List, Union, Dict
# import os
# cmd = r"cat /sys/class/thermal/thermal_zone9/temp"
# class CPU(BaseModel):
#     cpu_percent: Union[float, str]
#     cpu_temp: Union[float, str]
#     percpu: Dict[str,float]
    
# def cpu_info():
#     cpu_percent = psutil.cpu_percent()
#     stream = os.popen(cmd)
#     cpu_temp = float(stream.read().strip("\n"))/1000
#     cpu_percent_percpu = psutil.cpu_percent( percpu=True)
#     percpu = dict()
#     for i in range(len(cpu_percent_percpu)):
#         percpu[f"cpu{i+1}"] = cpu_percent_percpu[i]
#     return {"cpu_percent":cpu_percent,"cpu_temp":cpu_temp,"percpu":percpu}
    
# def main():
#     a = CPU(**cpu_info())
#     print(a)
    
# if __name__ == "__main__":
#     main()

import platform
from datetime import datetime, timedelta
from unittest import result
import psutil
import shutil
from typing import Union
from pydantic import BaseModel
import os
import asyncio
class CPU(BaseModel):
    #cpu
    Physical_cores : Union[str, str] = None
    Max_Frequency : Union[float, str] = None
    Min_Frequency : Union[float, str] = None
    Current_Frequency : Union[float, str] = None
    Total_CPU_Usage : Union[str, str] = None
    Temperatue_CPU: Union[str, str] = None

def get_cpu():
    Physical_cores = psutil.cpu_count(logical=False)
    cpufreq = psutil.cpu_freq()
    Max_Frequency = round(cpufreq.max, 5)
    Min_Frequency = round(cpufreq.min,5)
    Current_Frequency = round(cpufreq.current,2) 
    Total_CPU_Usage = psutil.cpu_percent()
    # cmd = r"cat /sys/class/thermal/thermal_zone9/temp"
    # stream = os.popen(cmd)
    # Temperatue_CPU = float(stream.read().strip("\n"))/1000
    cmd_temps = r"cat /sys/class/thermal/thermal_zone*/temp"
    cmd_types = r"cat /sys/class/thermal/thermal_zone*/type"
    Temperatue_CPU = 0
    try:
        temps = os.popen(cmd_temps).read().strip("\n").split("\n")
        types = os.popen(cmd_types).read().strip("\n").split("\n")
        results = dict(zip(types, temps))
        Temperatue_CPU = float(results["soc_dts1"])/1000
    except:

        pass

    return {
        "Physical_cores": Physical_cores,
        "Max_Frequency": Max_Frequency,
        "Min_Frequency": Min_Frequency,
        "Current_Frequency": Current_Frequency,
        "Total_CPU_Usage": Total_CPU_Usage,
        "Temperatue_CPU": Temperatue_CPU,
    }

class RAM(BaseModel):
    #memory
    Total_memory: Union[float, str] = None
    Available_memory : Union[str, str] = None
    Used_memory : Union[float, str] = None
    Percentage_memory : Union[float, str] = None

    Total_swap : Union[str, str] = None
    Free_swap : Union[str, str] = None
    Used_swap : Union[float, str] = None
    Percentage_swap : Union[float, str] = None

def get_ram():
    svmem = psutil.virtual_memory()
    Total_memory = svmem.total
    Available_memory = svmem.available
    Used_memory = svmem.used
    Percentage_memory = svmem.percent

    swap = psutil.swap_memory()
    Total_swap = swap.total
    Free_swap = swap.free
    Used_swap = swap.used
    Percentage_swap = swap.percent
    return {
       "Total_memory": Total_memory, 
       "Available_memory": Available_memory, 
       "Used_memory": Used_memory, 
       "Percentage_memory": Percentage_memory, 

       "Total_swap": Total_swap, 
       "Free_swap": Free_swap, 
       "Used_swap": Used_swap, 
       "Percentage_swap": Percentage_swap, 
    } 
class DISK(BaseModel):
    #Dick usage
    Total_dick : Union[str, str] = None
    Used_dick : Union[float, str] = None
    Free_dick : Union[float, str] = None

def get_disk():
    total, used, free = shutil.disk_usage("/") 

    Total_disk = round(total *10**-9, 2)
    Used_disk = round(used * 10**-9,2)
    Free_disk = round(free * 10**-9,2 )
    Percent_used = round( 100 * Used_disk / Total_disk, 2 )
    Percent_free = round( 100 * Free_disk / Total_disk, 2 )
    Percent_other = round(100 - (Percent_used+Percent_free),2)
    return {
        "Total_disk": Total_disk,
        "Used_disk": Used_disk,
        "Free_disk": Free_disk,
        "Percent_used": Percent_used,
        "Percent_free": Percent_free,
        "Percent_other": Percent_other,
    }
class System(BaseModel):
    # in4
    System : Union[str,str] = None
    Node :  Union[str, str] = None
    Release : Union[str, str] = None
    Version : Union[float, str] = None
    Machine: Union[float, str] = None
    Processor : Union[float, str] = None
    Boot_time : Union[float, str] = None

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
    1253656 => '1.20MB'
    1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_system():
    System = platform.system()
    Node = platform.node()
    Release = platform.release()
    Version = platform.version()
    Machine = platform.machine()
    Processor = platform.processor()

    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    time_now = datetime.now()
    total = time_now - timedelta(days=bt.day, hours=bt.hour, minutes=bt.minute, seconds=bt.second)
    total = total.strftime("%H:%M:%S")
    # Boot_time= (f"{total.hour}:{total.minute}:{total.second}")
    return {
        "System": System,
        "Node": Node,
        "Release": Release,
        "Version": Version,
        "Machine": Machine,
        "Processor": Processor,
        "Boot_time": total,
    }

async def _get_system():
    return get_system()
async def _get_cpu():
    return get_cpu()
async def _get_ram():
    return get_ram()
async def _get_disk():
    return get_disk()

async def get_system_info():
    task1 = asyncio.create_task(_get_cpu())
    task2 = asyncio.create_task(_get_ram())
    task3 = asyncio.create_task(_get_disk())
    task4 = asyncio.create_task(_get_system())
    results = await asyncio.gather(task1, task2, task3, task4)
    system = [
        "cpu", "ram", "disk", "system"
    ]
    results = dict(zip(system,results))
    return results

def main():
    # import time
    # start_time = time.time()
    # # a = System(**get_system())
    # # b = CPU(**get_cpu())
    # # c = RAM(**get_ram())
    # # d = DISK(**get_disk())
    # a = asyncio.run(get_system_info())
    # cpu = CPU(**a["cpu"])
    # print(cpu)
    # process_time = time.time() - start_time
    # print(process_time)
    # pass
    cmd_temps = r"cat /sys/class/thermal/thermal_zone9/temp"
    cmd_types = r"cat /sys/class/thermal/thermal_zone9/type"

    temps = os.popen(cmd_temps).read().strip("\n").split("\n")
    types = os.popen(cmd_types).read().strip("\n").split("\n")
    print(temps)
    print(types)
    results = dict(zip(types, temps))
    Temperatue_CPU = float(results["x86_pkg_temp"])/1000
    print(Temperatue_CPU)
    # Temperatue_CPU = float(stream.read().strip("\n").split("\n"))/1000

if __name__ == "__main__":
    # main()
    a = asyncio.run(_get_ram())
    print(a)
    pass

    

