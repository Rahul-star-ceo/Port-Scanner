from django.shortcuts import render
from django.http import HttpResponse
from .models import ipaddres
import socket
import re
import threading
# Create your views here.



def socket_app(request):
    return HttpResponse("welcome")
 
def ip_taking(request):
    Scanning=[]
    ip_pattern=re.compile(("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"))
    port_pattern=re.compile(("([0-9]+)-([0-9]+)"))
    port_min=0
    port_max=65535
    open_ports=[]
    threads = []
   

    if request.method=="POST":
        ip_address = request.POST.get('ipAddress')
        port_number = request.POST.get('portNumber')
        
        
        while True:
            if re.match(ip_pattern,ip_address):
                print(f"given ip {ip_address} is valid")
                break
            else:
                print(f"given ip {ip_address} is valid")
                break
        while True:
            port_number_valid=port_pattern.search(port_number.replace(" ",""))
            if port_number_valid:
                port_min=int(port_number_valid.group(1))
                port_max=int(port_number_valid.group(2))
            print(port_min,port_max)
            break
        def scan_port(ip_address,port,open_ports):
            try:
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as s:
                    # s.settimeout(0.5)
                    result=s.connect_ex((ip_address,port))
                    if result ==0:
                        print(f"port {port} is open")
                        status=f"port {port} is open"
                        Scanning.append(status)
                        open_ports.append(port)
                    else:
                        print(f"port {port} is closed") 
                        status=f"port {port} is closed"
                        Scanning.append(status)
            except socket.error as e:
                pass

        for port in range(port_min ,port_max+1):
            # try:
            #     with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            #         s.settimeout(0.5)
            #         s.connect((ip_address,port))
            #         open_ports.append(port)
            # except:
            #     pass
            thread=threading.Thread(target=scan_port,args=(ip_address,port,open_ports))
            thread.start()
            threads.append(thread)
            for thread in threads:
                thread.join() #waiting for the completion one thread execution.
         

       
        for port in open_ports:
          print(f"{port} is open of given {ip_address} ")

        scanning=ipaddres(ip_address=ip_address,port_number=port_number)
        scanning.save()
    if open_ports==0:
        open_ports=["no open ports "]
    content={
        'form':open_ports,
        'Scanning':Scanning,
    }
    
        

    return render(request,'socket.html',content)
    
