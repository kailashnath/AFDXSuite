package com.afdxsuite.core.network.manager;

public interface RedundancyHandler {
	public static final short SKEW_TIME_MILLIS = 66;

	public boolean isRedundantFrame(short sn, int vl);
	public void startRedundancyCheck();
	public boolean isPassed();
	public void registerNormalizer(Normalizer normalizer);
}
