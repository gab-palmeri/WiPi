import psutil
import subprocess
import docker
import socket

def get_local_ip():
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                return addr.address
    return "N/A"

def get_system_info():
    return {
        "local_ip": get_local_ip(),
        "cpu": psutil.cpu_percent(),
        "ram_used": psutil.virtual_memory().percent,
        "ram_total": round(psutil.virtual_memory().total / (1024 ** 3)),
        "temperature": get_temperature()
    }

def get_temperature():
    try:
        output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        return output.replace("temp=", "").strip()
    except Exception:
        return "N/A"


def get_docker_info():
    client = docker.from_env()
    containers = []

    docker_ps_info = client.api.containers(all=True)


    for c in docker_ps_info:
        status_str = c.get("Status", "Unknown")

        containers.append({
            "name": c["Names"][0],
            "status": status_str,
            "port": c['Ports'][-1]['PublicPort'] if c['Ports'] else "N/A",
        })
    return containers


def shutdown():
    try:
        subprocess.run(["sudo", "shutdown", "-h", "now"])
    except subprocess.CalledProcessError:
        return False

def reboot():
    try:
        subprocess.run(["sudo", "reboot"])
    except subprocess.CalledProcessError:
        return False