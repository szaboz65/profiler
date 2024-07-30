'''
Options for the PPM application
'''

import getopt
import config
from app.optionbase import OptionBase


class OptionPPM(OptionBase):

    SEPARATOR = ';'

    def __init__(self):
        OptionBase.__init__(self)
        self.__isCoding = False
        self.__isClear = False
        self.__ProjectRootDir = "."
        self.__MapFileDir = "."
        self.__ParseDirs = []
        self.__ParseFiles = []
        self.__ExcludeDirs = []
        self.__ExcludeFiles = []

    def get_isCoding(self):
        return self.__isCoding
    isCoding = property(get_isCoding)

    def get_isClear(self):
        return self.__isClear
    isClear = property(get_isClear)

    def get_ExcludeDirs(self):
        return self.__ExcludeDirs
    ExcludeDirs = property(get_ExcludeDirs)

    def get_ExcludeFiles(self):
        return self.__ExcludeFiles
    ExcludeFiles = property(get_ExcludeFiles)

    def get_ProjectRootDir(self):
        return self.__ProjectRootDir
    ProjectRootDir = property(get_ProjectRootDir)

    def get_MapFileDir(self):
        return self.__MapFileDir
    MapFileDir = property(get_MapFileDir)

    def get_ParseDirs(self):
        return self.__ParseDirs
    ParseDirs = property(get_ParseDirs)

    def get_ParseFiles(self):
        return self.__ParseFiles
    ParseFiles = property(get_ParseFiles)

    def loadOptions(self, appname, argv):
        try:
            opts, args = getopt.getopt(argv, "abcde:hm:lp:r:x:v",
                                       ["autocoding", "verbose", "clear", "debug", "excdir=", "help", "mapdir=",
                                        "log", "parse=", "root=", "excfile=", "version"])

            for opt, arg in opts:
                if opt in ("-a", "--autocoding"):
                    self.__isCoding = True
                elif opt in ("-b", "--verbose"):
                    self._isVerbose = True
                elif opt in ("-c", "--clear"):
                    self.__isClear = True
                elif opt in ("-d", "--debug"):
                    self._isDebug = True
                elif opt in ("-e", "--excdir"):
                    self.__ExcludeDirs = arg.split(OptionPPM.SEPARATOR)
                elif opt in ("-m", "--mapdir"):
                    self.__MapFileDir = arg
                elif opt in ("-l", "--log"):
                    self._isLog = True
                elif opt in ("-p", "--parse"):
                    self.__ParseDirs = arg.split(OptionPPM.SEPARATOR)
                elif opt in ("-r", "--root"):
                    self.__ProjectRootDir = arg
                elif opt in ("-x", "--excfile"):
                    self.__ExcludeFiles = arg.split(OptionPPM.SEPARATOR)
                elif opt in ("-v", "--version"):
                    print("Version: ", config.VERSION)
                    print("Created: ", config.CREATED_DATE)
                    return self.EXIT
                elif opt in ("-h", "--help"):
                    print(appname + '.py [-abcdehlprvx] [file1 [file2]...]')
                    print(' -a, --autocoding  autodetect file coding')
                    print(' -b, --verbose     dump verbose messages')
                    print(' -c, --clear       only clear PPM macro')
                    print(' -d, --debug       dump in debug messages')
                    print(' -e, --excdir=     exclude directories, separator: ' + OptionPPM.SEPARATOR)
                    print(' -h, --help        display this screen')
                    print(' -m, --mapdir=     set mapfile directory')
                    print(' -l, --log         make log file, ' + appname + ".log")
                    print(' -p, --parse=      parse directories, separator: ' + OptionPPM.SEPARATOR)
                    print(' -r, --root=       set projectroot directory')
                    print(' -x, --excfile=    exclude files, separator: ' + OptionPPM.SEPARATOR)
                    print(' -v, --version     dump version info')
                    return self.EXIT

            if argv:
                for arg in argv:
                    if len(arg) == 0 or arg.startswith('-'):
                        continue
                    self.__ParseFiles.append(arg)

            return self.OK

        except getopt.GetoptError as e:
            print(str(e))
            print('use ' + appname + '.py -h')
            return self.ERROR
