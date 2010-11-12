package com.afdxsuite;

import com.afdxsuite.afdx.AFDXListener;
import com.afdxsuite.application.ApplicationBinder;
import com.afdxsuite.application.ApplicationProperties;
import com.afdxsuite.config.parsers.Parser;
import com.afdxsuite.config.parsers.impl.ICDParser;
import com.afdxsuite.core.network.receiver.Receiver;
import com.afdxsuite.core.network.receiver.ReceiverListeners;
import com.afdxsuite.logging.ApplicationLogger;
import com.afdxsuite.models.VirtualLink.NETWORK;

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		init();
		Parser parser = new ICDParser(ApplicationProperties.get("config.icd.file"));
		if(parser.validFile())
			parser.parse();
		
		Receiver rx = new Receiver(NETWORK.A);
		ReceiverListeners.getInstance().registerListener(new AFDXListener());
		rx.start();

		for(int i = 0 ; i < 100 ; i ++) {
			Thread.sleep(100);
		}
		rx.stop();
	}

	private static void init() throws Exception {

		ApplicationLogger.info("Logger initialised successfully");
		ApplicationBinder.buildBinders();
	}
}
