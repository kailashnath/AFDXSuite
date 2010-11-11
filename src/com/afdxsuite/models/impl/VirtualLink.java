package com.afdxsuite.models.impl;

import com.afdxsuite.models.AFDXPort;
import com.afdxsuite.models.InputVl;
import com.afdxsuite.models.OutputVl;

public class VirtualLink extends AFDXPortImpl implements InputVl, OutputVl,
												AFDXPort {
	private String _afdxLineEMCProtection;

	private String _afdxPortMasterName;
	private short _bag;
	private int _mfs;
	private int _bufferSize;
	private String _connectorName;
	private FRAGMENTATION _ipFragmenation;
	private NETWORK _networkId;
	private short _noOfSubVls;
	private PHYSICAL_PORT _portId;
	private PHYSICAL_PORT_SPEED _portSpeed;
	private String _pinName;
	private DIRECTION _portDirection;
	private AFDX_PORT _portType;
	private NETWORK _selectedNetwork;
	private short _subVlId;
	private PORT_TRANSMISSION _transmissionType;
	private int _vlId;
	private String _vlName;
	private RMA _rma;
	private INTEGRITY_CHECKING _integrityCheck;
	private int _skewMax;
	private String _dstIpAddress;
	private String _srcIpAddress;
	private int _dstUDPPort;
	private int _srcUDPPort;

	@Override
	public String getAFDXLineEMCProtection() {
		return _afdxLineEMCProtection;
	}

	@Override
	public String getAFDXPortMasterName() {
		return _afdxPortMasterName;
	}

	@Override
	public short getBAG() {
		return _bag;
	}

	@Override
	public int getBufferSize() {
		return _bufferSize;
	}

	@Override
	public String getConnectorName() {
		return _connectorName;
	}

	@Override
	public FRAGMENTATION getIpFragmentationAllowed() {
		return _ipFragmenation;
	}

	@Override
	public int getMFS() {
		return _mfs;
	}

	@Override
	public NETWORK getNetworkId() {
		return _networkId;
	}

	@Override
	public short getNumberOfSubVls() {
		return _noOfSubVls;
	}

	@Override
	public PHYSICAL_PORT getPhysicalPortId() {
		return _portId;
	}

	@Override
	public PHYSICAL_PORT_SPEED getPhysicalPortSpeed() {
		return _portSpeed;
	}

	@Override
	public String getPinName() {
		return _pinName;
	}

	@Override
	public DIRECTION getPortDirection() {
		return _portDirection;
	}

	@Override
	public AFDX_PORT getPortType() {
		return _portType;
	}

	@Override
	public NETWORK getSelectedNetwork() {
		return _selectedNetwork;
	}

	@Override
	public short getSubVlId() {
		return _subVlId;
	}

	@Override
	public PORT_TRANSMISSION getTransmissionType() {
		return _transmissionType;
	}

	@Override
	public int getVlId() {
		return _vlId;
	}

	@Override
	public String getVlName() {
		return _vlName;
	}
	@Override
	public String getDstIpAddress() {
		return _dstIpAddress;
	}

	@Override
	public int getDstUDPPort() {
		return _dstUDPPort;
	}

	@Override
	public INTEGRITY_CHECKING getIntegrationCheck() {
		return _integrityCheck;
	}

	@Override
	public RMA getRMA() {
		return _rma;
	}

	@Override
	public int getSkewMax() {
		return _skewMax;
	}

	@Override
	public String getSrcIpAddress() {
		return _srcIpAddress;
	}

	@Override
	public int getSrcUDPPort() {
		return _srcUDPPort;
	}

	@Override
	public void setAFDXLineEMCProtection(String line) {
		_afdxLineEMCProtection = line;
	}

	@Override
	public void setAFDXPortMasterName(String name) {
		_afdxPortMasterName = name;
	}

	@Override
	public void setBAG(short bag) {
		_bag = bag;
	}

	@Override
	public void setBufferSize(int size) {
		_bufferSize = size;
	}

	@Override
	public void setConnectorName(String name) {
		_connectorName = name;
	}

	@Override
	public void setIpFragmentationAllowed(FRAGMENTATION fragmentation) {
		_ipFragmenation = fragmentation;
	}

	@Override
	public void setMFS(int mfs) {
		_mfs = mfs;
	}

	@Override
	public void setNetworkId(NETWORK networkId) {
		_networkId = networkId;
	}

	@Override
	public void setNumberOfSubVls(short noOfSubVls) {
		_noOfSubVls = noOfSubVls;
	}

	@Override
	public void setPhysicalPortId(PHYSICAL_PORT portId) {
		_portId = portId;
	}

	@Override
	public void setPhysicalPortSpeed(PHYSICAL_PORT_SPEED speed) {
		_portSpeed = speed;
	}

	@Override
	public void setPinName(String name) {
		_pinName = name;
	}

	@Override
	public void setPortDirection(DIRECTION direction) {
		_portDirection = direction;
	}

	@Override
	public void setPortType(AFDX_PORT type) {
		_portType = type;
	}

	@Override
	public void setSelectedNetwork(NETWORK network) {
		_selectedNetwork = network;
	}

	@Override
	public void setSubVlId(short subVlId) {
		_subVlId = subVlId;
	}

	@Override
	public void setTransmissionType(PORT_TRANSMISSION type) {
		_transmissionType = type;
	}

	@Override
	public void setVlId(int vlId) {
		_vlId = vlId;
	}

	@Override
	public void setVlName(String name) {
		_vlName = name;
	}



	@Override
	public void setDstIpAddress(String dstip) {
		_dstIpAddress = dstip;
	}

	@Override
	public void setDstUDPPort(int portId) {
		_dstUDPPort = portId;
	}

	@Override
	public void setIntegrationCheck(INTEGRITY_CHECKING status) {
		_integrityCheck = status;
	}

	@Override
	public void setRMA(RMA status) {
		_rma = status;
	}

	@Override
	public void setSkewMax(int skew) {
		_skewMax = skew;
	}

	@Override
	public void setSrcIpAddress(String srcip) {
		_srcIpAddress = srcip;
	}

	@Override
	public void setSrcUDPPort(int portId) {
		_srcUDPPort = portId;
	}

}
