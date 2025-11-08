# -*- coding: utf-8 -*-
"""
Created on Tue May 24 07:29:19 2022

@author: HP
"""
import pydicom 
 
ds = pydicom.dcmread("../data/CT.dcm")
print(ds)
print(ds.StudyDate)
print(ds.pixel_array)
