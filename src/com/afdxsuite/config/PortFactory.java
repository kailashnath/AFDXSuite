package com.afdxsuite.config;

import java.util.ArrayList;

import com.afdxsuite.models.AFDXPort;
import com.afdxsuite.models.InputVl;
import com.afdxsuite.models.OutputVl;
import com.afdxsuite.models.VirtualLink;
import com.afdxsuite.models.VirtualLink.AFDX_PORT;
import com.afdxsuite.models.VirtualLink.DIRECTION;
import com.afdxsuite.models.VirtualLink.PORT_CHARACTERISTIC;
import com.afdxsuite.models.impl.AFDXPortImpl;

public class PortFactory {
	private static ArrayList<InputVl> inputVls = new ArrayList<InputVl>();
	private static ArrayList<OutputVl> outputVls = new ArrayList<OutputVl>();
	
	public static void put(VirtualLink vl) {
		if(vl == null)
			return;
		if(vl.getPortDirection() == DIRECTION.INPUT)
		{
			inputVls.add((InputVl) vl);
		}
		else if (vl.getPortDirection() == DIRECTION.OUTPUT)
		{
			outputVls.add((OutputVl) vl);
		}
	}
	
	private static VirtualLink get(int portId, PORT_CHARACTERISTIC type) {
		for(AFDXPort port : inputVls) {
			if(port.getAfdxPortId() == portId &&
					port.getPortCharacteristic() == type)
				return (VirtualLink) port;
		}
		return null;
	}
	
	private static VirtualLink get(int vlId, DIRECTION direction) {
		if(direction == DIRECTION.INPUT)
			for(VirtualLink link : inputVls) {
				if(link.getVlId() == vlId)
					return link;
			}
		else
			for(VirtualLink link : outputVls) {
				if(link.getVlId() == vlId)
					return link;
			}
		return null;
	}

	public static void WRITE(int afdxPortId, String payload, int payloadLength) {
		
	}
	
	public static AFDXPort READ_Sampling(int samplingPortId) {
		return (AFDXPort) get(samplingPortId, PORT_CHARACTERISTIC.SAMPLING);
	}
	
	public static InputVl READ_Queuing(int queuingPortId) {
		return (InputVl) get(queuingPortId, PORT_CHARACTERISTIC.QUEUING);
	}
	
	public static int getVlCount(DIRECTION vlDirection) {
		if(vlDirection == DIRECTION.INPUT)
			return inputVls.size();
		else if (vlDirection == DIRECTION.OUTPUT)
			return outputVls.size();
		else
			return inputVls.size() + outputVls.size();
	}
	
	public static VirtualLink getInputVl(int vlId) {
		return (InputVl) get(vlId, DIRECTION.INPUT);
	}
	
	public static VirtualLink getOutputVl(int vlId) {
		return (InputVl) get(vlId, DIRECTION.OUTPUT);
	}
}
