#!/usr/bin/env python2

import sys
import re
from datetime import datetime, timedelta

def shift_time(ts,DELTA):
	return (datetime.strptime(ts, '%H:%M:%S,%f') + timedelta(seconds=DELTA/1000)).strftime('%H:%M:%S,%f')[:12]

def is_line_later_than(ts,start_time):
    # time of the line:
    hour, minute, second = ts.split(':')
    hour, minute = int(hour), int(minute)
    second_parts = second.split(',')
    second = int(second_parts[0])
    microsecond = int(second_parts[1])
    line_time_ms = hour * 60 * 60 * 1000 +\
    minute * 60 * 1000 +\
    second * 1000 +\
    microsecond
    
    # time of shift start:
    hour, minute, second = start_time.split(':')
    hour, minute, second = int(hour), int(minute), int(second)
    start_time_ms = hour * 60 * 60 * 1000 +\
    minute * 60 * 1000 +\
    second * 1000
    
    if line_time_ms >= start_time_ms:
        return True
    else:
        return False
    
#def parse_time(time):
#    hour, minute, second = time.split(':')
#    hour, minute = int(hour), int(minute)
#    second_parts = second.split(',')
#    second = int(second_parts[0])
#    microsecond = int(second_parts[1])
#
#    return (
#        hour * 60 * 60 * 1000 +
#        minute * 60 * 1000 +
#        second * 1000 +
#        microsecond
#    )
#
#
#def shift_time(time):
#    return time + shift_ms
#
#
#def get_time(time):
#    return (
#        time // (60 * 60 * 1000),
#        (time % (60 * 60 * 1000)) // (60 * 1000),
#        (time % (60 * 1000)) // 1000,
#        time % 1000,
#    )
#
#def str_time(time):
#    return '%02d:%02d:%02d,%03d' % get_time(time)
#

def main():
    try:
        filename = sys.argv[1]
        start_time = sys.argv[2]
        shift_ms = int(sys.argv[3])
    except (IndexError, ValueError):
        print("usage: python_subtitle_adjuster filename shift_starts_here_HH:mm:ss shift_ms")
        return

    out = ''
    
    enc = 'utf-8'
    ###enc = 'cp1250'
    with open(filename, 'r', encoding=enc) as file:
        for line in file:
            if '-->' in line:
                ts1, _, ts2 = line.split()
                if is_line_later_than(ts1,start_time):
                    ts1 = shift_time(ts1,shift_ms)
                    ts2 = shift_time(ts2,shift_ms)
                    #print('%(ts1)s --> %(ts2)s' % locals())
                out += ts1 + ' --> ' + ts2 + '\n'
            else:
                #print(s.strip())
                out += line
            
    file.close()
    #print(out)
    
    #import os
    #os.rename(filename, filename + '.orig')
    #os.replace(filename, filename + '.orig')
    import shutil
    shutil.copy(filename, filename + '.orig')
    
    destinationFile = filename
    fd = open(destinationFile, 'w', encoding=enc)    
    for line in out:
        fd.write(line)
    fd.close()
    

if __name__ == '__main__':
    main()

#References:
#https://github.com/haron/subtitles-shift/blob/master/shift.py
#https://github.com/adeel/srt-shift/blob/master/srt_shift.py

