from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers import ICD_ICMP
from com.afdxsuite.application.utilities import buildStaticMessage
from com.afdxsuite.application.properties import get

class Script022(Script):
    application = None
    def __init__(self, application):
        self.application = application
        super(Script022, self).__init__("ITR-ES-022", has_sequences = True)
        self.icmp_ports = self.getPorts({}, ICD_ICMP)

        if len(self.icmp_ports) == 0:
            self.logger.warning("The ICD has no ports satisfying the scripts" \
                                " criteria. Exiting from the script")
            return

    def sequence1(self):
        self.captureForSequence(1)
        msg_8kb = buildStaticMessage(8192, "Message size = 8192")
        msg_64kb = buildStaticMessage(64 * 1024, "Message size = 65536")
        msg = "ping test"
        msgs = [msg_8kb, msg_64kb, msg]
        for port in self.icmp_ports:
            setattr(port, 'ip_src', get("NMF_IP"))
            self.logger.info("Sending an ICMP from NMF ip : %s" % get("NMF_IP"))
            for msg in msgs:
                self.sendICMP(port, msg, False)

    def sequence2(self):
        self.captureForSequence(2)
        msg = "Loopback ping"
        for port in self.icmp_ports:
            setattr(port, 'ip_src', get("TE_IP"))
            self.logger.info("Sending ICMP from TE with ip %s" % get("TE_IP"))
            self.sendICMP(port, msg, False)

    def sequence3(self):
        self.captureForSequence(3)

        msg_small = buildStaticMessage(63, "small message")
        for port in self.icmp_ports:
            setattr(port, 'ip_src', get("NMF_IP"))
            self.logger.info("Sending an ICMP from NMF ip : %s with "\
                             "small message" % get("NMF_IP"))
            self.sendICMP(port, msg_small, False)

        msg_big = buildStaticMessage(65, "big message")
        for port in self.icmp_ports:
            setattr(port, 'ip_src', get("NMF_IP"))
            self.logger.info("Sending an ICMP from NMF ip : %s with "\
                             "big message" % get("NMF_IP"))
            self.sendICMP(port, msg_big, False)

    def run(self):
        self.logger.info("Starting sequence 1")
        self.sequence1()
        self.logger.info("Completed sequence 1")
        self.logger.info("Starting sequence 2")
        self.sequence2()
        self.logger.info("Completed sequence 2")
        self.logger.info("Starting sequence 3")
        self.sequence3()
        self.logger.info("Completed sequence 3")
