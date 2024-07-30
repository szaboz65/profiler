# Profiler for Performance Measurement in C++ application

This application can be used to profile an embedded C++ application or part of it for performance measurement on the target device.
The measurement minimally affects the operation of the C++ program and saves the measured data, which can be analyzed later.
The usual file encoding formats are handled (ansi, utf-8, utf-16-le/be, with/without boom). After measuring the profile macros can be cleared simply.  

## Usage steps
1. The application reads all cpp files in the given root directory and inserts a macro before the first line of each dependent. Within the root directory, you can define the directories to be read or, on the contrary, the directories and files to be excluded.
2. The functions in the read files are given an identifier, from which a map file is created.
3. You need to define the macro in the C++ program and rebuild the application.
4. After installation on the target device, performing the measurement and saving the results.
5. The attached statistical application can be used to connect the function map and the measurement result, and different statistical files are created in csv format.
6. This application clears the all profile macro from the C++ source. 

### Profiler application
Starting point: ppm.py

Command line switches: ppm.py [-abcdehlprvx] [file1 [file2]...]

| Switch | Verbose      | Description                         |
|--------|--------------|-------------------------------------|
| -a     | --autocoding | *autodetect file coding*            |
| -b     | --verbose    | *dump verbose messages*             |
| -c     | --clear      | *only clear PPM macro*              |
| -d     | --debug      | *dump in debug messages*            |
| -e     | --excdir=    | *exclude directories, separator: ;* |
| -h     | --help       | *display this screen*               |
| -m     | --mapdir=    | *set mapfile directory*             |
| -l     | --log        | *make log file, ppm.log*            |
| -p     | --parse=     | *parse directories, separator: ;*   |
| -r     | --root=      | *set projectroot directory*         |
| -x     | --excfile=   | *exclude files, separator: ;*       | 
| -v     | --version    | *dump version info*                 |

### Statistic application
Starting point: ppmstat.py

Command line switches: ppmstat.py [-bdhlv] mapfile

| Switch | Verbose    | Description                 |
|--------|------------|-----------------------------|
| -b     | --verbose  | dump verbose messages       |
| -d     | --debug    | dump in debug messages      |
| -h     | --help     | display this screen         |
| -l     | --log      | make log file, ppmstat.log  |
| -o     | --outdir   | output directory            |
| -v     | --version  | dump version info           |

## Format of the files
### Format of the map file
```
ProjectRootDirectory
Id,NameSpace;FunctionName;FileName;LineNumber
```
where
- ProjectRootDirectory: the root directory
- Id: the generated unique id for every function
- NameSpace: the class name including the namespace
- FunctionName: the name of the function
- FileName: the file name of the source file
- LineNumber: the line number in the source file

The name of the map file is 'ppm.map' which is configured in the config.py file.

### Format of the measured result file
```
id;count
Id;Result
```
where
- the first line is the header of the data but not used
- Id: the function id, see above
- Result: the measured value

The default extension of the result file is '.cov' which is configured in the config.py file.

### Format of the statistic files
Two kind of statistic generated:
1. One of them, the map file and result file is merged, and it contains the following fields: 
    - "method_id;class_name;method_name;source_file;line_num;count". 
    - Tree files are generated:
        - the all function
        - only the used functions (count>0)
        - the unused functions (count==0)
2. The other is a statistic for all source file which contains the following fields: 
    - "method_count;used_method_count;unused_method_count;used_method_percent;unused_method_percent;path".

## Using the C++ macro
The application will insert a macro into the all function after the opening curly bracket before the first instruction. This macro performs the measurement activity. The text of the macro is defined in the config.py file. It's format: MACRO_BEGIN Id MACRO_END

```
int func(int param)
{ SET_PPM(101)
    return 0;
}
```
The measurement activity can also be a simple counter that counts the number of times the given function was called, but it can also show the time spent in the function.
### Example for a simple counter:
```
extern unsigned long ppm[1000];
#define SET_PPM(id) ++ppm[id];
```

### Example to measure the executing time
```
class ppm {
public:
    ppm(_id): id(_id) {
        start[id] = microsecond();
    }
    ~ppm() {
        time[id] += microsecond() - start[id];
    }
private:
    unsingned short id;
    static unsigned long start[1000];
    static unsigned long time[1000];
}
#define SET_PPM(id) ppm _ppm(id);
```

> NOTE: In the both case the arrays need to be reserved and filled with zero.

## Create result file
It depends on the embedded system capabilities. Some idea:
- write data to a file example on SD card
- send data to a serial line and the terminal program writes it to file
- send data to a stream on a high speed line (USB, ethernet or Wi-Fi) and a receiver program writes it to file

In the last case there is possibility to send data periodically and to display it in real time like Windows TaskManager.
