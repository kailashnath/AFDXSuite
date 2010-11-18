package com.afdxsuite.core.network.manager;

import java.util.ArrayList;

import com.afdxsuite.core.network.AFDXPacket;

public class Normalizer {
	private ArrayList<AFDXPacket> _fragmentedPackets;
	
	public Normalizer() {
		_fragmentedPackets = new ArrayList<AFDXPacket>();
	}
	
	public void notify(AFDXPacket packet) {
		System.out.println("Normalizer");
	}
}
