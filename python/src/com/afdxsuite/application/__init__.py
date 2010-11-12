import ConfigParser

config = ConfigParser.RawConfigParser()
config.read("Application.config")
print 'Config file initialized'