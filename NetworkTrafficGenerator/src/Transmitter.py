from scapy import *
import time

if __name__ == '__main__':
    #reader = PcapReader("/media/6288526D88524029/Airbus/My Received Files/ADIRU/ADIRS_A350_old scripts results and captures/Captures/test_26_OKWL.cap")
    reader = PcapReader("/media/6288526D88524029/Airbus/My Received Files/ADIRU/ADIRS_A350_old scripts results and captures/Captures/test_20_OK.cap")
    packet = None
    i = 0
    while True:

        packet = reader.read_packet()

        if packet == None:
            break
        if i > 6:
            break

        if packet[IP].src in ('10.1.33.2', '1.2.3.4'):
            sendp(packet, iface = "wlan0")

            i += 1
            



