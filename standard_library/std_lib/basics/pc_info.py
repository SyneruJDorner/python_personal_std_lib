import psutil, platform, cpuinfo, GPUtil
from datetime import datetime

class PC_INFO():
    '''
    This class is used to get information about the PC.
    '''
    class system_info():
        '''
        This class is used to get information about the system.
        '''
        __uname = platform.uname()
        __system = None
        __node_name = None
        __release = None
        __version = None
        __machine = None
        __processor = None
        
        @classmethod
        def __update_system_info(cls):
            '''
            PRIVATE METHOD
            This method updates the system information.
            '''
            cls.__system = cls.__uname.system
            cls.__node_name = cls.__uname.node
            cls.__release = cls.__uname.release
            cls.__version = cls.__uname.version
            cls.__machine = cls.__uname.machine
            cls.__processor = cls.__uname.processor
    
        @classmethod
        def __str__(cls):
            '''
            PRIVATE METHOD
            This method prints the system information.
            '''
            cls.__update_system_info()
            constructed_str = ""
            constructed_str += "="*40 + "System Information" + "="*40 + "\n"
            constructed_str += "System: {0}".format(cls.__system) + "\n"
            constructed_str += "Node Name: {0}".format(cls.__node_name) + "\n"
            constructed_str += "Release: {0}".format(cls.__release) + "\n"
            constructed_str += "Version: {0}".format(cls.__version) + "\n"
            constructed_str += "Machine: {0}".format(cls.__machine) + "\n"
            constructed_str += "Processor: {0}".format(cls.__processor) + "\n"
            return constructed_str


        @classmethod
        def get_system(cls):
            '''
            This method returns the system.
            '''
            cls.__update_system_info()
            return cls.__system

        @classmethod
        def get_node_name(cls):
            '''
            This method returns the node name.
            '''
            cls.__update_system_info()
            return cls.__node_name

        @classmethod
        def get_release(cls):
            '''
            This method returns the release.
            '''
            cls.__update_system_info()
            return cls.__release

        @classmethod
        def get_version(cls):
            '''
            This method returns the version.
            '''
            cls.__update_system_info()
            return cls.__version

        @classmethod
        def get_machine(cls):
            '''
            This method returns the machine.
            '''
            cls.__update_system_info()
            return cls.__machine

        @classmethod
        def get_processor(cls):
            '''
            This method returns the processor.
            '''
            cls.__update_system_info()
            return cls.__processor

    class boot_info():
        '''
        This class is used to get information about the boot.
        '''
        __boot_time = None
        __uptime = None

        @classmethod
        def __update_boot_info(cls):
            '''
            PRIVATE METHOD
            This method updates the boot information.
            '''
            cls.__boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
            cls.__uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())


        @classmethod
        def __str__(cls):
            '''
            PRIVATE METHOD
            This method prints the boot information.
            '''
            cls.__update_boot_info()
            constructed_str = ""
            constructed_str += "="*40 + "Boot Information" + "="*40 + "\n"
            constructed_str += "Boot Time: {0}".format(cls.__boot_time) + "\n"
            constructed_str += "Uptime: {0}".format(cls.__uptime) + "\n"
            return constructed_str

        @classmethod
        def get_boot_time(cls):
            '''
            This method returns the boot time.
            '''
            cls.__update_boot_info()
            return cls.__boot_time

        @classmethod
        def get_uptime(cls):
            '''
            This method returns the uptime.
            '''
            cls.__update_boot_info()
            return cls.__uptime

    class cpu_info():
        '''
        This class is used to get information about the CPU.
        '''
        __cpu_name = None
        __physical_cores = None
        __total_cores = None
        __max_freq = None
        __min_freq = None
        __current_freq = None

        __cpu_percent = None
        __total_cpu_usage = None

        @classmethod
        def __update_cpu_info(cls):
            '''
            PRIVATE METHOD
            This method updates the CPU information.
            '''
            cls.__cpu_name = cpuinfo.get_cpu_info()['brand_raw']
            cls.__physical_cores = psutil.cpu_count(logical=False)
            cls.__total_cores = psutil.cpu_count(logical=True)
            cls.__max_freq = psutil.cpu_freq().max
            cls.__min_freq = psutil.cpu_freq().min
            cls.__current_freq = psutil.cpu_freq().current
            cls.__cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cls.__total_cpu_usage = psutil.cpu_percent()

        @classmethod
        def __str__(cls):
            '''
            PRIVATE METHOD
            This method prints the CPU information.
            '''
            cls.__update_cpu_info()
            constructed_str = ""
            constructed_str += "="*40 + "CPU Information" + "="*40 + "\n"
            constructed_str += "Physical cores: {0}\n".format(cls.__physical_cores)
            constructed_str += "Total cores: {0}\n".format(cls.__total_cores)
            constructed_str += "Max frequency: {0}\n".format(cls.__max_freq)
            constructed_str += "Min frequency: {0}\n".format(cls.__min_freq)
            constructed_str += "Current frequency: {0}\n".format(cls.__current_freq)
            constructed_str += "CPU Usage Per Core:\n"
            for i, percentage in enumerate(cls.__cpu_percent):
                constructed_str += "Core {0}: {1}%\n".format(i, percentage)
            constructed_str += "Total CPU Usage: {0}%\n".format(cls.__total_cpu_usage)
            return constructed_str

        @classmethod
        def get_cpu_name(cls):
            '''
            This method returns the CPU name.
            '''
            cls.__update_cpu_info()
            return cls.__cpu_name

        @classmethod
        def get_physical_cores(cls):
            '''
            This method returns the number of physical cores.
            '''
            cls.__update_cpu_info()
            return cls.__physical_cores

        @classmethod
        def get_total_cores(cls):
            '''
            This method returns the number of total cores.
            '''
            cls.__update_cpu_info()
            return cls.__total_cores

        @classmethod
        def get_max_freq(cls):
            '''
            This method returns the maximum frequency.
            '''
            cls.__update_cpu_info()
            return cls.__max_freq

        @classmethod
        def get_min_freq(cls):
            '''
            This method returns the minimum frequency.
            '''
            cls.__update_cpu_info()
            return cls.__min_freq

        @classmethod
        def get_current_freq(cls):
            '''
            This method returns the current frequency.
            '''
            cls.__update_cpu_info()
            return cls.__current_freq

        @classmethod
        def get_cpu_percent(cls):
            '''
            This method returns the CPU usage per core.
            '''
            cls.__update_cpu_info()
            return cls.__cpu_percent

        @classmethod
        def get_total_cpu_usage(cls):
            '''
            This method returns the total CPU usage.
            '''
            cls.__update_cpu_info()
            return cls.__total_cpu_usage

    class memory_info():
        '''
        This class is used to get information about the memory.
        '''
        vmem = psutil.virtual_memory()
        smem = psutil.swap_memory()
        __total = None
        __available = None
        __used = None
        __percent = None
        __free = None
        __swap_total = None
        __swap_used = None
        __swap_free = None
        __swap_percent = None
        __swap_sin = None
        __swap_sout = None

        @classmethod
        def __get_size(cls, bytes, suffix="B"):
            '''
            PRIVATE METHOD
            This method converts bytes to a human readable format.

            Scale bytes to its proper format
            e.g:
                1253656 => '1.20MB'
                1253656678 => '1.17GB'
            '''
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor

        @classmethod
        def __update_memory_info(cls):
            '''
            PRIVATE METHOD
            This method updates the memory information.
            '''
            cls.__total = cls.__get_size(cls.vmem.total)
            cls.__available =cls.__get_size( cls.vmem.available)
            cls.__used = cls.__get_size(cls.vmem.used)
            cls.__free = cls.__get_size(cls.vmem.free)
            cls.__percent = cls.vmem.percent
            cls.__swap_total = cls.__get_size(cls.smem.total)
            cls.__swap_used = cls.__get_size(cls.smem.used)
            cls.__swap_free = cls.__get_size(cls.smem.free)
            cls.__swap_percent = cls.smem.percent
            cls.__swap_sin = cls.smem.sin
            cls.__swap_sout = cls.smem.sout

        @classmethod
        def __str__(cls):
            '''
            PRIVATE METHOD
            This method prints the memory information.
            '''
            cls.__update_memory_info()
            constructed_str = ""
            constructed_str += "="*40 + "Memory Information" + "="*40 + "\n"
            constructed_str += "Total: {0}\n".format(cls.__total)
            constructed_str += "Available: {0}\n".format(cls.__available)
            constructed_str += "Used: {0}\n".format(cls.__used)
            constructed_str += "Free: {0}\n".format(cls.__free)
            constructed_str += "Percent: {0}\n".format(cls.__percent)
            constructed_str += "="*20 + "SWAP" + "="*20 + "\n"
            constructed_str += "Swap Total: {0}\n".format(cls.__swap_total)
            constructed_str += "Swap Used: {0}\n".format(cls.__swap_used)
            constructed_str += "Swap Free: {0}\n".format(cls.__swap_free)
            constructed_str += "Swap Percent: {0}\n".format(cls.__swap_percent)
            return constructed_str
        
        @classmethod
        def get_total(cls):
            '''
            This method returns the total memory.
            '''
            cls.__update_memory_info()
            return cls.__total
        
        @classmethod
        def get_available(cls):
            '''
            This method returns the available memory.
            '''
            cls.__update_memory_info()
            return cls.__available
        
        @classmethod
        def get_used(cls):
            '''
            This method returns the used memory.
            '''
            cls.__update_memory_info()
            return cls.__used

        @classmethod
        def get_free(cls):
            '''
            This method returns the free memory.
            '''
            cls.__update_memory_info()
            return cls.__free

        @classmethod
        def get_percent(cls):
            '''
            This method returns the memory usage.
            '''
            cls.__update_memory_info()
            return cls.__percent

        @classmethod
        def get_swap_total(cls):
            '''
            This method returns the total swap.
            '''
            cls.__update_memory_info()
            return cls.__swap_total

        @classmethod
        def get_swap_used(cls):
            '''
            This method returns the used swap.
            '''
            cls.__update_memory_info()
            return cls.__swap_used
        
        @classmethod
        def get_swap_free(cls):
            '''
            This method returns the free swap.
            '''
            cls.__update_memory_info()
            return cls.__swap_free

        @classmethod
        def get_swap_percent(cls):
            '''
            This method returns the swap usage.
            '''
            cls.__update_memory_info()
            return cls.__swap_percent

        @classmethod
        def get_swap_sin(cls):
            '''
            This method returns the swap in.
            '''
            cls.__update_memory_info()
            return cls.__swap_sin

        @classmethod
        def get_swap_sout(cls):
            '''
            This method returns the swap out.
            '''
            cls.__update_memory_info()
            return cls.__swap_sout

    class disk_info():
        '''
        This class is used to get information about the disk.
        '''
        __partitions = psutil.disk_partitions()
        _disks = []
        __disk_io = psutil.disk_io_counters()
        __disk_total_read = None
        __disk_total_write = None

        @classmethod
        def __update_disk_info(cls):
            '''
            PRIVATE METHOD
            This method updates the disk information.
            '''
            for partition in cls.__partitions:
                disk_info = { "device": partition.device, "mountpoint": partition.mountpoint, "fstype": partition.fstype, "partition_usage": None, "total": None, "used": None, "free": None, "percent": None }

                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                except PermissionError:
                    continue

                disk_info["partition_usage"] = partition_usage
                disk_info["total"] = cls.__get_size(partition_usage.total)
                disk_info["used"] = cls.__get_size(partition_usage.used)
                disk_info["free"] = cls.__get_size(partition_usage.free)
                disk_info["percent"] = partition_usage.percent
                cls._disks.append(disk_info)

            cls.__disk_total_read = cls.__get_size(cls.__disk_io.read_bytes)
            cls.__disk_total_write = cls.__get_size(cls.__disk_io.write_bytes)


        @classmethod
        def __get_size(cls, bytes, suffix="B"):
            '''
            PRIVATE METHOD
            This method converts bytes to a human readable format.

            Scale bytes to its proper format
            e.g:
                1253656 => '1.20MB'
                1253656678 => '1.17GB'
            '''
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor

        @classmethod
        def __str__(cls):
            '''
            PRIVATE METHOD
            This method prints the disk information.
            '''
            cls.__update_disk_info()
            constructed_str = ""
            constructed_str += "="*40 + "Disk Information" + "="*40 + "\n"
            constructed_str += "Partitions and Usage:\n"
            for disk in cls._disks:
                constructed_str += "=== Device: {0} ===\n".format(disk["device"])
                constructed_str += "  Mountpoint: {0}\n".format(disk["mountpoint"])
                constructed_str += "  File system type: {0}\n".format(disk["fstype"])
                constructed_str += "  Total Size: {0}\n".format(disk["total"])
                constructed_str += "  Used: {0}\n".format(disk["used"])
                constructed_str += "  Free: {0}\n".format(disk["free"])
                constructed_str += "  Percent: {0}\n".format(disk["percent"])
            constructed_str += "Total read: {0}\n".format(cls.__disk_total_read)
            constructed_str += "Total write: {0}\n".format(cls.__disk_total_write)
            return constructed_str

        @classmethod
        def get_partitions(cls):
            '''
            This method returns the partitions.
            '''
            cls.__update_disk_info()
            return cls._disks

        @classmethod
        def get_total_read(cls):
            '''
            This method returns the total read.
            '''
            cls.__update_disk_info()
            return cls.__disk_total_read

        @classmethod
        def get_total_write(cls):
            '''
            This method returns the total write.
            '''
            cls.__update_disk_info()
            return cls.__disk_total_write

    class network_info():
        '''
        This class is used to get information about the network.
        '''
        __if_addrs = psutil.net_if_addrs()
        _interfaces = []
        __net_io = psutil.net_io_counters()
        __total_bytes_sent = None
        __total_bytes_recv = None

        @classmethod
        def __update_network_info(cls):
            '''
            PRIVATE METHOD
            This method updates the network information.
            '''
            for interface_name, interface_addresses in cls.__if_addrs.items():
                for address in interface_addresses:
                    if (address.family == -1 or address.family == 23):
                        continue

                    interface_info = {"interface_name": None, "ip_addresses": None, "family": None, "mac_address": None, "netmask": None, "broadcast_ip": None, "broadcast_mac": None}
                    interface_info["interface_name"] = interface_name
                    interface_info["family"] = address.family

                    if (str(address.family) == 'AddressFamily.AF_INET'):
                        interface_info["ip_addresses"] = str(address.address)
                        interface_info["netmask"] = str(address.netmask)
                        interface_info["broadcast_ip"] = str(address.broadcast)
                    elif (str(address.family) == 'AddressFamily.AF_PACKET'):
                        interface_info["mac_address"] = str(address.address)
                        interface_info["netmask"] = str(address.netmask)
                        interface_info["broadcast_mac"] = str(address.broadcast)

                    cls._interfaces.append(interface_info)
            cls.__total_bytes_sent = cls.__get_size(cls.__net_io.bytes_sent)
            cls.__total_bytes_recv = cls.__get_size(cls.__net_io.bytes_recv)

        @classmethod
        def __get_size(cls, bytes, suffix="B"):
            '''
            PRIVATE METHOD
            This method converts bytes to a human readable format.
            Scale bytes to its proper format
            e.g:
                1253656 => '1.20MB'
                1253656678 => '1.17GB'
            '''
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor

        @classmethod
        def __str__(cls):
            '''
            PRIVATE METHOD
            This method prints the network information.
            '''
            cls.__update_network_info()
            constructed_str = ""
            constructed_str += "="*40 + "Network Information" + "="*40 + "\n"
            constructed_str += "Interfaces and Usage:\n"
            for interface in cls._interfaces:
                constructed_str += "=== Interface: {0} ===\n".format(interface["interface_name"])
                constructed_str += "  Family: {0}\n".format(interface["family"])

                if (str(interface["family"]) == 'AddressFamily.AF_INET'):
                    constructed_str += "  IP Address: {0}\n".format(interface["ip_addresses"])
                    constructed_str += "  Netmask: {0}\n".format(interface["netmask"])
                    constructed_str += "  Broadcast IP: {0}\n".format(interface["broadcast_ip"])
                elif (str(interface["family"]) == 'AddressFamily.AF_PACKET'):
                    constructed_str += "  MAC Address: {0}\n".format(interface["ip_addresses"])
                    constructed_str += "  Netmask: {0}\n".format(interface["netmask"])
                    constructed_str += "  Broadcast MAC: {0}\n".format(interface["broadcast_mac"])
            constructed_str += "Total Bytes Sent: {0}\n".format(cls.__total_bytes_sent)
            constructed_str += "Total Bytes Received: {0}\n".format(cls.__total_bytes_recv)
            return constructed_str

        @classmethod
        def get_interfaces(cls):
            '''
            This method returns the interfaces.
            '''
            cls.__update_network_info()
            return cls._interfaces

        @classmethod
        def get_total_bytes_sent(cls):
            '''
            This method returns the total bytes sent.
            '''
            cls.__update_network_info()
            return cls.__total_bytes_sent

        @classmethod
        def get_total_bytes_recv(cls):
            '''
            This method returns the total bytes received.
            '''
            cls.__update_network_info()
            return cls.__total_bytes_recv

    class gpu_info():
        '''
        This class is used to get information about the GPU.
        '''
        __gpus = GPUtil.getGPUs()
        __list_gpus = []
        __gpu_id = None 
        __gpu_name = None
        __gpu_load = None
        __gpu_free_memory = None
        __gpu_used_memory = None
        __gpu_total_memory = None
        __gpu_temperature = None
        __gpu_uuid = None

        @classmethod
        def __update_gpu_info(cls):
            '''
            PRIVATE METHOD
            This method updates the GPU information.
            '''
            cls.__list_gpus = []
            for gpu in cls.__gpus:
                gpu_info = {}
                gpu_info["gpu_id"] = gpu.id
                gpu_info["gpu_name"] = gpu.name
                gpu_info["gpu_load"] = str(gpu.load * 100) + "%"
                gpu_info["gpu_free_memory"] = str(gpu.memoryFree) + "MB"
                gpu_info["gpu_used_memory"] = str(gpu.memoryUsed) + "MB"
                gpu_info["gpu_total_memory"] = str(gpu.memoryTotal) + "MB"
                gpu_info["gpu_temperature"] = str(gpu.temperature) + "°C"
                gpu_info["gpu_uuid"] = gpu.uuid
                cls.__list_gpus.append(gpu_info)

        @classmethod
        def __str__(cls):
            '''
            PRIVATE METHOD
            This method prints the GPU information.
            '''
            cls.__update_gpu_info()
            constructed_str = ""
            constructed_str += "="*40 + "GPU Information" + "="*40 + "\n"
            constructed_str += "GPUs and Usage:\n"
            for gpu in cls.__list_gpus:
                constructed_str += "=== GPU: {0} ===\n".format(gpu["gpu_name"])
                constructed_str += "  GPU ID: {0}\n".format(gpu["gpu_id"])
                constructed_str += "  GPU UUID: {0}\n".format(gpu["gpu_uuid"])
                constructed_str += "  GPU Load: {0}\n".format(gpu["gpu_load"])
                constructed_str += "  GPU Free Memory: {0}\n".format(gpu["gpu_free_memory"])
                constructed_str += "  GPU Used Memory: {0}\n".format(gpu["gpu_used_memory"])
                constructed_str += "  GPU Total Memory: {0}\n".format(gpu["gpu_total_memory"])
                constructed_str += "  GPU Temperature: {0}\n".format(gpu["gpu_temperature"])
            return constructed_str

        @classmethod
        def get_gpus(cls, index=-1):
            '''
            This method returns the GPUs.
            '''
            cls.__update_gpu_info()
            return cls.__list_gpus if index == -1 else cls.__list_gpus[index]

        @classmethod
        def get_gpu_id(cls, index=-1):
            '''
            This method returns the GPU ID.
            '''
            cls.__update_gpu_info()
            gpu_ids = []
            for gpu in cls.__list_gpus:
                gpu_ids.append(gpu["gpu_id"])
            return gpu_ids if index == -1 else gpu_ids[index]

        @classmethod
        def get_gpu_name(cls, index=-1):
            '''
            This method returns the GPU name.
            '''
            cls.__update_gpu_info()
            gpu_names = []
            for gpu in cls.__list_gpus:
                gpu_names.append(gpu["gpu_name"])
            return gpu_names if index == -1 else gpu_names[index]

        @classmethod
        def get_gpu_load(cls, index=-1):
            '''
            This method returns the GPU load.
            '''
            cls.__update_gpu_info()
            gpu_loads = []
            for gpu in cls.__list_gpus:
                gpu_loads.append(gpu["gpu_load"])
            return gpu_loads if index == -1 else gpu_loads[index]

        @classmethod
        def get_gpu_free_memory(cls, index=-1):
            '''
            This method returns the GPU free memory.
            '''
            cls.__update_gpu_info()
            gpu_free_memory = []
            for gpu in cls.__list_gpus:
                gpu_free_memory.append(gpu["gpu_free_memory"])
            return gpu_free_memory if index == -1 else gpu_free_memory[index]

        @classmethod
        def get_gpu_used_memory(cls, index=-1):
            '''
            This method returns the GPU used memory.
            '''
            cls.__update_gpu_info()
            gpu_used_memory = []
            for gpu in cls.__list_gpus:
                gpu_used_memory.append(gpu["gpu_used_memory"])
            return gpu_used_memory if index == -1 else gpu_used_memory[index]

        @classmethod
        def get_gpu_total_memory(cls, index=-1):
            '''
            This method returns the GPU total memory.
            '''
            cls.__update_gpu_info()
            gpu_total_memory = []
            for gpu in cls.__list_gpus:
                gpu_total_memory.append(gpu["gpu_used_memory"])
            return gpu_total_memory if index == -1 else gpu_total_memory[index]

        @classmethod
        def get_gpu_temperature(cls, index=-1):
            '''
            This method returns the GPU temperature.
            '''
            cls.__update_gpu_info()
            gpu_temperature = []
            for gpu in cls.__list_gpus:
                gpu_temperature.append(gpu["gpu_temperature"])
            return gpu_temperature if index == -1 else gpu_temperature[index]

        @classmethod
        def get_gpu_uuid(cls, index=-1):
            '''
            This method returns the GPU UUID.
            '''
            cls.__update_gpu_info()
            gpu_uuid = []
            for gpu in cls.__list_gpus:
                gpu_uuid.append(gpu["gpu_uuid"])
            return gpu_uuid if index == -1 else gpu_uuid[index]

    @classmethod
    def __str__(cls):
        '''
        PRIVATE METHOD
        This method prints the PC_INFO for each subclass:
            -system_info
            -boot_info
            -cpu_info
            -memory_info
            -disk_info
            -network_info
            -gpu_info
        '''
        constructed_str = ""
        constructed_str += PC_INFO.system_info().__str__() + "\n"
        constructed_str += PC_INFO.boot_info().__str__()  + "\n"
        constructed_str += PC_INFO.cpu_info().__str__() + "\n"
        constructed_str += PC_INFO.memory_info().__str__() + "\n"
        constructed_str += PC_INFO.disk_info().__str__() + "\n"
        constructed_str += PC_INFO.network_info().__str__() + "\n"
        constructed_str += PC_INFO.gpu_info().__str__() + "\n"
        return constructed_str