package com.afdxsuite.models.impl;

import java.util.Date;

import com.afdxsuite.models.AFDXPort;
import com.afdxsuite.models.VirtualLink.PORT_CHARACTERISTIC;

public class AFDXPortImpl implements AFDXPort {
	private String _message;
	private Date _freshness;
	private int _portId;
	private PORT_CHARACTERISTIC _characteristic;

	public AFDXPortImpl() {
		_message = "";
	}

	@Override
	public void setAfdxPortId(int portId) {
		_portId = portId;
	}
	
	@Override
	public int getAfdxPortId() {
		return _portId;
	}

	
	public void setPortCharacteristic(PORT_CHARACTERISTIC characteristic) {
		_characteristic = characteristic;
	}
	
	public PORT_CHARACTERISTIC getPortCharacteristic() {
		return _characteristic;
	}
	
	@Override
	public void clearMessage() {
		_message = "";		
	}

	@Override
	public Date getFreshnessIndication() {
		return _freshness;
	}

	@Override
	public String readMessage() {
		if(_characteristic == PORT_CHARACTERISTIC.SAMPLING)
			return _message;
		else
		{
			String temp = _message;
			clearMessage();
			return temp;
		}
	}

	@Override
	public void writeMessage(String message) {
		_freshness = new Date();
	}

}
