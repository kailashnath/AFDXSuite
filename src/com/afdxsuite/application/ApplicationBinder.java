package com.afdxsuite.application;

import com.afdxsuite.hardware.configuration.ConfigurationModule;
import com.google.inject.Guice;

public class ApplicationBinder {
	
	public static void buildBinders() {
		Guice.createInjector(new ConfigurationModule());
	}

}