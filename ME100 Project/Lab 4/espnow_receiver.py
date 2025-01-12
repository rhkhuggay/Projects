import network
import espnow

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

while True:
    host, msg = e.recv()
    if msg:             # msg == None if timeout in recv()
        message = str(msg)
        print(message)
        
#         values = message.split(',')
#         
#         right_val = int(values[1])
#         left_val = int(values[2])
        
#         print(f"right: {right_val}, left: {left_val}")
        
#       print(int(str(msg)[5:-1]))
        if msg == b'end':
            break