import ConfigParser

config = ConfigParser.RawConfigParser()
config.read("conf/Application.config")
print 'Config file initializeds'
