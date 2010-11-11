package com.afdxsuite.models;

public interface VirtualLink extends AFDXPort {
	
	public enum DIRECTION {
		INPUT,
		OUTPUT,
		BOTH
	}
	
	public enum PORT_CHARACTERISTIC {
		SAP,
		SAMPLING,
		QUEUING
	}
	
	public enum AFDX_PORT {
		SAP,
		COM
	}
	
	public enum PORT_TRANSMISSION {
		UNICAST,
		MULTICAST
	}
	
	public enum NETWORK {
		A,
		B,
		AB
	}
	
	public enum PHYSICAL_PORT {
		PORT1,
		PORT2
	}

	public enum PHYSICAL_PORT_SPEED {
		TEN_Mbps {
			@Override
			public String toString() {
				return "10";
			}
		},
		HUNDRED_Mbps {
			@Override
			public String toString() {
				return "100";
			}
		}
	};
	
	public enum INTEGRITY_CHECKING {
		ACTIVE {
			@Override
			public String toString() {
				return "yes";
			}
		},
		INACTIVE
	}
	
	public enum RMA {
		ACTIVE,
		INACTIVE
	}
	
	public enum FRAGMENTATION {
		YES,
		NO
	}
	
	public void setPortDirection(DIRECTION direction);
	public DIRECTION getPortDirection();
	
	public void setPhysicalPortId(PHYSICAL_PORT portId);
	public PHYSICAL_PORT getPhysicalPortId();

	public void setPhysicalPortSpeed(PHYSICAL_PORT_SPEED speed);
	public PHYSICAL_PORT_SPEED getPhysicalPortSpeed();
	
	public void setPinName(String name);
	public String getPinName();
	
	public void setAFDXLineEMCProtection(String line);
	public String getAFDXLineEMCProtection();
	
	public void setConnectorName(String name);
	public String getConnectorName();

	public void setNetworkId(NETWORK networkId);
	public NETWORK getNetworkId();
	
	public void setVlId(int vlId);
	public int getVlId();
	
	public void setVlName(String name);
	public String getVlName();
	
	public void setNumberOfSubVls(short noOfSubVls);
	public short getNumberOfSubVls();
	
	public void setSubVlId(short subVlId);
	public short getSubVlId();

	public void setAFDXPortMasterName(String name);
	public String getAFDXPortMasterName();
	
	public void setPortType(AFDX_PORT type);
	public AFDX_PORT getPortType();
	
	public void setPortCharacteristic(PORT_CHARACTERISTIC characteristicType);
	public PORT_CHARACTERISTIC getPortCharacteristic();
	
	public void setIpFragmentationAllowed(FRAGMENTATION allowed);
	public FRAGMENTATION getIpFragmentationAllowed();
	
	public void setTransmissionType(PORT_TRANSMISSION type);
	public PORT_TRANSMISSION getTransmissionType();

	public void setSelectedNetwork(NETWORK network);
	public NETWORK getSelectedNetwork();

	public void setBAG(short bag);
	public short getBAG();

	public void setMFS(int mfs);
	public int getMFS();
	
	public void setBufferSize(int size);
	public int getBufferSize();

}
