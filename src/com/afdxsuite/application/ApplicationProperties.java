package com.afdxsuite.application;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Properties;

public class ApplicationProperties {
	private static Properties props = null;
	
	private static void init() throws IOException, FileNotFoundException {
		if(props == null) {
			props = new Properties();
			props.load(new FileInputStream(new File("Application.properties")));
		}
	}
	
	public static String get(String key) throws IOException, 
												FileNotFoundException {
		if(props == null)
			init();
		return props.getProperty(key).toString();
	}
}
