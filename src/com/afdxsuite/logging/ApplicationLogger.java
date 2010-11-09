package com.afdxsuite.logging;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

import org.apache.log4j.Appender;
import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.ConsoleAppender;
import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

import com.afdxsuite.application.ApplicationProperties;

public final class ApplicationLogger {
	private static Logger logger = null;
	
	private static void init(String propsFilename) {
		File propsFile = new File(propsFilename);
		if(propsFile.exists())
		{
			PropertyConfigurator.configure(propsFilename);
		}
		else
		{
			BasicConfigurator.configure();			
		}
		logger = Logger.getRootLogger();
	}
	
	public static Logger getLogger() {
		try {
			if(logger == null)
				init(ApplicationProperties.get("logger.properties.filename").toString());

			return logger;
		}
		catch(IOException ioe) {
			System.out.println("IOE");
			return Logger.getLogger(""); 
		}
	}

}
