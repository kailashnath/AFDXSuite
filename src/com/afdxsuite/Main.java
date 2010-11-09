package com.afdxsuite;

import com.afdxsuite.application.ApplicationBinder;
import com.afdxsuite.hardware.configuration.Configuration;
import com.afdxsuite.logging.ApplicationLogger;

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		init();
		Configuration config = new Configuration();
	}
	
	private static void init() throws Exception {

		ApplicationLogger.info("Logger initialised successfully");
		ApplicationBinder.buildBinders();
	}

}
