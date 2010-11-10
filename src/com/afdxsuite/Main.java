package com.afdxsuite;

import com.afdxsuite.application.ApplicationBinder;
import com.afdxsuite.hardware.configuration.Configuration;
import com.afdxsuite.logging.ApplicationLogger;

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		init();
		Configuration.loadVLConfiguration();
	}
	
	private static void init() {

		ApplicationLogger.getLogger().info("kailash");
		ApplicationBinder.buildBinders();
	}

}
