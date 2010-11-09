package com.afdxsuite.hardware.configuration;

import java.util.ArrayList;

import com.afdxsuite.hardware.configuration.models.vl.InputVL;
import com.afdxsuite.hardware.configuration.models.vl.OutputVL;

public class Container {
	private static ArrayList<InputVL> inputVls = new ArrayList<InputVL>();
	private static ArrayList<OutputVL> outputVls = new ArrayList<OutputVL>();

	public static void addVl(InputVL vl) {
		inputVls.add((InputVL) vl);
	}
	
	public static void addVl(OutputVL vl) {
		outputVls.add(vl);
	}
	
	public static ArrayList<InputVL> getInputVls() {
		return inputVls;
	}
	
	public static ArrayList<OutputVL> getOutputVls() {
		return outputVls;
	}
}
