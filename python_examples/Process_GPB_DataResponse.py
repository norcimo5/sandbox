import os 
import sys
import argparse
import math
import time
from struct import unpack, pack
#import numpy as np
from colors import *

PrintColors = (BRIGHT_CYAN, CYAN)

# before use, set an env var pointing to the top of the proto dir, ie, .../TacticalSensorStack/libsensorservice/proto
TGI_PROTO_DIR = os.getenv("TGI_PROTO_DIR")

# to allow importing of services.sensor.ss_*
sys.path.append(os.path.abspath(TGI_PROTO_DIR))

# now import the GPB definitions
import services.sensor.ss_pb2 as pb
import services.sensor.ss_dataproduct_pb2 as dp

def fetchNextDataResponse(inFile):
    data_response = dp.DataResponse()
    in_buf = inFile.read(4)
    if in_buf != "":
        size = int(in_buf.encode('hex'), 16)
        #size = unpack('I', pack('<I', int(data.encode('hex'), 16)))[0]
        # read in the data_response
        rawGPB = inFile.read(size)
        data_response.ParseFromString(rawGPB)
    return data_response
    
def Process_DataResponse_Stream(inFile):
    """Takes a stream of GPBs of data_responses and parses
       according to ss_dataproduct

    Args:
        inFile: the file handle for the input stream
    Returns:
        none...returns when stream is empty
    Raises:
        none. 
    """
    # create a dict for metrics, and initialize
    metrics = {}
    metrics['bytes_read']      = 0
    metrics['data_rate_Mbps']  = 0.0
    metrics['elapsed_time_s']  = 0.0
    metrics['start_time_ts']   = time.time()
    metrics['responseCnt']     = 0
    metrics['missing_msg_seq_num'] = 0

    try:
        data_resp = fetchNextDataResponse(inFile)
        while data_resp.ByteSize() > 0:
            metrics['bytes_read']  += data_resp.ByteSize()
            metrics['responseCnt'] += 1        
            if data_resp.HasField('msg_seq_num'):
                msg_seq_num = data_resp.msg_seq_num
                print("%sNew data_response [%d]: msg_seq_num %d.  Has %d data_product(s):%s" % 
                    ( BRIGHT_WHITE, metrics['responseCnt'], msg_seq_num, len(data_resp.data_products), RESET ) )
            else:
                metrics['missing_msg_seq_num'] += 1
                print("%sNew data_response [%d]: %sMissing msg_seq_num!!%s, missing_msg_seq_num cnt %d.  Has %d data_product(s):%s" % 
                    ( BRIGHT_WHITE, metrics['responseCnt'], BRIGHT_RED, BRIGHT_WHITE, metrics['missing_msg_seq_num'], len(data_resp.data_products), RESET ) )
     
            for idx, data_prod in enumerate(data_resp.data_products):
                if data_prod.HasExtension(dp.psd_data):
                    power_spec_data = data_prod.Extensions[dp.psd_data]  
                    # grab the header data
                    start_freq_mhz  = (power_spec_data.header.start_freq_hz / 1.0e6)
                    end_freq_mhz    = (power_spec_data.header.end_freq_hz   / 1.0e6)
                    inc_khz         = (end_freq_mhz - start_freq_mhz) / len(power_spec_data.spectrum_data.data) * 1.0e3
                    # print some stats
                    num_PSD_pts = len(power_spec_data.spectrum_data.data)/(power_spec_data.spectrum_data.format.bits_per_value / 8)
                    print("  %s[%d] PowerSpectrum, PSD pts: %d. Range (MHz): %06.2f -> %06.2f, inc (KHz): %5.2f%s" % 
                        ( BRIGHT_CYAN, idx, num_PSD_pts, start_freq_mhz, end_freq_mhz, inc_khz, RESET))
                          
                elif data_prod.HasExtension(dp.pcm_linear_audio_data):
                    pcm_data = data_prod.Extensions[dp.pcm_linear_audio_data]  
                    # grab the header data
                    freq_mhz  = (pcm_data.header.frequency_hz / 1.0e6)
                    soi_index = pcm_data.header.soi_index
                    # print some stats
                    print("  %s[%d] pcm_linear_audio, size: %d. freq (MHz): %.4f, soi_index: %d%s" %
                        ( BRIGHT_MAGENTA, idx, data_prod.ByteSize(), freq_mhz, soi_index, RESET))
                          
                elif data_prod.HasExtension(dp.iq_data):
                    print("  %s[%d] iq_data, size: %d.%s" % 
                          ( BRIGHT_YELLOW, idx, data_prod.ByteSize(), RESET))
                          
                elif data_prod.HasExtension(dp.pcm_mulaw_audio_data):
                    print("  %s[%d] pcm_mulaw_audio_data, size: %d.%s" % 
                          ( GREEN, idx, data_prod.ByteSize(), RESET))
                          
                elif data_prod.HasExtension(dp.qm_data):
                    print("  %s[%d] qm_data, size: %d.%s" % 
                          ( GREEN, idx, data_prod.ByteSize(), RESET))
                          
                elif data_prod.HasExtension(dp.speex_audio_data):
                    print("  %s[%d] speex_audio_data, size: %d.%s" % 
                          ( GREEN, idx, data_prod.ByteSize(), RESET))
                          
                elif data_prod.HasExtension(dp.fov_data):
                    print("  %s[%d] fov_data, size: %d.%s" % 
                          ( GREEN, idx, data_prod.ByteSize(), RESET))
                          
                elif data_prod.HasExtension(dp.detection_data):
                    print("  %s[%d] detection_data, size: %d.%s" % 
                          ( GREEN, idx, data_prod.ByteSize(), RESET))
                          
                elif data_prod.HasExtension(dp.lob_data):
                    print("  %s[%d] lob_data, size: %d.%s" % 
                          ( GREEN, idx, data_prod.ByteSize(), RESET))
                          
                elif data_prod.HasExtension(dp.nav_data):
                    print("  %s[%d] nav_data, size: %d.%s" % 
                          ( GREEN, idx, data_prod.ByteSize(), RESET))
            data_resp = fetchNextDataResponse(inFile)
        
        print "No more data responses in stream...Total responses read: %d, Bytes read: %d" % (metrics['responseCnt'], metrics['bytes_read'])
        if metrics['missing_msg_seq_num'] > 0:
            print "Total responses with missing_msg_seq_num: %d" % (metrics['missing_msg_seq_num'])
    finally:
        inFile.close()
		
if __name__ == "__main__":
    '''
    process_GPB_DataResponse.py GPBDataFile
    '''
    parser = argparse.ArgumentParser(description='Processes a stream of GPBs of data_responses, extracting data_record data, from either a file or stdin, analyze and print some stats')
    parser.add_argument('-i', dest='in_file', type=str, help='input file...if not specified then use stdin')
    args = parser.parse_args()
    
    if args.in_file:
        inFile = open(args.in_file, 'rb')
    else:
        inFile = sys.stdin
    
    Process_DataResponse_Stream(inFile)
