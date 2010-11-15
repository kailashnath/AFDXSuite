package com.afdxsuite.core.network.manager;

import java.util.HashMap;

import org.apache.log4j.Logger;

import com.afdxsuite.core.network.AFDXPacket;
import com.afdxsuite.logging.ApplicationLogger;
import com.afdxsuite.models.InputVl;
import com.afdxsuite.models.VirtualLink.INTEGRITY_CHECKING;
import com.afdxsuite.models.VirtualLink.RMA;

public class PacketHandler implements IntegrityHandler, RedundancyHandler,
										SequenceNumberHandler {
	public static PacketHandler _instance;
	private AFDXPacket _packet;
	private HashMap<Integer, Short> _prsn = new HashMap<Integer, Short>();
	private HashMap<Integer, Short> _pasn = new HashMap<Integer, Short>();
	
	private Normalizer _normalizer;
	private RedundancyHandler _redundancy_handler;
	private IntegrityHandler _integrity_handler;
	private Logger _logger;
	
	private int _firstFrameVlId;
	private boolean _redundancy_passed = false;

	private PacketHandler() {
		_logger = ApplicationLogger.getLogger();
	}
	
	public static PacketHandler getInstance() {
		// double check locking. Thread safe
		if(_instance == null) {
			synchronized (PacketHandler.class) {
				_instance = new PacketHandler();
			};
		}
		return _instance;
	}
	
	public void onReceive(AFDXPacket packet) {
		_packet = packet;
		System.out.println("In on receive");
		if(_packet.getConfigVl() != null)
		{
			if(((InputVl)_packet.getConfigVl()).getIntegrationCheck() == 
												INTEGRITY_CHECKING.ACTIVE)
			{
				_logger.info("Starting integration check on the packet");
				if(_integrity_handler.isSequenceNumberValid()) {
					_logger.info("Packet has passed the integration check " + 
							"successfully");
					if(((InputVl)_packet.getConfigVl()).getRMA() == RMA.ACTIVE)
						_integrity_handler.notifyRedundancyHandler();
				}
				else {
					_logger.error("The packet has failed with integrity check");
				}
			}
			else {
				_logger.info("This vl does not support integration check");
				System.out.println(_packet.getDstVlId());
			}
		}
		else {
			_logger.error("No entry in configuration file for the given vl");
		}
	}
	
	@Override
	public boolean isSequenceNumberValid() {
		if(_packet == null) {
			_logger.warn("No Packet to work on.");
			return false;
		}
		short current_sn = _packet.getSequenceNumber();
		_logger.info("Sequence number is " + current_sn);
		int vlId 		 = _packet.getDstVlId();

		short prsn 			 = getPRSN(_packet.getDstVlId());
		short prsn_next 	 = getNextFrameSequenceNumber(prsn);
		short prsn_next_next = getNextFrameSequenceNumber(prsn_next);

		if((current_sn == prsn_next || current_sn == prsn_next_next) ||
				(current_sn == 0 && prsn != 0) ||
				(isFirstFrame(vlId)))
		{
			setExpiredSequenceNumber(current_sn, vlId);
			return true;
		}
		return false;
	}

	@Override
	public short getNextFrameSequenceNumber() {
		if(_packet == null) {
			_logger.warn("No Packet to work on. Failed getting frame " + 
					"sequence number");
		}
		return 0;
	}

	@Override
	public short getNextFrameSequenceNumber(short currentSequenceNumber) {
		if(currentSequenceNumber == 255)
			return 1;
		else
			return (short)(currentSequenceNumber + 1);
	}

	@Override
	public short getPRSN(int vlId) {
		if(_prsn.containsKey(vlId)) {
			return _prsn.get(vlId);
		}
		else {
			_prsn.put(vlId, (short)0);
			_firstFrameVlId = vlId;
			return 0;
		}
	}

	@Override
	public boolean isFirstFrame(int vlId) {
		return vlId == _firstFrameVlId ? true : false;
	}

	@Override
	public void setExpiredSequenceNumber(short sn, int vlId) {
			_prsn.put(vlId, sn);
	}
	
	@Override
	public void setExpiredAcceptedSequenceNumber(short sn, int vlId) {
		_pasn.put(vlId, sn);
	}

	@Override
	public boolean isPassed() {
		return _redundancy_passed;
	}

	@Override
	public void startRedundancyCheck() {
		_redundancy_passed = isRedundantFrame();
		if(_redundancy_passed) {
			_logger.info("The packet has passed the redundancy check");
		}
		else {
			_logger.error("The packet has failed with redundancy check");
		}
	}

	@Override
	public short getPASN(int vlId) {
		if(_pasn.containsKey(vlId)) {
			return _pasn.get(vlId);
		}
		else {
			_pasn.put(vlId, (short) 0);
			return 0;
		}
	}

	public boolean isRedundantFrame() {
		return isRedundantFrame(_packet.getSequenceNumber(), 
				_packet.getDstVlId());				
	}
	
	@Override
	public boolean isRedundantFrame(short sn, int vlId) {
		short rsn = _packet.getSequenceNumber();
		short pasn = getPASN(vlId);
		if(isFirstFrame(vlId) ||
				(rsn >= pasn + 1 && rsn <= pasn + 66))
		{
			setExpiredAcceptedSequenceNumber(sn, vlId);
			return true;
		}
		return false;
	}
	
	@Override
	public void notifyRedundancyHandler() {
		if(_redundancy_handler != null)
		{
			_redundancy_handler.startRedundancyCheck();

			if(_redundancy_handler.isPassed())
				if(_normalizer != null)
					_normalizer.notify(_packet);
		}
	}
	
	@Override
	public void registerRedundancyHandler(RedundancyHandler handler) {
		_redundancy_handler = handler;
	}

	@Override
	public void registerNormalizer(Normalizer normalizer) {
		_normalizer = normalizer;
	}
	
	public void registerIntegrityHandler(IntegrityHandler handler) {
		_integrity_handler = handler;
	}
}
