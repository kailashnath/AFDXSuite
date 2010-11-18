package com.afdxsuite.models;

public interface InputVl extends VirtualLink {
	public static final DIRECTION VL_DIRECTION = DIRECTION.INPUT; 
	public void setRMA(RMA status);
	public RMA getRMA();
	
	public void setIntegrationCheck(INTEGRITY_CHECKING status);
	public INTEGRITY_CHECKING getIntegrationCheck();
	
	public void setSkewMax(int skew);
	public int getSkewMax();

	public void setDstIpAddress(String dstip);
	public String getDstIpAddress();

	public void setDstUDPPort(int portId);
	public int getDstUDPPort();

}
