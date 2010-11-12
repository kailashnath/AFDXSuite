package com.afdxsuite.core.network.manager;

public interface IntegrityHandler {

	public boolean isSequenceNumberValid();
	public void registerRedundancyHandler(RedundancyHandler handler);
	public void notifyRedundancyHandler();
}
