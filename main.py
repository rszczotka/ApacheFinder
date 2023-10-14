import socket
import urllib.request
import threading

def is_apache_running(ip_address):
    try:
        url = f"http://{ip_address}/"
        response = urllib.request.urlopen(url, timeout=1)
        server_header = response.headers.get("Server")
        if server_header and "Apache" in server_header:
            return True
    except:
        pass
    return False

def scan_ip_address(ip_address, results):
    if is_apache_running(ip_address):
        print(f"Apache server found at {ip_address}")
        results.append(ip_address)

def scan_network():
    subnet = ".".join(socket.gethostbyname_ex(socket.gethostname())[2][0].split(".")[:3])
    print(f"Scanning network {subnet}.0/24 for Apache servers...")
    results = []
    threads = []
    for i in range(1, 255):
        ip_address = f"{subnet}.{i}"
        thread = threading.Thread(target=scan_ip_address, args=(ip_address, results))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    if not results:
        print("No Apache servers found on the network.")
scan_network()
input("Press any key to exit...")