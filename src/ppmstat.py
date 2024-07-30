#!/usr/bin/python3/python
import sys
from appstat.appstat import AppStat
from app.optionbase import OptionBase


def main(argv):
    app = AppStat('ppmstat')
    error = app.loadOptions(argv)
    if error == OptionBase.OK:
        app.setLogging()
        app.Init()
        error = app.Run()
        app.Exit()

    sys.exit(error)


if __name__ == '__main__':
    main(sys.argv[1:])
