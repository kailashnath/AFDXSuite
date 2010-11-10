package com.afdxsuite.files.icd;

import com.afdxsuite.hardware.configuration.models.vl.InputVL;
import com.afdxsuite.hardware.configuration.models.vl.OutputVL;
import com.google.inject.Inject;

public class Builder {
	
	private String _data;

	public Builder() {
		
	}

	public Builder(String data) {
		_data = data;
	}
	
	public void set_data(String data) {
		_data = data;
	}
	
	@Inject
	public OutputVL buildOutputVL(OutputVL vl) {
		String[] tokens = _data.split(Constants.ICD_DELIMITER);
		for(int i = 0; i < tokens.length; i ++)
		{
			vl.set_port_id(tokens[1]);
			vl.set_port_speed(Short.parseShort(tokens[2]));
			vl.set_port_pin(Short.parseShort(tokens[3]));
			vl.set_line_emc_protection(tokens[4]);
			vl.set_network_id(tokens[5].charAt(0));
			vl.set_connector_name(tokens[6]);
			vl.set_vl_id(Integer.parseInt(tokens[7]));
			vl.set_vl_name(tokens[8]);
			vl.set_network_select(tokens[9]);
			vl.set_bag(Short.parseShort(tokens[10]));
			vl.set_max_frame_size(Integer.parseInt(tokens[11]));
			vl.set_no_sub_vls(Short.parseShort(tokens[12]));
			vl.set_sub_vl_id(Short.parseShort(tokens[13]));
			vl.set_afdx_port_id(Integer.parseInt(tokens[13]));
			vl.set_port_master_name(tokens[14]);
			vl.set_port_type(tokens[15]);
			vl.set_port_characteristic(tokens[16]);
			vl.set_frag_allowed(tokens[17]);
			vl.set_transmission_type(tokens[18]);
			vl.set_src_ip(tokens[19]);
			vl.set_dst_ip(tokens[20]);
			vl.set_src_udp(tokens[21]);
			vl.set_dst_udp(tokens[22]);
			vl.set_buffer_size(Integer.parseInt(tokens[23]));
		}
		return vl;
	}
	
	@Inject
	public InputVL buildInputVL(InputVL vl) {
		return vl;
	}
}
