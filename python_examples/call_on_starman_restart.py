#!/usr/bin/python
import sys, os
import shutil
import time
import subprocess

def _get_site_id():
    scratch_dir = os.environ.get('GEONET_SCRATCH_DIR')
    if scratch_dir is None:
        return
    dir_parts = scratch_dir.split('/')
    local_site_id = dir_parts[2]
    return local_site_id

def execute_command(cmd, even_if_disabled=False):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out.strip()

def archive_files(rc, cmd_line):
    "Copy files to an archive directory for later inspection"

    # Note: For starman, scratch dir is actually /GEOnet/siteid/starman/runtime.
    # Build it from scratch for consistency with other archive scripts.
    if _get_site_id() is None: return
    scratch_dir = "/GEOnet/" + _get_site_id() + "/runtime"


    # Make the archive dir
    archive_dir = scratch_dir + "/post_crash_archives/" + time.strftime("%Y%m%d_%H%M%S") + "/"
    if (not os.path.exists(archive_dir)): os.makedirs(archive_dir)

    # Write in the command line that died:
    readme = open(archive_dir + "/README.txt", 'w');
    readme.write("This watchdogged command died with return code " + str(rc) + ": " + cmd_line)
    readme.close()

    # gather files
    top_dir = os.path.abspath(scratch_dir + "/../")
    files = []
    dirs_to_archive = ["/starman/log/"]
    for this_dir in dirs_to_archive:
        dir_files = os.listdir(top_dir + "/" + this_dir)
        for this_file in dir_files:
            if this_file.endswith(".log"):
                files += [top_dir + "/" + this_dir + "/" + this_file]

    # Archive and compress
    for f in files:
      dest = archive_dir + "/" + f
      dest_dir = os.path.dirname(dest)
      if (not os.path.exists(dest_dir)): os.makedirs(dest_dir)
      shutil.copyfile(f, dest)
      os.system("gzip -f " + dest)

def main():
    rc = int(sys.argv[1])
    if (rc != 0): archive_files(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
