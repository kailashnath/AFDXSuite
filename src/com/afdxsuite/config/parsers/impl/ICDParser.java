package com.afdxsuite.config.parsers.impl;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;

import com.afdxsuite.config.PortFactory;
import com.afdxsuite.config.parsers.Parser;
import com.afdxsuite.logging.ApplicationLogger;
import com.afdxsuite.models.AFDXPort;
import com.afdxsuite.models.InputVl;
import com.afdxsuite.models.OutputVl;
import com.afdxsuite.models.VirtualLink;
import com.afdxsuite.models.VirtualLink.AFDX_PORT;
import com.afdxsuite.models.VirtualLink.DIRECTION;
import com.afdxsuite.models.VirtualLink.FRAGMENTATION;
import com.afdxsuite.models.VirtualLink.INTEGRITY_CHECKING;
import com.afdxsuite.models.VirtualLink.NETWORK;
import com.afdxsuite.models.VirtualLink.PHYSICAL_PORT;
import com.afdxsuite.models.VirtualLink.PHYSICAL_PORT_SPEED;
import com.afdxsuite.models.VirtualLink.PORT_CHARACTERISTIC;
import com.afdxsuite.models.VirtualLink.PORT_TRANSMISSION;
import com.afdxsuite.models.VirtualLink.RMA;

public class ICDParser implements Parser {

	private static final String DELIMITER = ";";
	private static final String REJECT_CHAR = "#";
	private static final String INPUT_VL = "AFDX_INPUT_VL";
	private static final String OUTPUT_VL = "AFDX_OUTPUT_VL";

	private BufferedReader _reader;
	private boolean _fileValid;
	
	public ICDParser(String filename) {
		try {
			_reader = new BufferedReader(new InputStreamReader(
					new FileInputStream(filename)));
			_fileValid = true;
		}
		catch (FileNotFoundException e) {
			ApplicationLogger.getLogger().error("ICD file not found. Please " +
					"check the properties file.");
			e.printStackTrace();
			_fileValid = false;
		}
	}

	@Override
	public void parse() throws IOException {
		String line;
		while((line = _reader.readLine()) != null) {
			if(line.startsWith(ICDParser.REJECT_CHAR)) {
				continue;
			}
			line = line.replaceAll(";;", ";0;");
			String[] tokens = line.split(ICDParser.DELIMITER);
			
			PortFactory.put(parseToVirtualLink(tokens));
		}
	}

	@Override
	public boolean validFile() {
		return _fileValid;
	}
	
