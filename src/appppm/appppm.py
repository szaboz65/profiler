"""
Main class for PPM application
"""
import logging
from app.appbase import AppBase
from appppm.mapfilecontrol import MapFileControl
from appppm.optionppm import OptionPPM


class AppPPM(AppBase):
    def __init__(self, appname=''):
        AppBase.__init__(self, appname)
        self.option = OptionPPM()
        self.Control = None

    def loadOptions(self, argv):
        return self.option.loadOptions(self.appname, argv)

    def onInit(self):
        self.Control = MapFileControl(self.option.MapFileDir, self.option.isCoding)

    def onRun(self):
        success = False
        if len(self.option.ParseFiles) == 0 and len(self.option.ParseDirs) == 0:
            logging.warning("There is nothing to parse.")

        elif self.Control is not None:
            if self.option.isClear:
                success = self.Control.ClearDefines(self.option.ProjectRootDir, self.option.ParseDirs,
                                                    self.option.ExcludeDirs, self.option.ExcludeFiles,
                                                    self.option.ParseFiles)
            else:
                success = self.Control.SetDefines(self.option.ProjectRootDir, self.option.ParseDirs,
                                                  self.option.ExcludeDirs, self.option.ExcludeFiles,
                                                  self.option.ParseFiles)
        return AppBase.EXIT_OK if success else AppBase.EXIT_ERROR
