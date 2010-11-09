package com.afdxsuite.hardware.configuration;

import java.io.IOException;

import com.afdxsuite.application.ApplicationProperties;
import com.afdxsuite.files.icd.Parser;

public class Configuration {
	Parser icdParser;

	public Configuration() {
		try {
		     icdParser = new Parser(
						ApplicationProperties.get("config.icd.file"));
		}
		catch(IOException iex) {
			
		}
	}
}
