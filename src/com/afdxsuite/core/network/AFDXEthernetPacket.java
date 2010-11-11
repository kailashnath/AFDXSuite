package com.afdxsuite.core.network;

import com.afdxsuite.application.ApplicationProperties;

import jpcap.packet.EthernetPacket;
import jpcap.packet.Packet;

public class AFDXEthernetPacket {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private Packet _packet;
	private static String srcMacConstant = ApplicationProperties
												.get("src.mac.constant")
												.toString();
	private static String dstMacConstant = ApplicationProperties
												.get("dst.mac.constant")
												.toString();
	public AFDXEthernetPacket() {
		_packet = new Packet();
	}

	public AFDXEthernetPacket(Packet packet) {
		_packet = packet;
	}
	
	public void setSrcVlId(int vlId) {
		String macVl = String.format("%04x", vlId);
		macVl = srcMacConstant + ":" + macVl.substring(0, 2) + ":" 
					+ macVl.substring(2, 4);
		String[] vals = macVl.split(":");
		byte[] mac = new byte[6];
		for(int i = 0; i < 6; i++) {
			mac[i] = (byte)Integer.parseInt(vals[i], 16);
		}
		((EthernetPacket)_packet.datalink).src_mac = mac;
	}
	
	public void setDstVlId(int vlId) {
		String macVl = String.format("%04x", vlId);
		macVl = dstMacConstant + ":" + macVl.substring(0, 2) + ":" 
					+ macVl.substring(2, 4);
		String[] vals = macVl.split(":");
		byte[] mac = new byte[6];
		for(int i = 0; i < 6; i++) {
			mac[i] = (byte)Integer.parseInt(vals[i], 16);
		}
		((EthernetPacket)_packet.datalink).dst_mac = mac;
	}
	
	public void setSequenceNumber(int sn) {
		
	}
}
