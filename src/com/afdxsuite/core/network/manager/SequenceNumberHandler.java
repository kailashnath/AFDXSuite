package com.afdxsuite.core.network.manager;

public interface SequenceNumberHandler {

	public short getNextFrameSequenceNumber();
	public short getNextFrameSequenceNumber(short currentSequenceNumber);
	
	public void setExpiredSequenceNumber(short sn, int vlId);
	public void setExpiredAcceptedSequenceNumber(short sn, int vlId);

	public short getPRSN(int vlId);
	public boolean isFirstFrame(int vlId);
	
	public short getPASN(int vlId);
	
}
