import subprocess
import psutil

def get_cpu_info():
    # Execute the lscpu command and decode the output
    result = subprocess.run(['lscpu'], stdout=subprocess.PIPE)
    lscpu_output = result.stdout.decode('utf-8')

    cpu_manufacturer = "Unknown"
    cpu_model = "Unknown"
    cpu_cores = "Unknown"
    cpu_arch = "Unknown"
    threads_per_core = 1  # Defaulting to 1 in case it's not found
    cores_per_socket = 1  # Defaulting to 1 in case it's not found
    sockets = 1           # Defaulting to 1 in case it's not found

    for line in lscpu_output.splitlines():
        if "Vendor ID:" in line:
            cpu_manufacturer = line.split(":")[1].strip()
        if "Model name:" in line:
            cpu_model = line.split(":")[1].strip()
            # Setting cpu_model to Apple silicon if found
            if cpu_manufacturer == "Apple":
                cpu_model = "Apple silicon ARM-based processor"				
        if "Thread(s) per core:" in line:
            threads_per_core = int(line.split(":")[1].strip())
        if "Core(s) per socket:" in line:
            cores_per_socket = int(line.split(":")[1].strip())
        if "Socket(s):" in line:
            sockets = int(line.split(":")[1].strip())
        if "Architecture:" in line:
            cpu_arch = line.split(":")[1].strip()

    # Calculate total cores as threads per core * cores per socket * sockets
    cpu_cores = str(threads_per_core * cores_per_socket * sockets)

    return cpu_manufacturer, cpu_model, cpu_cores, cpu_arch

def get_cpu_utilization():
    # Use psutil to get current CPU utilization, pausing for 1 second to get an average
    return psutil.cpu_percent(interval=1)
