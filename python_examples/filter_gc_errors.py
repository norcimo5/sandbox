#!/usr/bin/python

import sys 
"""Write a [site_id]_errors.log file that only has error messages from gc
   and its descendants (def_link, ftClient, etc). """

import os

def get_gate_siteid():
    gate_id = ''
    try:
        output = execute_command("cat /h/GEOnet/config/node.properties | grep node.site_id", even_if_disabled=True)
        split_regex = re.compile(r"^\s*node.site_id\s*=\s*(\w+)")
        match = split_regex.match(output)
        if (match): gate_id = match.group(1)
        if (match): gate_id = match.group(1)
    except Exception, e:
        return ''
    return gate_id

def filtered(line):
    #don't print out low-level "comm" errors about connections that aren't set up yet
    if line.find("comm.cc") >= 0:
        return True
    if line.find("unexpected snl statement") >= 0:
        return True
    return False


def write_error_log(log_file, error_file):
    #go through the log line by line and find errors in gc and its children
    processes_of_interest = ['gc', 'def_link', 'ftClient', 'socketJicdListener', 'audio_bridge', 'audio_translator_client']
    levels_of_interest = ['ERRO', 'CRIT', 'ALRT', 'EMRG']

    for line in log_file:
        fields = line.split(',')
        if len(fields) < 7:
            continue
        process = fields[2]
        level = fields[3]
        if process in processes_of_interest and level in levels_of_interest:
            if not filtered(line):
                error_file.write(line)
            #also write lines about dropping JICD messages
        elif process in processes_of_interest and line.lower().find("dropping") >= 0:
            error_file.write(line)

    log_file.close()
    error_file.close()


def main(args):
    #figure out what the log file is, from $GEONET_SITE_ID or the command line
    log_filename = ''
    if (len(args) >= 2):
        log_filename = args[1]
    else:
        site_id = os.environ.get('GEONET_SITE_ID')
        if site_id is None:
            site_id = get_site_id()
        if site_id == '':
            print "Cannot find the log file"
            print "Either pass the log file on the command line, set $GEONET_SITE_ID, or"
            print "set node.site_id in /h/GEOnet/config/node.properties"
            return
        log_filename = "/GEOnet/" + site_id + "/log/" + site_id + ".log"

    #figure out what the error log is
    error_filename = log_filename.replace(".log", "_errors.log")
    
    #open the log and the error-only log
    log_file = None
    error_file = None
    try:
        log_file = open(log_filename, 'r')
    except:
        print "Cannot open log file " + log_filename + " for reading"
        return
    try:
        error_file = open(error_filename, 'w')
    except:
        print "Cannot open error-only log file " + error_filename + " for writing"
        return

    write_error_log(log_file, error_file)
    print "Wrote errors to " + error_filename
        
    

if __name__ == '__main__':
    main(sys.argv)
