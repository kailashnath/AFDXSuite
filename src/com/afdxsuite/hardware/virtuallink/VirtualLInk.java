package com.afdxsuite.hardware.virtuallink;

public interface VirtualLInk {
	public void setMessage(String message);
	public String getMessage();
	
	public void setMessage(String message, short sub_vl_id);
	public String getMessage(short sub_vl_id);
	
	public void raiseTrap();

}
