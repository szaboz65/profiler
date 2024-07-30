"""
Base class for application
"""
import logging


class AppBase(object):
    EXIT_OK = 0
    EXIT_ERROR = 1

    def __init__(self, appname=''):
        self.appname = appname
        self.option = None

    def loadParams(self, argv):
        return self.option.loadOptions(self.appname, argv)

    def setLogging(self):
        log_format = '%(levelname)-7s | %(asctime)-15s | %(message)s'
        if self.option.isDebug:
            log_level = logging.DEBUG
        elif self.option.isVerbose:
            log_level = logging.INFO
        else:
            log_level = logging.WARNING
        if self.option.isLog:
            logging.basicConfig(format=log_format, level=log_level, filename=self.appname+'.log')
        else:
            logging.basicConfig(format=log_format, level=log_level)

    def Init(self):
        logging.info("Init program")
        self.onInit()

    def Run(self):
        logging.info("Start program")
        return self.onRun()

    def Exit(self):
        logging.info("Exit program")
        self.onExit()

    # virtuals-----------
    def onInit(self):
        pass

    def onRun(self):
        pass

    def onExit(self):
        pass
