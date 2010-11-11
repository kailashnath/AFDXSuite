package com.afdxsuite.models;

public interface OutputVl extends VirtualLink {
	public static final DIRECTION VL_DIRECTION = DIRECTION.OUTPUT;
	public void setSrcIpAddress(String srcip);
	public String getSrcIpAddress();
	
	public void setDstIpAddress(String dstip);
	public String getDstIpAddress();
	
	public void setSrcUDPPort(int portId);
	public int getSrcUDPPort();
	
	public void setDstUDPPort(int portId);
	public int getDstUDPPort();
	
}
