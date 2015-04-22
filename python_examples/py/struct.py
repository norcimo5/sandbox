#!/usr/bin/env python2.7
import binascii

mydict =  { 'ask4_version' : binascii.unhexlify('3A02FE0000'), \
'ask4_status' : binascii.unhexlify('3A03FD0000'), \
'ask4_status_text' : binascii.unhexlify('3A04FC0000'), \
'set_SALed' : binascii.unhexlify('3A07F90000'), \
'reset_host' : binascii.unhexlify('3A11EF095245534554484F535436'), \
'gps_led_red' : binascii.unhexlify('3A17E90100FF'), \
'gps_led_green' : binascii.unhexlify('3A17E90101FE'), \
'gps_led_orange' : binascii.unhexlify('3A17E90102FD'), \
'gps_led_off' : binascii.unhexlify('3A17E90103FC'), \
'AttLed_on' : binascii.unhexlify('3A1BE50101FE'), \
'AttLed_off' : binascii.unhexlify('3A1BE50100FF'), \
'AttLed_status' : binascii.unhexlify('3A1BE5013FC0'), \
'Async_on' : binascii.unhexlify('3A1CE40101FE'), \
'Async_off' : binascii.unhexlify('3A1CE40100FF'), \
'Async_status' : binascii.unhexlify('3A1CE4013FC0'), \
'ask4_rfu_version' : binascii.unhexlify('3A32CE0000') }
