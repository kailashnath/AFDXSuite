package com.afdxsuite.hardware.configuration.models.vl;

public interface InputVL {

	public void setPortId(int portId);
	public int getPortId();
	
	public void setPortMasterName(String name);
	public String getPortMasterName();
	
	public void setPortType(short type);
	public short getPortType();
	
	public void setPortCharacteristic(short characteristic);
	public short getPortCharacteristic();
	
	public void setFragmentation(boolean isFragmentation);
	public boolean getFragmentation();
	
	public void setTransmissionType(short type);
	public short getTransmissionType();
	
	public void setSrcIPAddress(String ipaddress);
	public String getSrcIPAddress();
	
	public void setDstIPAddress(String ipaddress);
	public String getIPAddress();
	
	public void setSrcUDPAddress(int port);
	public int getSrcUDPAddress();
	
	public void setDstUDPAddress(int port);
	public int getDstUDPAddress();
	
	public void setBufferSize(int size);
	public int getBufferSize();
}
