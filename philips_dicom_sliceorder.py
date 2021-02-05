 # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import pydicom
import numpy as np
from scipy.stats import rankdata
import pandas as pd
import datetime
import sys

file_location = sys.argv[1]

print(file_location)

pd.set_option("display.max_rows", None, "display.max_columns", None)


ds = pydicom.dcmread(file_location)


all_slices = ds.PerFrameFunctionalGroupsSequence

slices = [s for s in all_slices
         if s.FrameContentSequence[0].TemporalPositionIndex == 1]
    
loops_to_do = int(len(all_slices)/len(slices))


timesOut = pd.DataFrame([])

i=393
for i in range(loops_to_do):
    
    slices = [s for s in all_slices
              if s.FrameContentSequence[0].TemporalPositionIndex == i+1]
    
    slice_position = [s.PlanePositionSequence[0].ImagePositionPatient
                      for s in slices]
                      
                      
    slice_timing_str = [v[0x2005, 0x140f][0].SOPInstanceUID.split('.')[-1]
                        for v in slices]
    
    


    slice_timing_date = [datetime.datetime(year=int(x[0:4]),month=int(x[4:6]),\
                                           day=int(x[6:8]),hour=int(x[8:10]),\
                                           minute=int(x[10:12]),second=int(x[12:14]),\
                                           microsecond=int(x[14:])*10) for x in slice_timing_str]
   
    slice_timing_timestamp = [x.timestamp() for x in slice_timing_date]

    
    slice_timing_timestamp[0]
    
    
    slice_order = (rankdata(slice_timing_timestamp, method='min') - 1).astype(int)
    
    orderIdx = slice_order == 0
    orderIdx = [i for i, val in enumerate(orderIdx) if val][0]
    
    firstTime = slice_timing_timestamp[orderIdx]
    
    slice_timing = [x-firstTime for x in slice_timing_timestamp]
    
    ser = pd.Series(slice_timing).to_frame().T

    timesOut = pd.concat([timesOut,ser],axis=0)


timesOut.reset_index(drop=True,inplace=True)

median_times = timesOut.median()

print("Slice Times:")
print(median_times)

order_out = rankdata(median_times, method='min') - 1

print("Slice Order (without rounding):")
print(order_out)
print("this order is without rounding, and for multiband rounding might be needed")


rounded_times = median_times.round(decimals=3)

order_out_round = rankdata(rounded_times, method='min') - 1

print("Slice Order (without rounding):")
print(order_out_round)
print("this order is with rounding but still might be off")







