package com.afdxsuite.logging;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

import com.afdxsuite.application.ApplicationProperties;

public final class ApplicationLogger {
	private static Logger logger = null; 
	
	public static void init(String propsFilename) {
		PropertyConfigurator.configure(propsFilename);
		if(logger == null)
			logger = Logger.getRootLogger();
	}
	
	public static void setLogger(String logName) {
		logger = Logger.getLogger(logName);
	}
	
	public static Logger getLogger() {
		if(logger == null)
			init(ApplicationProperties.get("logger.properties.filename").toString());

		return logger;
	}
	
	public static void debug(String message) {
		getLogger().debug(message);
	}
	
	public static void info(String message) {
		getLogger().info(message);
	}
	
	public static void error(String message) {
		getLogger().error(message);
	}
	
	public static void fatal(String message) {
		getLogger().fatal(message);
	}
}
