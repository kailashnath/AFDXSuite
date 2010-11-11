package com.afdxsuite.models;

public interface ICMP {

	// Below is used for replying to echo requests
	public void setDstIpAddress(String ip);
	public String getDstIpAddress();
	
	public void setReplyVlId(int vlId);
	public int getReplyVlId();
	
	public void setReplySubVlId(int subVlId);
	public int getReplySubVlId();

	public void setReplyNetworkSelect(VirtualLink.NETWORK ntwrk);
	public VirtualLink.NETWORK getReplyNetworkSelect();
	
	public void setReplyVlBAG(short bag);
	public short getReplyVlBAG();
	
	public void setReplyVlMFS(int mfs);
	public int getReplyVlMFS();
	
	public void setReplyVlBufferSize(int size);
	public int getReplyVlBufferSize();
	
	// Below is used for sending echo requests
	public void setReceivedVlId(int vlId);
	public int getReceivedVlId();
	
	public void setReceivedNetworkSelect(VirtualLink.NETWORK select);
	public VirtualLink.NETWORK getReceivedNetworkSelect();
	
	public void setReceivedVlBAG(int bag);
	public int getReceivedVlBAG();
	
	public void setReceivedVlSkewMax(int skew);
	public int getReceivedVlSkewMax();
	
	public void setReceivedVlIntegrityChecking(VirtualLink.INTEGRITY_CHECKING check);
	public VirtualLink.INTEGRITY_CHECKING getReceivedVlIntegrityChecking();
	
	public void setRMA(VirtualLink.RMA rma);
	public VirtualLink.RMA getRMA();
	
	public void setReceivedVlMFS(int mfs);
	public int getReceivedVlMFS();
	
	public void setReceivedVlBufferSize(int bfs);
	public int getReceivedVlBufferSize();
	

}
