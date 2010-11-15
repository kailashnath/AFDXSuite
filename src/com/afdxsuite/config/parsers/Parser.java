package com.afdxsuite.config.parsers;

import java.io.IOException;

public interface Parser {

	public boolean validFile();
	public void parse() throws IOException;

}
