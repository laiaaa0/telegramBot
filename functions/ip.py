
import socket
from requests import get

def get_external_ip():
    ip = get('https://api.ipify.org').text
    return ip

def get_internal_ip():
    return socket.gethostbyname(socket.gethostname())

def get_ip_information():
    txt = "Your external IP is {external_ip} \n Your internal IP is {internal_ip}"
    return txt.format(external_ip=get_external_ip(), internal_ip=get_internal_ip())

