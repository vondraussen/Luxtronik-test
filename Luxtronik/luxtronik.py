import os
import websocket
import xml.etree.ElementTree as ET


class Luxtronik:
    def __init__(self, ip, port=8214, password=999999):
        self.ip = ip
        self.port = port
        self.password = password
        self.ws = websocket.WebSocket()
        self.ws.connect(f'ws://{ip}:{port}')

    def login(self):
        self.ws.send(f'LOGIN;{self.password}')

    def refresh(self):
        self.ws.send('REFRESH')
        return self.ws.recv()

    def save(self):
        self.ws.send('SAVE;1')

    def get(self, key):
        self.ws.send(f'GET;{key}')

    def set(self, key, value):
        self.ws.send(f'SET;{key};{value}')

    def parse_refresh_data(self, data):

        tree = ET.ElementTree(ET.fromstring(data))
        root = tree.getroot()
        
        # Access elements and attributes in the XML file
        # Example: print the tag name of the root element
        print(root.tag)

        childs = []
        
        # Iterate over child elements
        for child in root:
            childs.append((child.attrib, child.text))
            print(child.tag, child.attrib, child.text)

            # Access specific child elements
            for sub_child in child:
                print(sub_child.tag, sub_child.text)

        return root

def main():
    password = os.getenv('LUXT_PW', 290999)
    ip = os.getenv('LUXT_IP', '192.168.178.84')
    print(f'connecting to {ip} with password {password}')
    lux = Luxtronik(ip, password=password)
    lux.login()
    print(lux.refresh())

if __name__ == '__main__':
    main()
