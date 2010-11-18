from com.afdxsuite.application.properties import get
from com.afdxsuite.core.network.scapy import load_mib, conf

oid_value_mapping = {}

load_mib(get("AFDXES_MIB"))

for oidname in conf.mib.keys():
    val = conf.mib[oidname]

    val = str(val).replace("enterprises", "1.3.6.1.4.1")

    oid_value_mapping[val] = 0

print 'Loaded AFDX end system MIB objects'


SNMP_IP_MIB_CODE = "afdxProtocolInError"
SNMP_FRAG_MIB_CODE = "iPreassemblyInError"
SNMP_UDP_MIB_CODE  = "afdxUDPCoherencyError"