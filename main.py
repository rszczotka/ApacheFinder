import socket
import urllib.request
import threading

print('''
 █████╗ ██████╗  █████╗  ██████╗██╗  ██╗███████╗    ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔══██╗██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝    ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
███████║██████╔╝███████║██║     ███████║█████╗      █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██╔══██║██╔═══╝ ██╔══██║██║     ██╔══██║██╔══╝      ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██║  ██║██║     ██║  ██║╚██████╗██║  ██║███████╗    ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                            v2.0 by @rszczotka
''')

def is_apache_running(ip_address):
    try:
        url = f"http://{ip_address}/"
        response = urllib.request.urlopen(url, timeout=1)
        server_header = response.headers.get("Server")
        if server_header and "Apache" in server_header:
            print("Apache server found on: "+ ip_address)
            return True
    except:
        pass
    return False

def check_folders(ip_address, folders):
    matches = []
    for folder in folders:
        try:
            url = f"http://{ip_address}/{folder}"
            response = urllib.request.urlopen(url, timeout=1)
            matches.append(folder)
        except:
            pass
    if matches:
        print(f"Folders {', '.join(matches)} found on {ip_address}.")

def scan_network(folders, subs):
    print(f"Scanning network for Apache servers...")
    results = []
    threads = []
    for j in (subs):
        print("\n###################################")
        print("\nChecking subnet: " + j + "...\n")
        for i in range(1, 255):            
            ip_address = f"192.168.{j}.{i}"
            thread = threading.Thread(target=scan_ip_address, args=(ip_address, results, folders))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        if not results:
            print("No Apache servers found on the subnet:" + j)
    if results:
        print("\n###################################")
        print("Checking for accessible folders...\n")
        for result in results:
            check_folders(result, folders)
    input("Press enter to exit...")



def scan_ip_address(ip_address, results, folders):
    if is_apache_running(ip_address):
        results.append(ip_address)

def main():
    scan_type = input("Do you want to do (q)uick or (f)ull scan?").lower()
    if scan_type == "quick" or scan_type == "q":
        local_ip_address = socket.gethostbyname(socket.gethostname())
        subnet = local_ip_address.split(".")[2]
        subs = [subnet]
    elif scan_type == "full" or scan_type == "f":
        subs = input("Enter subnets names separated by comma: ").split(",")
    else:
        print("Invalid scan type.")
        return
    folders = input("Enter folder names separated by comma: ").split(",")
    scan_network(folders, subs)
    

if __name__ == "__main__":
    main()
