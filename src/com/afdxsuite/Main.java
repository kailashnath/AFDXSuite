package com.afdxsuite;

import java.net.InetAddress;

import jpcap.JpcapCaptor;
import jpcap.JpcapSender;
import jpcap.PacketReceiver;
import jpcap.packet.EthernetPacket;
import jpcap.packet.IPPacket;
import jpcap.packet.Packet;
import jpcap.packet.TCPPacket;
import jpcap.packet.UDPPacket;

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
		JpcapSender sender=JpcapSender.openDevice(JpcapCaptor.getDeviceList()[1]);

		//create a TCP packet with specified port numbers, flags, and other parameters
		TCPPacket p=new TCPPacket(12,34,56,78,false,false,false,false,true,true,true,true,10,10);

		//specify IPv4 header parameters
		p.setIPv4Parameter(0,false,false,false,0,false,false,false,0,1010101,100,IPPacket.IPPROTO_TCP,
		  InetAddress.getByName("www.microsoft.com"),InetAddress.getByName("www.google.com"));

		//set the data field of the packet
		p.data=("data").getBytes();

		//create an Ethernet packet (frame)
		EthernetPacket ether=new EthernetPacket();
		//set frame type as IP
		ether.frametype=EthernetPacket.ETHERTYPE_IP;
		//set source and destination MAC addresses
		ether.src_mac=new byte[]{(byte)0,(byte)1,(byte)2,(byte)3,(byte)4,(byte)5};
		ether.dst_mac=new byte[]{(byte)0,(byte)6,(byte)7,(byte)8,(byte)9,(byte)Integer.parseInt("ff", 16)};

		//set the datalink frame of the packet p as ether
		p.datalink=ether;

		//send the packet p
		sender.sendPacket(p);

		sender.close();
		init();
		Parser parser = new ICDParser(ApplicationProperties.get("config.icd.file"));
		if(parser.validFile())
			parser.parse();
		
		Receiver rx = new Receiver(NETWORK.B);
		ReceiverListeners.getInstance().registerListener(new PacketReceiver() {

			@Override
			public void receivePacket(Packet packet) {
				if(packet.datalink instanceof EthernetPacket) {
					EthernetPacket pckt = (EthernetPacket) packet.datalink;
					System.out.println(pckt.getSourceAddress());
				}
			}
		});

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
