package com.afdxsuite.hardware.configuration.models.vl;

public interface VirtualLink {
	public String get_port_id();
	public void set_port_id(String portId);
	
	public short get_port_speed();
	public void set_port_speed(short portSpeed);
	
	public short get_port_pin();
	public void set_port_pin(short portPin);
	
	public String get_line_emc_protection();
	public void set_line_emc_protection(String lineEmcProtection);
	
	public  char get_network_id();
	public  void set_network_id(char networkId);
	
	public  String get_connector_name();
	public  void set_connector_name(String connectorName);
	
	public  int get_vl_id();
	public  void set_vl_id(int vlId);
	
	public  String get_vl_name();
	public  void set_vl_name(String vlName);
	
	public  String get_network_select();
	public  void set_network_select(String networkSelect);
	
	public short get_bag();
	public void set_bag(short bag);
	
	public int get_max_frame_size();
	public void set_max_frame_size(int maxFrameSize);
	
	public  short get_no_sub_vls();
	public  void set_no_sub_vls(short noSubVls);
	
	public  short get_sub_vl_id();
	public  void set_sub_vl_id(short subVlId);
	
	// Begin : Exclusive InputVL functions
	public boolean is_rma();
	public void set_rma(String rma);
	
	public  boolean is_integration_check_active();
	public  void set_integration_check_active(
			String integrationCheckActive);
	
	public  int get_skew_max();
	public  void set_skew_max(int skewMax);

	// End : Exclusive input vl functions
	
	public  int get_afdx_port_id();
	public  void set_afdx_port_id(int afdxPortId);
	
	public  String get_port_master_name();
	public  void set_port_master_name(String portMasterName);
	
	public  String get_port_type();
	public  void set_port_type(String portType);
	
	public  String get_port_characteristic();
	public  void set_port_characteristic(String portCharacteristic);
	
	public  boolean is_frag_allowed();
	public  void set_frag_allowed(String fragAllowed);
	
	public  String get_transmission_type();
	public  void set_transmission_type(String transmissionType);
	
	public  String get_src_ip();
	public  void set_src_ip(String srcIp);
	
	public  String get_dst_ip();
	public  void set_dst_ip(String dstIp);
	
	public  String get_src_udp();
	public  void set_src_udp(String srcUdp);
	
	public  String get_dst_udp();
	public  void set_dst_udp(String dstUdp);
	
	public  int get_buffer_size();
	public  void set_buffer_size(int bufferSize);
	
	

}
