#!/usr/bin/python
import sys, os
import shutil
import time
import subprocess

def archive_files(rc, cmd_line):
    "Copy files to an archive directory for later inspection"
    f = open("/tmp/ntgstuff.txt", 'a')
    f.write("archiving NTG logs...\n")
    site_id = os.environ.get('GEONET_SITE_ID')
    scratch_dir = "/GEOnet"
    if site_id is not None:
        scratch_dir = scratch_dir + "/" + site_id
    f.write("scratch_dir = " + scratch_dir + "\n")

    #make the scratch dir
    archive_dir = scratch_dir + "/ntg_crash_archives/" + time.strftime("%Y%m%d_%H%M%S") + "/"
    dir_to_archive = "/log"
    top_dir = "/GEOnet/" + site_id
    os.makedirs(archive_dir)

    # Write in the command line that died:
    readme = open(archive_dir + "/README.txt", 'w');
    readme.write("This watchdogged command died with return code " + str(rc) + ": " + cmd_line)
    readme.close()

    #copy files to it
    # Save the current log files, and the most-recent previous one for NTG (ending with .1)
    os.makedirs(archive_dir + dir_to_archive)
    files = os.listdir(top_dir + dir_to_archive)
    for this_file in files:
        if this_file.endswith(".log") or this_file.endswith(".log.1"):
            dest_file = archive_dir + dir_to_archive + "/" + this_file
            shutil.copyfile(top_dir + dir_to_archive + "/" + this_file, dest_file)
            os.system("gzip " + dest_file)
            f.write("source: " + this_file + "-> dest: " + dest_file + "\n")
    f.close();

def main():
    f = open("/tmp/ntgstuff.txt", 'w')
    f.write("RUNNING\n")
    f.close()
    archive_files(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
