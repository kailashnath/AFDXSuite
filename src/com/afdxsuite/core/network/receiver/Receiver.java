package com.afdxsuite.core.network.receiver;

import java.io.IOException;

import org.apache.log4j.Logger;

import com.afdxsuite.logging.ApplicationLogger;
import com.afdxsuite.models.VirtualLink.NETWORK;

import jpcap.JpcapCaptor;
import jpcap.NetworkInterface;

// singleton class
public class Receiver {
	private ReceiverThread _thread_network_A;
	private ReceiverThread _thread_network_B;
	private Logger _logger = ApplicationLogger.getLogger();

	public Receiver(NETWORK network) {
		try {
			if(network == NETWORK.A) {
				_logger.info("Initialising network on interface A");
				_thread_network_A = new ReceiverThread(0);
			}
			else if (network == NETWORK.B) {
				_logger.info("Initialising network on interface B");
				_thread_network_B = new ReceiverThread(1);
			}
			else {
				_logger.info("Initialising network on both interfaces A&B");
				_thread_network_A = new ReceiverThread(0);
				_thread_network_B = new ReceiverThread(1);
			}
		}
		catch(IOException ioe) {
			_logger.error("Failed initialising receiver. Reason : " + 
					ioe.getMessage());
			ioe.printStackTrace();
		}
	}
	
	public void start() {
		if(_thread_network_A != null) {
			_thread_network_A.start();
		}
		if(_thread_network_B != null) {
			_thread_network_B.start();
		}
	}
	
	public void stop() {
		if(_thread_network_A != null) {
			_thread_network_A.stopReceiver();
		}
		if(_thread_network_B != null) {
			_thread_network_B.stopReceiver();
		}
	}
}

class ReceiverThread extends Thread {

	private NetworkInterface _network;
	private JpcapCaptor _receiver;
	private ReceiverListeners _listener;
	private Logger _logger = ApplicationLogger.getLogger();

	public ReceiverThread(int network) throws ArrayIndexOutOfBoundsException,
	IOException {
		_network = JpcapCaptor.getDeviceList()[network];
		_receiver = JpcapCaptor.openDevice(_network, 65535, true, -1);
		_logger.info("Successfully opened network interface on :" + 
				_network.name);
		_listener = ReceiverListeners.getInstance();
	}

	public void run() {
		_logger.info("Preparing receiver for receiving packets");
		_receiver.setNonBlockingMode(true);
		_receiver.loopPacket(-1, _listener);
	}

	public void stopReceiver() {
		_receiver.breakLoop();
		_receiver.close();
	}
}
