package com.afdxsuite.hardware.configuration;

import java.io.IOException;

import com.afdxsuite.application.ApplicationProperties;
import com.afdxsuite.files.icd.Parser;
import com.afdxsuite.logging.ApplicationLogger;

public class Configuration {
	
	public static boolean loadVLConfiguration() {
		try {
		     new Parser(ApplicationProperties.get("config.icd.file"));
		     return true;
		}
		catch(IOException iex) {
			ApplicationLogger.getLogger().error("Couldn't find the provided " +
					"icd file on the system. : " + iex.getMessage());
			return false;
		}		
	}
	
	public static void buildHardwareFromConfiguration() {
		// should create the virtual links, ports and map them together
		
	}
}
