package com.afdxsuite.core.network.receiver;

import java.io.IOException;
import java.util.ArrayList;

import org.apache.log4j.Logger;

import com.afdxsuite.logging.ApplicationLogger;

import jpcap.JpcapCaptor;
import jpcap.NetworkInterface;
import jpcap.PacketReceiver;
import jpcap.packet.Packet;

// singleton class
public class Receiver extends Thread {

	private JpcapCaptor _receiver_a;
	private JpcapCaptor _receiver_b;
	private ReceiverListeners _listener;
	private Logger _logger = ApplicationLogger.getLogger();
	
	public Receiver() throws IOException {

		try {
			NetworkInterface[] interfaces = JpcapCaptor.getDeviceList();
			if(interfaces.length < 1) {
				_logger.error("This equipment has no " + 
						"network interfaces defined");
			}
	
			_receiver_a = JpcapCaptor.openDevice(interfaces[0], 65535, true, -1);
			_logger.info("Ethernet interface " + interfaces[0].name + 
					" initialized");
			if(interfaces.length > 1)
			{
				_receiver_b = JpcapCaptor.openDevice(interfaces[1], 65535,
						true, 20);
				_logger.info("Ethernet interface " + interfaces[1].name + 
						" initialized");
			}
	
			_listener = new ReceiverListeners();
			}
		finally {

		}
	}

	public void run() {
		_logger.info("Preparing receiver for receiving packets");
		_receiver_a.setNonBlockingMode(true);
		_receiver_b.setNonBlockingMode(false);
		_receiver_a.loopPacket(-1, _listener);
		//_receiver_b.loopPacket(-1, _listener);
		_logger.info("Completed receiving packets");
	}
	
	public void stopReceiving() {
		_receiver_a.breakLoop();
		_receiver_b.breakLoop();
		_receiver_a.close();
	}
}

class PacketReceiverListener implements PacketReceiver {

	private ArrayList<PacketReceiver> _receivers;

	public PacketReceiverListener() {
		_receivers = new ArrayList<PacketReceiver>();
	}
	
	@Override
	public void receivePacket(Packet p) {
		System.out.println(p);
		for(PacketReceiver rx : _receivers) {
			rx.receivePacket(p);
		}
	}
	
	public void register(PacketReceiver rx) {
		_receivers.add(rx);
	}
}
