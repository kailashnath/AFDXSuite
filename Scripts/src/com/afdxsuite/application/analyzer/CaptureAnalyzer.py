from com.afdxsuite.core.network.scapy import PcapReader, IP, Raw, Ether, \
                                                defrag
from com.afdxsuite.application.properties import get
from com.afdxsuite.application import LOGGER_PARENT_DIRECTORY,\
    CAPTURES_PARENT_DIRECTORY
from com.afdxsuite.logger import Logger

import os
import glob

APPLICATION_CODES = ('EIPC', 'ERPQ', 'ESAP', 'ICMP', 'RRPC', 'RSET', 'TCRQ')

class Analyzer(object):

    def __init__(self):
        self.log_filename = "Analysis-Report.log" 
        self.logger = Logger(LOGGER_PARENT_DIRECTORY, 
                             logger_name = self.log_filename).script_logger

    def printPacketDetails(self, packet, code):
        network = 'A'
        response = 'ERR'

        if str(packet[Ether].src).endswith('40'):
            network = 'B'
            
        if(packet[IP].src == self.src_ip):
            self.logger.info('Sent a packet with %s on network %s' % \
                             (code, network))
        else:
            if 'OK' in packet[Raw]:
                response = 'OK'
            self.logger.info('Received an %s response for %s on network %s' % \
                    (response, code, network))

        '''
        if packet.haslayer(Padding):
            sn = str(packet[Padding]).encode('hex')
            print '%s Sequence number : %d' % ( '-' * 4, int(sn, 16))
        '''


    def start(self):
        if not os.path.exists(CAPTURES_PARENT_DIRECTORY):
            self.logger.error("The directory %s does not exist" % \
                              CAPTURES_PARENT_DIRECTORY)
            return

        count = 0
        for file in glob.glob(os.path.join(CAPTURES_PARENT_DIRECTORY,
                                           "*.cap")):
            self.logger.info("%s Starting analysis for capture %s %s" % 
                             ("=" * 5, file, "=" * 5))
            self.reader = PcapReader(file)
            self.src_ip = get("TE_IP")
            self.dst_ip = get("TR_IP")

            global APPLICATION_CODES
            packets = self.reader.read_all()
            fragd, defragd, _ = defrag(packets)
            packets = fragd + defragd 

            for packet in packets:
                if packet.haslayer(Raw):
                    for code in APPLICATION_CODES:
                        if code in str(packet[Raw]):
                            self.printPacketDetails(packet, code)
            count += 1
        if count == 0:
            self.logger.warn("There are no capture files in directory : %s" % \
                             CAPTURES_PARENT_DIRECTORY)
        else:
            self.logger.info("Successfully analyzed %d capture%s" % \
                             (count, "s" if count > 1 else ""))
            print "Please check the log file %s at %s for the analyzer report" \
            % (self.log_filename, LOGGER_PARENT_DIRECTORY)
