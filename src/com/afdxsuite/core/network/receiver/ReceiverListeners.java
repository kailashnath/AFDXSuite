package com.afdxsuite.core.network.receiver;

import java.util.ArrayList;

import jpcap.PacketReceiver;
import jpcap.packet.Packet;

public class ReceiverListeners implements PacketReceiver {

	private static ArrayList<PacketReceiver> receivers = 
		new ArrayList<PacketReceiver>();
	
	public ReceiverListeners() {
		
	}
	
	public static void registerListener(PacketReceiver receiver) {
		receivers.add(receiver);
	}
	
	@Override
	public void receivePacket(Packet packet) {
		for(PacketReceiver rx : receivers) {
			rx.receivePacket(packet);
		}
		
	}
	

}
