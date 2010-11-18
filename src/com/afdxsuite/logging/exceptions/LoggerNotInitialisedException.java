package com.afdxsuite.logging.exceptions;

public class LoggerNotInitialisedException extends Exception {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	public LoggerNotInitialisedException() {
		super("Logger is not yet initialised. Please initialise the logger");
	}
	
	public LoggerNotInitialisedException(String message) {
		super("Logger is not yet initialised. Please initialise the logger" + 
				"Reason : " + message);
	}
	
	public LoggerNotInitialisedException(Exception ex) {
		super(ex);
	}
}
