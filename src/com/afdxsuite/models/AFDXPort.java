package com.afdxsuite.models;

import java.util.Date;

import com.afdxsuite.models.VirtualLink.PORT_CHARACTERISTIC;

public interface AFDXPort {

	public void setAfdxPortId(int portId);
	public int getAfdxPortId();
	
	public void setPortCharacteristic(PORT_CHARACTERISTIC characteristic);
	public PORT_CHARACTERISTIC getPortCharacteristic();

	public void writeMessage(String message);
	public String readMessage();
	public void clearMessage();
	public Date getFreshnessIndication();
}
