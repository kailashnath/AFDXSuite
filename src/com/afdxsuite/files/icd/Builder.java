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
		return vl;
	}
	
	@Inject
	public InputVL buildInputVL(InputVL vl) {
		return vl;
	}
}
