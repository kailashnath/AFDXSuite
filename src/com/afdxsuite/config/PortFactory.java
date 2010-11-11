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
	
	public static VirtualLink read(int portId, PORT_CHARACTERISTIC type) {
		for(AFDXPort port : inputVls) {
			if(port.getAfdxPortId() == portId &&
					port.getPortCharacteristic() == type)
				return (VirtualLink) port;
		}
		return null;
	}
	

	public static void WRITE(int afdxPortId, String payload, int payloadLength) {
		
	}
	
	public static AFDXPort READ_Sampling(int samplingPortId) {
		return (AFDXPort) read(samplingPortId, PORT_CHARACTERISTIC.SAMPLING);
	}
	
	public static InputVl READ_Queuing(int queuingPortId) {
		return (InputVl) read(queuingPortId, PORT_CHARACTERISTIC.QUEUING);
	}
	
	public static int getVlCount(DIRECTION vlDirection) {
		if(vlDirection == DIRECTION.INPUT)
			return inputVls.size();
		else if (vlDirection == DIRECTION.OUTPUT)
			return outputVls.size();
		else
			return inputVls.size() + outputVls.size();
	}
}
