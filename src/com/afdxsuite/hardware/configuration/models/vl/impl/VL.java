package com.afdxsuite.hardware.configuration.models.vl.impl;

import com.afdxsuite.hardware.configuration.models.vl.VirtualLink;

public class VL implements VirtualLink {

	private String _port_id;
	private short _port_speed;
	private short _port_pin;
	private String _line_emc_protection;
	private char _network_id;
	private String _connector_name;
	private int _vl_id;
	private String _vl_name;
	private String _network_select;
	private short _bag;
	private int _max_frame_size;
	private short _no_sub_vls;
	private short _sub_vl_id;
	private short _afdx_port_id;
	private String _port_master_name;
	private String _port_type;
	private String _port_characteristic;
	private boolean _frag_allowed;
	private String _transmission_type;
	private String _src_ip;
	private String _dst_ip;
	private String _src_udp;
	private String _dst_udp;
	private int _buffer_size;
	
	private boolean _rma;
	private boolean _integration_check_active;
	private int _skew_max;

	public VL() {}

	public final String get_port_id() {
		return _port_id;
	}

	public final void set_port_id(String portId) {
		_port_id = portId;
	}
	
	public final short get_port_speed() {
		return _port_speed;
	}
	
	public final void set_port_speed(short portSpeed) {
		_port_speed = portSpeed;
	}
	
	public final short get_port_pin() {
		return _port_pin;
	}
	
	public final void set_port_pin(short portPin) {
		_port_pin = portPin;
	}
	
	public final String get_line_emc_protection() {
		return _line_emc_protection;
	}
	
	public final void set_line_emc_protection(String lineEmcProtection) {
		_line_emc_protection = lineEmcProtection;
	}
	
	public final char get_network_id() {
		return _network_id;
	}
	
	public final void set_network_id(char networkId) {
		_network_id = networkId;
	}
	
	public final String get_connector_name() {
		return _connector_name;
	}
	
	public final void set_connector_name(String connectorName) {
		_connector_name = connectorName;
	}
	
	public final int get_vl_id() {
		return _vl_id;
	}
	
	public final void set_vl_id(int vlId) {
		_vl_id = vlId;
	}
	
	public final String get_vl_name() {
		return _vl_name;
	}
	
	public final void set_vl_name(String vlName) {
		_vl_name = vlName;
	}
	
	public final String get_network_select() {
		return _network_select;
	}
	
	public final void set_network_select(String networkSelect) {
		_network_select = networkSelect;
	}
	
	public final short get_bag() {
		return _bag;
	}
	
	public final void set_bag(short bag) {
		_bag = bag;
	}
	
	public final int get_max_frame_size() {
		return _max_frame_size;
	}
	
	public final void set_max_frame_size(int maxFrameSize) {
		_max_frame_size = maxFrameSize;
	}
	
	public final short get_no_sub_vls() {
		return _no_sub_vls;
	}
	
	public final void set_no_sub_vls(short noSubVls) {
		_no_sub_vls = noSubVls;
	}
	
	public final short get_sub_vl_id() {
		return _sub_vl_id;
	}
	
	public final void set_sub_vl_id(short subVlId) {
		_sub_vl_id = subVlId;
	}
	
	public final short get_afdx_port_id() {
		return _afdx_port_id;
	}
	
	public final void set_afdx_port_id(short afdxPortId) {
		_afdx_port_id = afdxPortId;
	}
	
	public final String get_port_master_name() {
		return _port_master_name;
	}
	
	public final void set_port_master_name(String portMasterName) {
		_port_master_name = portMasterName;
	}
	
	public final String get_port_type() {
		return _port_type;
	}
	
	public final void set_port_type(String portType) {
		_port_type = portType;
	}
	
	public final String get_port_characteristic() {
		return _port_characteristic;
	}
	
	public final void set_port_characteristic(String portCharacteristic) {
		_port_characteristic = portCharacteristic;
	}
	
	public final boolean is_frag_allowed() {
		return _frag_allowed;
	}
	
	public final void set_frag_allowed(String fragAllowed) {
		if(fragAllowed.equalsIgnoreCase("yes"))
			_frag_allowed = true;
		else
			_frag_allowed = false;
	}
	
	public final String get_transmission_type() {
		return _transmission_type;
	}
	
	public final void set_transmission_type(String transmissionType) {
		_transmission_type = transmissionType;
	}
	
	public final String get_src_ip() {
		return _src_ip;
	}
	
	public final void set_src_ip(String srcIp) {
		_src_ip = srcIp;
	}
	
	public final String get_dst_ip() {
		return _dst_ip;
	}
	
	public final void set_dst_ip(String dstIp) {
		_dst_ip = dstIp;
	}
	
	public final String get_src_udp() {
		return _src_udp;
	}
	
	public final void set_src_udp(String srcUdp) {
		_src_udp = srcUdp;
	}
	
	public final String get_dst_udp() {
		return _dst_udp;
	}
	
	public final void set_dst_udp(String dstUdp) {
		_dst_udp = dstUdp;
	}
	
	public final int get_buffer_size() {
		return _buffer_size;
	}
	
	public final void set_buffer_size(int bufferSize) {
		_buffer_size = bufferSize;
	}

	public final boolean is_rma() {
		return _rma;
	}

	public final void set_rma(String rma) {
		if(rma.equalsIgnoreCase("active"))
			_rma = true;
		else
			_rma = false;
	}

	public final boolean is_integration_check_active() {
		return _integration_check_active;
	}

	public final void set_integration_check_active(
			String integrationCheckActive) {
		if(integrationCheckActive.equalsIgnoreCase("yes"))
			_integration_check_active = true;
		else
			_integration_check_active = false;
	}

	public final int get_skew_max() {
		return _skew_max;
	}

	public final void set_skew_max(int skewMax) {
		_skew_max = skewMax;
	}



}
