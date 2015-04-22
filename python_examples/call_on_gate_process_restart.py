#!/usr/bin/python
import sys, os
import shutil
import time
import subprocess

# This must match what both def_link and gc return on a config parsing failure
BAD_CONFIG = 2

def _get_site_id():
    scratch_dir = os.environ.get('GEONET_SCRATCH_DIR')
    if scratch_dir is None:
        return
    dir_parts = scratch_dir.split('/')
    local_site_id = dir_parts[2]
    return local_site_id

def execute_command(cmd, even_if_disabled=False):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.strip()

def write_status():
    "If the config file was bad, we never wrote a status. Write it now."
    scratch_dir = os.environ.get('GEONET_SCRATCH_DIR')
    if scratch_dir is None:
        return
    local_gate_id = _get_site_id()
    report_status_name = scratch_dir + "/" + "RemoteGateStatus.txt"

    try:
      f = open(report_status_name, 'w')
      tools_path = os.path.abspath(os.path.dirname(sys.argv[0]))
      config_path = os.path.abspath(tools_path + "/../config")
      f.write("Configuration parsing failure.\n\n")
      f.write("gate_config.xml status:\n")
      f.write(execute_command(tools_path+"/gate_config_validator "+config_path+"/gate_config.xml"))
      f.write("\n")
      f.close()
    except Exception, e:
      print str(e)
      pass
        

def archive_files():
    "Copy files to an archive directory for later inspection"
    #make the scratch dir
    scratch_dir = os.environ.get('GEONET_SCRATCH_DIR')
    if scratch_dir is None:
        return
    site_id = _get_site_id()
    archive_dir = scratch_dir + "/post_crash_archives/" + time.strftime("%Y%m%d_%H%M%S") + "/"
    dirs_to_archive = ["/log", "/starman/log", "/runtime"]
    top_dir = "/GEOnet/" + site_id
    os.makedirs(archive_dir)

    #copy files to it
    for this_dir in dirs_to_archive:
        os.makedirs(archive_dir + this_dir)
        files = os.listdir(top_dir + this_dir)
        for this_file in files:
            if this_file.endswith(".log") or this_file.endswith(".uff"):
                dest_file = archive_dir + this_dir + "/" + this_file
                shutil.copyfile(top_dir + this_dir + "/" + this_file, dest_file)
                os.system("gzip " + dest_file)
    

def main():
    rc = int(sys.argv[1])
    if rc == BAD_CONFIG:
        write_status()
    archive_files()
    

if __name__ == '__main__':
    main()
