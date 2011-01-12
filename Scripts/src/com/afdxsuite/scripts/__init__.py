from com.afdxsuite.core.network.receiver.Receiver import IReceiver, Receiver
from com.afdxsuite.core.network.scapy import PcapWriter, conf
from com.afdxsuite.application import CAPTURES_PARENT_DIRECTORY,\
    LOGGER_PARENT_DIRECTORY
from com.afdxsuite.logger import Logger, general_logger
from com.afdxsuite.config import Factory
from com.afdxsuite.application.commands.RSET import RSET
from com.afdxsuite.application.utilities import pollForResponse
from com.afdxsuite.application.properties import get
from com.afdxsuite.core.network import NETWORK_AB, NETWORK_A

import os
import sys
import time
import traceback

class ScriptReceiver(IReceiver):
    __writer = None
    __filter = None
    __scriptName = None
    __filename = None
    __lockOnCapture = False
    __captures = None

    def __init__(self, scriptName):
        self.__scriptName = scriptName
        print 'Initialising receiver for script : %s' % scriptName

    def start(self, seqno = 0):

        if seqno > 0:
            self.stop()

        self.__captures = []
        if seqno > 0:
            filename = self.__scriptName + "_SEQ" + str(seqno) + ".cap"
        else:
            filename = self.__scriptName + ".cap"

        self.__filename = filename
        self.__lockOnCapture = False

    def notify(self, packet):

        if self.__lockOnCapture:
            return

        if self.__filter != None:
            if not self.__filter(packet):
                return
        try:
            self.__captures.append(packet)
        except Exception, ex:
            general_logger.warning("Error at Script notify function : %s" % \
                                   str(ex))
            general_logger.error("Error with capturing for script %s" % \
                                 self.__scriptName)

    def setFilter(self, filterfunc):
        self.__filter = filterfunc

    def stop(self):

        try:
            if self.__captures != None and len(self.__captures) > 0:

                filename = self.__filename
                if os.path.exists(CAPTURES_PARENT_DIRECTORY + "/" + filename):
                        os.remove(CAPTURES_PARENT_DIRECTORY + "/" + filename)
                filename = CAPTURES_PARENT_DIRECTORY + "/" + filename
                time.sleep(1)
                self.__writer = PcapWriter(filename)
                self.__lockOnCapture = True
                self.__writer.write(self.__captures)
                self.__writer.flush()
                self.__writer.close()
        except Exception, ex:
            general_logger.error("Could not write to capture file from script" \
                                 " receiver handler : %s" % str(ex))
            general_logger.error("Crash", exc_info = 1)
            traceback.print_exc(file = sys.stdout)
        finally:            
            self.__writer = None
            self.__captures = None

class Script(object):
    __receiver = None
    __scriptName = None
    logger = general_logger
    network  = NETWORK_A

    def __init__(self, name, has_sequences = False):
        self.logger = \
        Logger(LOGGER_PARENT_DIRECTORY, logger_name = name).script_logger
        self.logger.info("Intialising the script " + name)
        self.__receiver = ScriptReceiver(name)

        if not has_sequences:
            self.__receiver.start()

        self.__scriptName = name
        Receiver.register(self.__receiver, NETWORK_AB)

    def captureForSequence(self, seqNo):
        self.__receiver.start(seqNo)

    def getPorts(self, filter, port_type):
        result_ports = []
        ports = Factory.GET_Ports(None, port_type)
    
        for port in ports:
            if type(filter) == dict:
                add = True
                for key in filter.keys():
                    if hasattr(port, key):
                        lhs_val = getattr(port, key)
                        rhs_val = filter[key]
                        if type(rhs_val) in (list, tuple):
                            condition = lhs_val in rhs_val
                        else:
                            condition = lhs_val == rhs_val
                        if not condition:
                            add = False
                            break
                    else:
                        add = False
                        break
                if add:
                    result_ports.append(port)
            else:
                if filter(port):
                    result_ports.append(port)
    
        return result_ports

    def remove_common_ports(self, ports):
        filtered_ports = []
        for port in ports:
            if hasattr(port, 'udp_src'):
                val = port.udp_src
            elif hasattr(port, 'udp_dst'):
                val = port.udp_dst
            if val in (int(get("TE_UDP")), int(get("SNMP_UDP_PORT"))) or \
            (hasattr(port, 'vl_id') and \
             int(port.vl_id) in (int(get("TE_TX_VL")),int(get("TE_RX_VL")))):
                continue
            filtered_ports.append(port)
        return filtered_ports

    def send(self, payload, ports):

        if type(ports) != list:
            ports = [ports]

        for port in ports:
            outport = Factory.WRITE(port.RX_AFDX_port_id, payload)

            self.application.transmitter.transmit(outport, self.network)

    def sendRSET(self, poll = True):
        rset = RSET()
        self.logger.info("Sent an RSET command")
        self.send(rset.buildCommand(), Factory.GET_TX_Port())
        if not poll:
            return
        if not pollForResponse('OK'):
            self.logger.warn("The ES has not responded to RSET")


    def sendICMP(self, port, message, poll = True):
        port = Factory.WRITE_ICMP(port.rx_vl_id, message)
        self.application.transmitter.transmit(port, self.network)
        if poll:
            pollForResponse(message, timeout = 1)

    def stop(self):
        self.logger.info("Stopping the script " + self.__scriptName)
        Receiver.deregister(self.__receiver, NETWORK_AB)
        self.__receiver.stop()

    def getMIBGroup(self, group_name, extra_id = None):
        oid_lst = []
        for key in conf.mib.keys():
            if group_name in key and len(key) > len(group_name) and "Group" not in key:
                oid_value = conf.mib[key]
                oid_lst.append(oid_value)
    
        oid_lst.sort()
        return oid_lst

    def getAFDXEquipmentGroup(self):
        mib_group = [conf.mib['afdxEquipmentDesignation'],
                     conf.mib['afdxEquipmentPN'],
                     conf.mib['afdxEquipmentSN'],
                     conf.mib['afdxEquipmentLN'],
                     conf.mib['afdxEquipmentStatus'],
                     conf.mib['afdxEquipmentLocation'],
                     conf.mib['afdxEquipmentUpTime']]
        return mib_group

    def getAFDXMacGroup(self):
        mib_group = [conf.mib['afdxMACAddress'],
                     conf.mib['afdxMACStatus'],
                     conf.mib['afdxMACInOctets'],
                     conf.mib['afdxMACOutOctets'],
                     conf.mib['afdxMACTotalInErrors'],
                     conf.mib['afdxMACDestAddrErrors'],
                     conf.mib['afdxMACAlignmentErrors'],
                     conf.mib['afdxMACRCErrors'],
                     conf.mib['afdxMACFrameLengthErrors'],
                     conf.mib['afdxMACIntMacRxErrors']]
        return mib_group
