package com.afdxsuite.core.network.receiver;

import java.util.ArrayList;
import java.util.HashMap;

import com.afdxsuite.models.VirtualLink.NETWORK;

import jpcap.PacketReceiver;
import jpcap.packet.Packet;

public class ReceiverListeners implements PacketReceiver {

	private static ReceiverListeners _instance;
	private HashMap<NETWORK, ArrayList<PacketReceiver>> _receivers;
	private NETWORK _networkId = NETWORK.A;

	private ReceiverListeners() {
		_receivers = new HashMap<NETWORK, ArrayList<PacketReceiver>>();
	}
	
	public void setNetworkId(NETWORK network) {
		_networkId = network;
	}
	
	public void registerListener(PacketReceiver receiver) {
		if(!_receivers.containsKey(_networkId))
			_receivers.put(_networkId, new ArrayList<PacketReceiver>());
		_receivers.get(_networkId).add(receiver);
	}
	
	@Override
	public void receivePacket(Packet packet) {
		for(PacketReceiver rx : _receivers.get(_networkId)) {
			rx.receivePacket(packet);
		}
	}
	
	public static ReceiverListeners getInstance() {
		if(_instance == null)
			_instance = new ReceiverListeners();
		return _instance;
	}

}
