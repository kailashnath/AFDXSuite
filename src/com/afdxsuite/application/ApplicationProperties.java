package com.afdxsuite.application;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Properties;

import com.afdxsuite.logging.ApplicationLogger;

public class ApplicationProperties {
	private static Properties props = null;
	
	private static void init() {
		try {
			if(props == null) {
				props = new Properties();
				props.load(new FileInputStream(
						new File("Application.properties")));
			}
		}
		catch(FileNotFoundException fie) {
			ApplicationLogger.getLogger()
			.error("Properties file not found. Reason : " + fie.getMessage());
			fie.printStackTrace();
		}
		catch(IOException ioe) {
			ApplicationLogger.getLogger()
			.error("IO Exception at application properties. Reason : " + 
					ioe.getMessage());
			ioe.printStackTrace();
		}
	}
	
	public static String get(String key) {
		if(props == null)
			init();
		return props.getProperty(key).toString();
	}
}
