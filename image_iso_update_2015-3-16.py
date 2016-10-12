# -*- coding: utf-8 -*-

# Author: Meng Yang <meyang@redhat.com>
# Description: Make iso for the latest build
# Update: 2015-2-28
# Version: 1.0


import os
import shutil
import subprocess
import smtplib
import time
import re


class CreateIso:

    def __init__(self, iso_dir, nfs_dir, nfs_server, iso_nfs_dir, iso_nfs_server):

        self.iso_dir = iso_dir
        self.nfs_dir = nfs_dir
        self.nfs_server = nfs_server
        self.iso_nfs_dir = iso_nfs_dir
        self.iso_nfs_server = iso_nfs_server
        self.__build_env__()

    # Make necessary directories and mount necessary NFS server

    def __build_env__(self):

        if not os.path.exists(self.iso_dir):
            os.mkdir(self.iso_dir)
        else:
            os.chdir(self.iso_dir)
            self.__clean_iso__(self.iso_dir)

        if not os.path.exists(self.nfs_dir):
            os.mkdir(self.nfs_dir)

        if not os.path.exists(self.iso_nfs_dir):
            os.mkdir(self.iso_nfs_dir)

        self.__mount_dir__()

    # Get the latest build that need to make

    def get_latest_build_list(self, filename):

        fd = open(filename, mode='r')
        try:
            old_list = [x.strip() for x in fd.readlines()]
        finally:
            fd.close()
        new_list = os.listdir("%s/rel-eng" % self.nfs_dir)
        with open(filename, mode='w') as fd:
            for i in new_list:
                fd.write(i+'\n')
        latest_build = [x for x in (set(new_list) - set(old_list))]
        return latest_build

    # Sending mail to Notify

    def __send_mail__(self, iso_file_name):

        # TODO: Don't know the smtp password,can't use smtplib

        subject = "\"[Image Update]: %s Created\"" % iso_file_name
        smtp_server = "smtp=smtp://smtp.corp.redhat.com"
        sender = "from=imageupdate@redhat.com"
        receiver = "meyang@redhat.com"
        cc = "kvm-autotest@redhat.com"
        # cc = "meyang@redhat.com"
        content = "\"The Latest ISO [ %s ] has been Copied to NFS server: 10.66.90.121:/vol/s2kvmauto/iso\""\
                  % iso_file_name
        mail_cmd = "echo %s | " % content
        mail_cmd += "mail -v -s %s -S %s -S %s -c %s %s" % (subject, smtp_server, sender, cc, receiver)
        s1 = subprocess.Popen(mail_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        s1.wait()
        if s1.returncode == 0:
            print "send mail successfully"
        else:
            print "send mail failed"
            exit()

    # Judge if the link name exists

    def __if_link_exists__(self, link_name):

        if os.path.exists(link_name):
            os.unlink(link_name)

    # Create soft link for the latest build RHEL5 RHEL6 RHEL7

    def __create_symlink_version2__(self, iso_name):

        """
        Don't consider RHEL6.5 and the version before it.
        """

        rhel_ver = re.search("RHEL-(\d)\.(\d)-(\d+)", iso_name, re.I)
        architecture = ["i386", "x86_64"]
        os.chdir("%s/linux" % self.iso_nfs_dir)
        for i in architecture:
            if rhel_ver is not None and iso_name.find(i) != -1:
                link_name = "RHEL%s.%s-Server-%s.iso" % (rhel_ver.group(1), rhel_ver.group(2), i)

                latest_rhel_ver = re.search("RHEL-(\d)\.(\d)-(\d+)", os.readlink(link_name), re.I)
                if rhel_ver.group(3) > latest_rhel_ver.group(3):
                    print "%s Is The Latest Build ,Update The Symbolic %s to It." % (iso_name,link_name)
                    self.__if_link_exists__(link_name)
                    os.symlink(iso_name, link_name)
                else:
                    print "%s Is Not The Latest Build ,Will Not Create The Symbolics." % iso_name

    def __create_symlink_version1__(self, iso_name):

        """
        before RHEL6.5,the version number startswith RHEL6 ,after RHEL6.5,it startswith RHEL-6
        """
        architecture = ["i386", "x86_64"]
        os.chdir("%s/linux" % self.iso_nfs_dir)
        for i in architecture:
            if iso_name.startswith("RHEL-7") and iso_name.find(i) != -1:
                r1 = re.search("RHEL-7\.([0-9])", iso_name, re.I)
                if r1 is not None:
                    link_name_7 = "RHEL7.%s-Server-%s.iso" % (r1.group(1), i)
                    self.__if_link_exists__(link_name_7)
                    os.symlink(iso_name, link_name_7)
            elif iso_name.startswith("RHEL-6") or iso_name.startswith("RHEL6") and iso_name.find(i) != -1:
                r2 = re.search("RHEL-6\.([0-9])", iso_name)
                if r2 is not None:
                    link_name_6 = "RHEL6.%s-Server-%s.iso" % (r2.group(1), i)
                    self.__if_link_exists__(link_name_6)
                    os.symlink(iso_name, link_name_6)
                r3 = re.search("RHEL6\.([0-9])", iso_name)
                if r3 is not None:
                    link_name_6_1 = "RHEL6.%s-Server-%s.iso" % (r3.group(1), i)
                    self.__if_link_exists__(link_name_6_1)
                    os.symlink(iso_name, link_name_6_1)
            else:
                r4 = re.search("RHEL5\.([0-9])", iso_name)
                if r4 is not None:
                    link_name_5 = "RHEL5.%s-Server-%s.iso" % (r4.group(1), i)
                    self.__if_link_exists__(link_name_5)
                    os.symlink(iso_name, link_name_5)

    def create_iso(self, latest_build):

        jigdo_cmd = ""
        iso_file_name = ""
        architecture = ["i386", "x86_64"]
        if latest_build:
            for i in latest_build:
                for arch in architecture:
                    if i.find("RHEL-6") != -1:
                        jigdo_file_dir = "/home/redhat/rel-eng/%s/compose/Server/%s/jigdo" % (i,arch)
                    else:
                        if arch == "i386":
                            continue
                        jigdo_file_dir = "/home/redhat/rel-eng/%s/compose/Server/x86_64/jigdo" % i
                    # if jigdo_file_dir.endswith("/"):
                    # jigdo_file_dir = os.path.dirname(jigdo_file_dir)
                    for j in os.listdir(jigdo_file_dir):
                        shutil.copy2(os.path.join(jigdo_file_dir, j), self.iso_dir)
                        if j.endswith(".jigdo"):
                            iso_file_name = os.path.splitext(j)[0]
                            jigdo_cmd = "jigdo-lite --scan %s %s/%s" % (
                            os.path.dirname(jigdo_file_dir), self.iso_dir, j)
                    os.chdir(self.iso_dir)
                    before_run = time.time()
                    print "-" * 68
                    print "\nBegin To Create: %s ,Please Wait...\n" % iso_file_name
                    run_jigdo_cmd = subprocess.Popen(jigdo_cmd, shell=True, stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE)
                    run_jigdo_cmd.communicate()
                    if run_jigdo_cmd.returncode != 0:
                        print "Create iso Failed"
                        exit()

                    shutil.copy2(os.path.join(self.iso_dir, iso_file_name), "%s/linux" % self.iso_nfs_dir)
                    time.sleep(5)
                    self.__create_symlink_version2__(iso_file_name)

                    time.sleep(20)
                    self.__send_mail__(iso_file_name)
                    after_run = time.time()
                    print "\nIso Creation Completes And Uses %2.2f Seconds." % (after_run - before_run)
                    print "-" * 68
            self.__clean_iso__(self.iso_dir)
        else:
            print("No new build yet!")
            exit()

    # Clean the iso_dir After the copy

    def __clean_iso__(self, iso_dir):

        [os.unlink("%s/%s" % (iso_dir, i)) for i in os.listdir(iso_dir)]
        self.__umount_dir__()

    def __umount_dir__(self):

        for i in [self.iso_nfs_dir, self.nfs_dir]:
           if not os.path.ismount(i):
               pass
           else:
                u1 = subprocess.Popen("umount -l %s" % i, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                data, data_err = u1.communicate()
                if u1.returncode == 0:
                    pass
                elif data_err.find("busy") != -1:
                    print "fail to umount because of the following error:\n%s" % data_err
                    # os.system("fuser -km %s" % i)
                    u2 = subprocess.Popen("umount -l %s " % i, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if u2.returncode == 0:
                        pass
                    else:
                        print "umount error"

    def __mount_dir__(self):

        mount_iso_nfs_server = "mount -t nfs %s %s" % (self.iso_nfs_server, self.iso_nfs_dir)
        mount_nfs_server = "mount -t nfs %s %s" % (self.nfs_server, self.nfs_dir)

        self.__umount_dir__()

        for i in [mount_nfs_server, mount_iso_nfs_server]:
            m1 = subprocess.Popen(i, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            m1.wait()
            if m1.returncode == 0:
                # print "Mount %s successfull.\n" % i
                pass
            else:
                print "mount %s error." % i
                print m1.stderr

def main():
    iso_dir = "/home/iso"
    nfs_dir = "/home/redhat"
    iso_nfs_dir = "/home/kvm_autotest_root/iso"
    nfs_server = "nfs.englab.nay.redhat.com:/pub/rhel"
    iso_nfs_server = "10.66.90.121:/vol/s2kvmauto/iso"

    # If the file path changes ,need to update  the filename
    filename = "/root/image_iso_create/result.txt"

    # TODO: Need to create filename if it doesn't exist

    update_iso = CreateIso(iso_dir, nfs_dir, nfs_server, iso_nfs_dir, iso_nfs_server)
    update_iso.create_iso(update_iso.get_latest_build_list(filename))

if __name__ == '__main__':
    main()
