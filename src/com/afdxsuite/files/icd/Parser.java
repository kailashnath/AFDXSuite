package com.afdxsuite.files.icd;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;

import com.afdxsuite.hardware.configuration.Container;
import com.afdxsuite.hardware.configuration.models.vl.impl.VL;
import com.afdxsuite.logging.ApplicationLogger;

public class Parser {
	private InputStreamReader iStreamReader;
	
	public Parser(String filename) throws FileNotFoundException {
		try {
			ApplicationLogger.getLogger().info("Reading the ICD file from location " +
					filename);
			iStreamReader = new InputStreamReader(
								new FileInputStream(
										new File(filename)));
			parse();
		}
		catch(FileNotFoundException ex)
		{
			ApplicationLogger.getLogger().error("ICD file missing in the location : " +
					filename);
			ex.printStackTrace();
			throw ex;
		}
	}
	
	private void parse() {
		BufferedReader reader = new BufferedReader(iStreamReader);
		String line;
		Builder objBuilder = new Builder();
		try {
			while((line = reader.readLine()) != null) {

				if (line.charAt(0) == Constants.LINE_DISCARD_CHAR)
					continue;

				objBuilder.set_data(line);
				if (line.startsWith(Constants.AFDX_INPUT_VL)) {
					Container.addVl(
							objBuilder.buildInputVL(new VL())
							);
				}
				else if (line.startsWith(Constants.AFDX_OUTPUT_VL)) {
					Container.addVl(
							objBuilder.buildOutputVL(new VL())
							);
				}
			}
		}
		catch(IOException iex) {
			ApplicationLogger.getLogger().error("Error occured while trying to parse the" +
					" icd file. Reason : " + iex.getMessage());
			iex.printStackTrace();
		}
		finally {
			ApplicationLogger.getLogger().info("Loaded " + Container.getInputVls().size() +
					" input vls and " + Container.getOutputVls().size() + 
					" output vls");
		}
	}
}
