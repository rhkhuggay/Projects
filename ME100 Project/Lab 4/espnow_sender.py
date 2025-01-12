import network
import espnow

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)
#peer = b'\x44\x17\x93\x5C\x0B\x44'   # MAC address of peer's wifi interface
peer = b'\x00\x00\x00\x00\x00\x00'
e.add_peer(peer)      # Must add_peer() beforee send()

e.send(peer, "Starting...")
for i in range(100):
    e.send(peer, "Hi! I've sent this many messages: " + str(i), True)
    # Arguments for send are Mac address of receiver, message string, and whether or not to wait for a
    #confirmation from the receiver that the message has been received before moving on from this line (good for debugging). 
e.send(peer, b'end')