	private VirtualLink parseToVirtualLink(String[] tokens) {
		VirtualLink vl = new com.afdxsuite.models.impl.VirtualLink();
		if(tokens[0].startsWith(ICDParser.INPUT_VL)) {
			vl.setPortDirection(DIRECTION.INPUT);
			((InputVl) vl).setRMA(tokens[12]
                             .equalsIgnoreCase(RMA.ACTIVE.toString()) ? 
                            		 RMA.ACTIVE : RMA.INACTIVE);
			((InputVl) vl).setIntegrationCheck(tokens[13]
                              .equalsIgnoreCase(
                            		  INTEGRITY_CHECKING.ACTIVE.toString()) ?
                        				  INTEGRITY_CHECKING.ACTIVE : 
                            			  INTEGRITY_CHECKING.INACTIVE);
			((InputVl) vl).setSkewMax(Integer.parseInt(tokens[14]));
			((AFDXPort) vl).setAfdxPortId(Integer.parseInt(tokens[15]));
			vl.setAFDXPortMasterName(tokens[16]);
			vl.setPortType(tokens[17]
			                      .equalsIgnoreCase(AFDX_PORT.SAP.toString()) ? 
			                    		  AFDX_PORT.SAP : AFDX_PORT.COM);
			if(tokens[18].equalsIgnoreCase(
					PORT_CHARACTERISTIC.SAMPLING.toString()))
				vl.setPortCharacteristic(PORT_CHARACTERISTIC.SAMPLING);
			else if (tokens[18].equalsIgnoreCase(
					PORT_CHARACTERISTIC.QUEUING.toString()))
				vl.setPortCharacteristic(PORT_CHARACTERISTIC.QUEUING);
			else
				vl.setPortCharacteristic(PORT_CHARACTERISTIC.SAP);
			
			vl.setIpFragmentationAllowed(tokens[19]
                .equalsIgnoreCase(FRAGMENTATION.YES.toString()) ?
					FRAGMENTATION.YES : FRAGMENTATION.NO);
			((InputVl) vl).setDstIpAddress(tokens[20]);
			((InputVl) vl).setDstUDPPort(Integer.parseInt(tokens[21]));
			vl.setBufferSize(Integer.parseInt(tokens[22]));
		}
		else if (tokens[0].startsWith(ICDParser.OUTPUT_VL)) {
			vl.setPortDirection(DIRECTION.OUTPUT);
			vl.setNumberOfSubVls(Short.parseShort(tokens[12]));
			vl.setSubVlId(Short.parseShort(tokens[13]));
			((AFDXPort) vl).setAfdxPortId(Integer.parseInt(tokens[14]));
			vl.setAFDXPortMasterName(tokens[15]);
			vl.setPortType(tokens[16]
			                      .equalsIgnoreCase(AFDX_PORT.SAP.toString()) ? 
			                    		  AFDX_PORT.SAP : AFDX_PORT.COM);
			if(tokens[17].equalsIgnoreCase(
					PORT_CHARACTERISTIC.SAMPLING.toString()))
				vl.setPortCharacteristic(PORT_CHARACTERISTIC.SAMPLING);
			else if (tokens[17].equalsIgnoreCase(
					PORT_CHARACTERISTIC.QUEUING.toString()))
				vl.setPortCharacteristic(PORT_CHARACTERISTIC.QUEUING);
			else
				vl.setPortCharacteristic(PORT_CHARACTERISTIC.SAP);
			
			vl.setIpFragmentationAllowed(tokens[18]
                .equalsIgnoreCase(FRAGMENTATION.YES.toString()) ?
					FRAGMENTATION.YES : FRAGMENTATION.NO);
			
			vl.setTransmissionType(tokens[19]
                  .equalsIgnoreCase(PORT_TRANSMISSION.UNICAST.toString())?
					PORT_TRANSMISSION.UNICAST : PORT_TRANSMISSION.MULTICAST);
			((OutputVl) vl).setSrcIpAddress(tokens[20]);
			((OutputVl) vl).setDstIpAddress(tokens[21]);
			((OutputVl) vl).setSrcUDPPort(Integer.parseInt(tokens[22]));
			((OutputVl) vl).setDstUDPPort(Integer.parseInt(tokens[23]));
			vl.setBufferSize(Integer.parseInt(tokens[24]));
		}
		else {
			return null;
		}
		
		
		vl.setPhysicalPortId(tokens[1]
		   .equalsIgnoreCase(PHYSICAL_PORT.PORT1.toString()) ?
		  		  PHYSICAL_PORT.PORT1 : PHYSICAL_PORT.PORT2);
		
		vl.setPhysicalPortSpeed(tokens[2]
           .equalsIgnoreCase(PHYSICAL_PORT_SPEED.TEN_Mbps.toString()) ? 
				PHYSICAL_PORT_SPEED.TEN_Mbps : 
					PHYSICAL_PORT_SPEED.HUNDRED_Mbps);
		
		vl.setPinName(tokens[3]);
		vl.setAFDXLineEMCProtection(tokens[4]);
		vl.setNetworkId(tokens[5].equalsIgnoreCase(NETWORK.A.toString()) ?
				NETWORK.A : NETWORK.B);
		vl.setConnectorName(tokens[6]);
		vl.setVlId(Integer.parseInt(tokens[7]));
		vl.setVlName(tokens[8]);
		if(tokens[9].equalsIgnoreCase(NETWORK.A.toString()))
			vl.setSelectedNetwork(NETWORK.A);
		else if(tokens[9].equalsIgnoreCase(NETWORK.B.toString()))
			vl.setSelectedNetwork(NETWORK.B);
		else
			vl.setSelectedNetwork(NETWORK.AB);
		vl.setBAG(Short.parseShort(tokens[10]));
		vl.setMFS(Integer.parseInt(tokens[11]));
		
		
			
			
		return vl;
	}
}
