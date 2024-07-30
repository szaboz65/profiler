'''
options for the statistic application
'''

import getopt
import config
from app.optionbase import OptionBase


class OptionStat(OptionBase):
    def __init__(self):
        OptionBase.__init__(self)
        self.__ParseDir = "."
        self.__OutputDir = "."
        self.__MapFileName = ""

    def get_MapFileName(self):
        return self.__MapFileName
    MapFileName = property(get_MapFileName)

    def get_ParseDir(self):
        return self.__ParseDir
    ParseDir = property(get_ParseDir)

    def get_OutputDir(self):
        return self.__OutputDir
    OutputDir = property(get_OutputDir)

    def loadOptions(self, appname, argv):
        try:
            opts, args = getopt.getopt(argv, "bdhlo:v",
                                       ["verbose", "debug", "help", "log", "outdir=", "version"])

            for opt, arg in opts:
                if opt in ("-b", "--verbose"):
                    self._isVerbose = True
                elif opt in ("-d", "--debug"):
                    self._isDebug = True
                elif opt in ("-l", "--log"):
                    self._isLog = True
                elif opt in ("-o", "--outdir"):
                    self.__OutputDir = arg
                elif opt in ("-v", "--version"):
                    print("Version: ", config.VERSION)
                    print("Created: ", config.CREATED_DATE)
                    return self.EXIT
                elif opt in ("-h", "--help"):
                    print(appname + '.py [-bdhlv] mapfile')
                    print(' -b, --verbose     dump verbose messages')
                    print(' -d, --debug       dump in debug messages')
                    print(' -h, --help        display this screen')
                    print(' -l, --log         make log file, ' + appname + ".log")
                    print(' -o, --outdir      output directory')
                    print(' -v, --version     dump version info')
                    return self.EXIT

            if argv:
                i = 0
                for arg in argv:
                    if len(arg) == 0 or arg.startswith('-'):
                        continue
                    i += 1
                    if i == 1:
                        self.__ParseDir = arg
                    else:
                        self.__MapFileName = arg
                        break

            return self.OK

        except getopt.GetoptError as e:
            print(str(e))
            print('use ' + appname + '.py -h')
            return self.ERROR
