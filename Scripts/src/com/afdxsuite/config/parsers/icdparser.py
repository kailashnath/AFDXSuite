from com.afdxsuite.config.parsers import ICD_OUTPUT_VL, ICD_INPUT_VL, ICD_ICMP

PORT_SAMPLING = 'Sampling'
PORT_QUEUING  = 'Queuing'
PORT_SAP      = 'SAP'

def intORnull(x):
    if x:
        return int(x)
    return 0

class ICDPARSER(object):
    def __init__(self, data):
        if data and data[0].strip().lower() == self.port_name.lower():
            self.valid = True
            i = 1
            if len(data) > len(self.columns):
                data = data[:len(self.columns) + 1]

            for ele in data[1:]:

                if self.columns_filters.has_key(i):
                    ele = self.columns_filters[i](ele)

                setattr(self, self.columns[i -1], ele)

                i += 1
        else:
            print 'invalid'
            self.valid = False

class ICD_AFDX_OUTPUT_VL(ICDPARSER):
    columns = ("phys_port_id", "phys_port_speed", "pin_name", "afdx_emc_prot", "network_id", "connector_name",
               "vl_id", "vl_name", "network_select", "bag", "max_frame_size", "sub_vl_nb", "sub_vl_id",
               "tx_AFDX_port_id", "AFDX_port_master_name", "AFDX_port_type", "port_characteristic",
               "ip_frag_allowed", "AFDX_unicast", "ip_src", "ip_dst", "udp_src", "udp_dst", "buffer_size")

    columns_filters = { 2:int, 7:int, 10:int, 11:int, 12:int, 13:int, 14:int, 18:lambda x:x.strip().lower()=="yes",
                       19:lambda x:x.lower()=="unicast", 22:int, 23:intORnull, 24:int, }
    
    port_name = ICD_OUTPUT_VL
    def __init__(self, data = None):
        super(ICD_AFDX_OUTPUT_VL, self).__init__(data)

class ICD_AFDX_INPUT_VL(ICDPARSER):

    columns = ("phys_port_id", "phys_port_speed", "pin_name", "afdx_emc_prot", "network_id", "connector_name",
               "vl_id", "vl_name", "network_select", "bag", "max_frame_size", "rma", "ic_active",
               "skew_max", "RX_AFDX_port_id", "AFDX_port_master_name", "AFDX_port_type",
               "port_characteristic", "ip_frag_allowed", "ip_dst", "udp_dst", "buffer_size")
    columns_filters = { 2:int, 7:int, 10:int, 11:int, 12:lambda x:"active" == x.strip().lower(),
                        13:lambda x:x.lower()=="yes", 14:int, 15:int, 19:lambda x:str(x).strip().lower() not in("no" ,''),
                        21:int, 22:int, }    
    port_name = ICD_INPUT_VL

    def __init__(self, data = None):
        super(ICD_AFDX_INPUT_VL, self).__init__(data)

class ICD_AFDX_ICMP(ICDPARSER):
    columns = ("dest_ip", 'reply_vl_id', 'reply_sub_vl_id', 'reply_vl_network_select',
               'reply_vl_bag', 'reply_vl_mfs', 'reply_vl_buffersize', 'rx_vl_id',
               'rx_vl_network_select', 
               'rx_vl_bag', 'rx_vl_skew_max', 'rx_vl_ic', 'rma', 'rx_vl_mfs', 
               'rx_vl_buff_size')

    columns_filters = {2:int}
    port_name = ICD_ICMP

    def __init__(self, data = None):
        super(ICD_AFDX_ICMP, self).__init__(data)
        setattr(self, 'max_frame_size', getattr(self, 'reply_vl_mfs'))


CONFIG_ENTRIES = {ICD_OUTPUT_VL : list(),
                  ICD_INPUT_VL  : list(),
                  ICD_ICMP      : list()}


def parseICD(filename):
    global CONFIG_ENTRIES

    mapping = {ICD_OUTPUT_VL : ICD_AFDX_OUTPUT_VL,
               ICD_INPUT_VL  : ICD_AFDX_INPUT_VL,
               ICD_ICMP      : ICD_AFDX_ICMP}
    obj_dict = {ICD_OUTPUT_VL: [],
                ICD_INPUT_VL : [],
                ICD_ICMP : []}

    file = open(filename)

    for line in file:
        line = str(line).strip()

        if line.startswith('#'):
            continue

        params = str(line).split(';')

        mapping_key = params[0]

        if mapping_key in mapping.keys():

            p = mapping[mapping_key](params)

            if p.valid:
                obj_dict[mapping_key].append(p)
    tx_details = "AFDX_INPUT_VL;port1;100;10;;A;BP;1;VLRXCMD;A&B;128;8192;Active;yes;65500;50025;;AFDX communication port;Queuing;yes;224.224.0.2;50025;8192;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;"
    obj_dict[ICD_INPUT_VL].append(ICD_AFDX_INPUT_VL(tx_details.split(';')))

    CONFIG_ENTRIES = obj_dict
