#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import ADS1263
import RPi.GPIO as GPIO

REF = 5.08          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V

# ADC1 test part
TEST_ADC1       = True



ADC = ADS1263.ADS1263()
    
# The faster the rate, the worse the stability
# and the need to choose a suitable digital filter(REG_MODE1)
if (ADC.ADS1263_init_ADC1('ADS1263_10SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel



channelList = [0, 1]
while(1):
    ADC_Value = ADC.ADS1263_GetAll(channelList)    # get ADC1 value
    for i in channelList:
        if(ADC_Value[i]>>31 ==1):
               print("-ADC1 IN%d = -%lf" %(i, (REF*2 - ADC_Value[i] * REF / 0x80000000)))
        else:
                print("+ADC1 IN%d = %lf" %(i, (ADC_Value[i] * REF / 0x7fffffff)))   # 32bit   print all





