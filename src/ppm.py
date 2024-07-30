#!/usr/bin/python3/python
import sys
from app.optionbase import OptionBase
from appppm.appppm import AppPPM


def main(argv):
    app = AppPPM('ppm')
    error = app.loadOptions(argv)
    if error == OptionBase.OK:
        app.setLogging()
        app.Init()
        error = app.Run()
        app.Exit()

    sys.exit(error)


if __name__ == '__main__':
    main(sys.argv[1:])
