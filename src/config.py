# version
VERSION = "0.0.0"
CREATED_DATE = "2024.07.30"

# search for FILE_EXTENSION
FILE_EXTENSION = ".cpp"

# skip source files under FILE_MIN_SIZE
FILE_MIN_SIZE = 5

# PPM macro: SET_PPM(id)
MACRO_BEGIN = " SET_PPM("
MACRO_END = ")"

# mapfile extension
MAPFILE_EXTENSION = ".map"
MAPFILE_NAME = "ppm" + MAPFILE_EXTENSION
SEPARATOR = ';'

# coverity file extension
COVFILE_EXTENSION = ".cov"

# stat files
CSVFILE_EXTENSION = ".csv"
PPM_ALL_FN = "ppm_allfn" + CSVFILE_EXTENSION
PPM_USED_FN = "ppm_usedfn" + CSVFILE_EXTENSION
PPM_UNUSED_FN = "ppm_unusedfn" + CSVFILE_EXTENSION
PPM_ALL_STAT = "ppm_allstat" + CSVFILE_EXTENSION
