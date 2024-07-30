"""
Main class for STAT application
"""

import os
import config
import logging
from app.appbase import AppBase
from appstat.optionstat import OptionStat
from appstat.statcontrol import StatControl


class AppStat(AppBase):
    def __init__(self, appname=''):
        AppBase.__init__(self, appname)
        self.option = OptionStat()
        self.Control = None

    def loadOptions(self, argv):
        return self.option.loadOptions(self.appname, argv)

    def onInit(self):
        self.Control = StatControl()

    def onRun(self):
        if len(self.option.MapFileName) == 0:
            logging.warning("There is no mapfile.")
            return AppBase.EXIT_ERROR

        if not self.Control.parseMap(self.option.MapFileName):
            return AppBase.EXIT_ERROR

        logging.info("Coverity files parsing... ")
        self.Control.parseCov(self.option.ParseDir)
        logging.info("Coverity files loaded. ")

        self.Control.Save_AllFunc(self.makeCSVFilename(config.PPM_ALL_FN))
        logging.info("All function record saved. ")
        self.Control.Save_UnusedFunc(self.makeCSVFilename(config.PPM_UNUSED_FN))
        logging.info("Unused function records saved. ")
        self.Control.Save_UsedFunc(self.makeCSVFilename(config.PPM_USED_FN))
        logging.info("Used function records saved. ")

        self.Control.Save_AllStat(self.makeCSVFilename(config.PPM_ALL_STAT))
        logging.info("All statistic saved. ")

        return AppBase.EXIT_OK

    def makeCSVFilename(self, name):
        return os.path.join(self.option.OutputDir, name)
