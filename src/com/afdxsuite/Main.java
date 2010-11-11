package com.afdxsuite;

import jpcap.JpcapCaptor;
import jpcap.PacketReceiver;
import jpcap.packet.Packet;

import com.afdxsuite.application.ApplicationBinder;
import com.afdxsuite.application.ApplicationProperties;
import com.afdxsuite.config.PortFactory;
import com.afdxsuite.config.parsers.Parser;
import com.afdxsuite.config.parsers.impl.ICDParser;
import com.afdxsuite.core.network.receiver.Receiver;
import com.afdxsuite.core.network.receiver.ReceiverListeners;
import com.afdxsuite.logging.ApplicationLogger;
import com.afdxsuite.models.AFDXPort;
import com.afdxsuite.models.InputVl;

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		init();
		Parser parser = new ICDParser(ApplicationProperties.get("config.icd.file"));
		if(parser.validFile())
			parser.parse();

		ReceiverListeners.registerListener(new PacketReceiver() {
			
			@Override
			public void receivePacket(Packet arg0) {
				System.out.println(arg0);
				
			}
		});
		Receiver rx = new Receiver();
		rx.start();
		
		for(int i = 0 ; i < 10 ; i ++) {
			System.out.println("Here");
			Thread.sleep(100);
		}
		rx.stopReceiving();

	}
	
	private static void init() throws Exception {

		ApplicationLogger.info("Logger initialised successfully");
		ApplicationBinder.buildBinders();
	}

}
