package com.afdxsuite.core.network;

import com.afdxsuite.application.ApplicationProperties;
import com.afdxsuite.config.PortFactory;
import com.afdxsuite.models.VirtualLink;

import jpcap.packet.DatalinkPacket;
import jpcap.packet.EthernetPacket;
import jpcap.packet.IPPacket;
import jpcap.packet.Packet;
import jpcap.packet.UDPPacket;

public class AFDXPacket {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private static String srcMacConstant = ApplicationProperties
												.get("src.mac.constant")
												.toString();
	private static String dstMacConstant = ApplicationProperties
												.get("dst.mac.constant")
												.toString();
	private Packet _packet;
	private VirtualLink _vl_conf;

	public AFDXPacket() {
		if(_packet == null)
			_packet = new Packet();
	}

	public AFDXPacket(Packet packet) {
		System.out.println("Initialized");
		_packet = packet;
		_vl_conf = PortFactory.getInputVl(getDstVlId());
	}
	
	public VirtualLink getConfigVl() {
		return _vl_conf;
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
	
	public short getSequenceNumber() {

		for(int i =0; i < _packet.data.length; i++)
			System.out.print(String.format("%x", _packet.data[i]) + " ");
		EthernetPacket packet = (EthernetPacket) _packet.datalink;

		return _packet.data[_packet.len - 1];
	}
	
	public int getSrcVlId() {
		EthernetPacket ether = (EthernetPacket) _packet.datalink;
		String src = ether.getSourceAddress();
		String vlId = src.substring(src.length() - 5, src.length())
						.replaceAll(":", "");
		return Integer.parseInt(vlId, 16);
	}
	
	public int getDstVlId() {
		EthernetPacket ether = (EthernetPacket) _packet.datalink;
		String dst = ether.getDestinationAddress();
		String vlId = dst.substring(dst.length() - 5, dst.length())
						.replaceAll(":", "");
		return Integer.parseInt(vlId, 16);
	}
	
}
