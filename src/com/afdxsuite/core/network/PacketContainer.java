package com.afdxsuite.core.network;

import java.util.ArrayList;

import jpcap.packet.Packet;

public class PacketContainer {
	public static ArrayList<Packet> receivedPackets = new ArrayList<Packet>();
	
	public static void put(Packet packet) {
		receivedPackets.add(packet);
		if(receivedPackets.size() > 200) {
			for(int i = 0 ; i < 100 ; i++)
			receivedPackets.remove(i);
		}
	}

}
