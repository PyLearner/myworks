__maintainer__ = 'meyang@redhat.com'
__version__ = '1.0'

import os
import sys
import shutil
import smtplib
import logging.config
import subprocess
import ConfigParser
from email.mime.text import MIMEText


def mail_sent(to_list, subject, content, maintainer="meyang",
              smtp="smtp.corp.redhat.com"):
    """
    send email
    """
    mail = MIMEText(content, _subtype='plain', _charset='utf-8')
    mail['Subject'] = subject
    mail['To'] = ";".join(to_list)
    mail['From'] = maintainer

    try:
        server = smtplib.SMTP(smtp)
        server.sendmail(maintainer, to_list, mail.as_string())
        server.quit()
    except Exception as e:
        logger.info(e)
    return


class UpdateVirtioWin:

    virtio_win_name_list = []

    def __init__(self, tag, packagename, virtio_win_version, nfspath, workdir, nfsserver, decompressed_dir):
        self.tag = tag
        self.packagename = packagename
        self.nfspath = nfspath
        self.nfsserver = nfsserver
        self.workdir = workdir
        self.decompressed_dir = decompressed_dir
        self.virtio_win_version = virtio_win_version

    def check_virtio_win(self):
        """
        Check if there is new virtio_win version.
        :return: bool
        """
        existed_virtio_win = os.listdir(self.nfspath)
        logger.info('Existed virtio_win_file and its linkname:\n {}'.format(existed_virtio_win))
        for version in existed_virtio_win:
            virtio_win_name = self.get_latest_virtio_win_name()
            if virtio_win_name in version:
                return True

        return False

    def process_cmd(self, cmd):
        # run shell cmd
        try:
            logger.info('Start to execute the command: {}'.format(cmd))
            output = subprocess.check_output(cmd, shell=True).strip()
            return output
        except:
            logger.info("Can't execute the command {}".format(cmd))

    def __get_latest_virtio_win(self):
        """
        Get the latest virtio_win and its info.
        :return: virtio_win name
        """
        virtio_win_list = []
        for t in self.tag:
            cmd = "brew latest-pkg {} {}".format(t, self.packagename)
            cmd += " | grep virtio | awk '{print $1}'"
            virtio_win_list.append((self.process_cmd(cmd), t))

        if virtio_win_list[0][0] == virtio_win_list[1][0]:
            return virtio_win_list[0]
        else:
            for i, j in virtio_win_list:
                if '_' in i:
                    return i, j

    def get_latest_virtio_win_name(self):
        """
        Get the latest virtio_win_name
        :return: latest virtio_win_name
        """
        virtio_win_name = self.__get_latest_virtio_win()[0]
        logger.info('The latest virtio_win_name is: {}'.format(virtio_win_name))
        return virtio_win_name

    def get_latest_virtio_win_tag(self):
        """
        Get the latest virtio_win_tag
        :return: latest virtio_win_tag
        """
        virtio_win_tag = self.__get_latest_virtio_win()[1]
        logger.info('The latest virtio_win_tag is: {}'.format(virtio_win_tag))
        return virtio_win_tag

    def download(self):
        """
        Download the virtio_win package.
        :return: None
        """
        tagname = self.get_latest_virtio_win_tag()
        cmd = "cd {};brew download-build --arch=noarch --latestfrom={} {}"
        cmd = cmd.format(self.workdir, tagname, self.packagename)
        logger.info('Start to Download virtio_win rpm package: {}'.format(self.packagename))
        self.process_cmd(cmd)
        # subp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # data, data_err = subp.communicate()
        #
        # if not subp.returncode == 1:
        #     print('download error. {}'.format(data_err))

    def decompress_rpm_package(self):
        """
        Decompress the package and find the iso files needed.
        :return: None
        """
        package = "{}.noarch.rpm".format(self.get_latest_virtio_win_name())
        cmd = "cd {};rpm2cpio {} | cpio -dimv".format(self.workdir, package)
        logger.info('Start to decompress: {}'.format(package))
        subprocess.check_call(cmd, shell=True)

    def __get_file_dir(self):
        """
        Get the directory after decompress
        :return:
        """
        return os.path.join(self.workdir, self.decompressed_dir)

    def __rename_file(self, pattern='virtio-win-'):
        """
        Rename the virio_win file name according to the one defined.
        :param pattern:
        :return:
        """
        virtio_win_name = self.get_latest_virtio_win_name()
        file_dir = self.__get_file_dir()
        logger.info('Current directory: {}'.format(file_dir))
        os.chdir(file_dir)
        for i in os.listdir(file_dir):
            if pattern in i:
                if i.endswith('.iso'):
                    shutil.move(i, '{}.iso'.format(virtio_win_name))
                elif i.endswith('amd64.vfd'):
                    shutil.move(i, '{}_amd64.vfd'.format(virtio_win_name))
                else:
                    shutil.move(i, '{}_x86.vfd'.format(virtio_win_name))

    def __get_virtio_win_name_list(self, pattern='virtio-win-'):
        """
        Get the virtio_win list after rename
        :param pattern:
        :return: the virtio_win list after rename
        """
        self.__rename_file()
        virtio_list = []
        file_dir = self.__get_file_dir()
        for filename in os.listdir(file_dir):
            if pattern in filename:
                virtio_list.append(os.path.join(file_dir, filename))

        return virtio_list

    def copy_to_nfs(self):
        """
        Copy the needed iso/vfd files to our working nfs.
        :return: None
        """
        virtio_list = self.__get_virtio_win_name_list()
        for filename in virtio_list:
            shutil.copy(filename, self.nfspath)

    def make_link(self):
        """
        Create the predefined soft link name:
        virtio-win.iso.el6 -> virtio-win-latest-signed-el6.iso ->
        virtio-win_x86.vfd.el6 -> virtio-win-latest-signed-el6.vfd.i386 ->
        virtio-win_amd64.vfd.el6 -> virtio-win-latest-signed-el6.vfd.amd64 ->
        virtio-win.iso.el7 -> virtio-win-latest-signed-el7.iso ->
        virtio-win_x86.vfd.el7 -> virtio-win-latest-signed-el7.vfd.i386 ->
        virtio-win_amd64.vfd.el7 -> virtio-win-latest-signed-el7.vfd.amd64 ->
        :return:
        """
        virtio_win_map = {
            "el6": {
                "virtio-win.iso.el6": "virtio-win-latest-signed-el6.iso",
                "virtio-win_x86.vfd.el6": "virtio-win-latest-signed-el6_x86.vfd",
                "virtio-win_amd64.vfd.el6": "virtio-win-latest-signed-el6_amd64.vfd",
            },
            "el7": {
                "virtio-win.iso.el7": "virtio-win-latest-signed-el7.iso",
                "virtio-win_x86.vfd.el7": "virtio-win-latest-signed-el7_x86.vfd",
                "virtio-win_amd64.vfd.el7": "virtio-win-latest-signed-el7_amd64.vfd",
            }
        }
        image_type = ['amd64.vfd', 'x86.vfd', 'iso']

        def __create_soft_link(target, linkname):
            """
            Create soft link
            :param target:
            :param linkname:
            :return:
            """
            cmd = 'ln -sf {} {}'.format(target, linkname)
            logger.info('Start make softlink, command: {}'.format(cmd))
            return self.process_cmd(cmd)

        def __create(imagetype):
            virtio_list = self.__get_virtio_win_name_list()

            for virtio_win_name in virtio_list:
                if virtio_win_name.endswith(imagetype):
                    for key, value in virtio_win_map[self.virtio_win_version].items():
                        if value.endswith(imagetype) and virtio_win_name.find(self.virtio_win_version):
                            if os.path.exists(os.path.basename(virtio_win_name)):
                                self.virtio_win_name_list.append(os.path.basename(virtio_win_name))
                                os.chdir(self.nfspath)
                                __create_soft_link(os.path.basename(virtio_win_name), value)
                                __create_soft_link(value, key)

        for image in image_type:
            __create(image)

    def __make_dir(self):
        """
        Create directory
        :return:
        """
        logger.info('Start to create nfs mountpoint: {}'.format(self.nfspath))
        if not os.path.exists(self.nfspath):
            os.mkdir(self.nfspath)

        logger.info('Start to create working directory: {}'.format(self.workdir))
        if not os.path.exists(self.workdir):
            os.mkdir(self.workdir)

    def umount_dir(self):
        """
        Umount directory
        :return:
        """
        if os.path.ismount(self.nfspath):
            u1 = subprocess.Popen("umount -l {}".format(self.nfspath),
                                  shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data, data_err = u1.communicate()
            # if data_err.find('not mounted'):
            #     logger.error('Umount error: {}'.format(data_err))
            if not u1.returncode == 0:
                logger.error("Fail to umount because of the following error: {}".format(data_err))
                return
        self.__clean()

    def mount_dir(self):
        """
        Mount directory
        :return:
        """
        self.umount_dir()
        self.__make_dir()
        virtio_win_nfs_server = "mount -t nfs %s %s" % (self.nfsserver, self.nfspath)
        m1 = subprocess.Popen(virtio_win_nfs_server, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data, data_err = m1.communicate()
        if not m1.returncode == 0:
            logger.error("mounting {} got error {}".format(virtio_win_nfs_server, data_err))
            exit(1)

    def __clean(self):
        """
        Clean everything such as the downloaded package, the mounted dir and etc.
        :return:
        """
        if os.path.exists(self.nfspath) and not os.path.ismount(self.nfspath):
            os.rmdir(self.nfspath)
        if os.path.exists(self.workdir):
            shutil.rmtree(self.workdir)

    def update_virtio_win(self):
        logger.info('Start to update virtio_win, Please wait for a while.')
        self.mount_dir()
        if not self.check_virtio_win():
            self.download()
            self.decompress_rpm_package()
            self.copy_to_nfs()
            self.make_link()
            self.umount_dir()
        else:
            logger.warn('{} exists, will not recreate it.'.format(self.get_latest_virtio_win_name()))

    def __str__(self):
        pass


def main():
    """
    working function of all.
    """
    # froce_create = False

    logger.debug('Start init Env:')
    cfg = ConfigParser.ConfigParser()
    cfg.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'virtio_win.cfg'))
    base = 'BASE'
    nfsserver = cfg.get(base, 'nfsserver')
    nfspath = cfg.get(base, 'nfspath')
    packagename = cfg.get(base, 'package_name')
    rhel = cfg.get(base, 'os_list').split()
    workdir = cfg.get(base, 'workdir')
    decompressed_dir = cfg.get(base, 'decompressed_dir')
    maintainer = cfg.get(base, 'maintainer')
    sender = maintainer.split('@')[0]
    sender = "{} <{}>".format(sender, maintainer)
    notification_list = cfg.get(base, 'notification_list').split()
    subject = cfg.get(base, 'subject')
    content = open(os.path.join(os.path.dirname(__file__), 'mailcontent'), 'r').read()

    virtio_win_version = ""
    name_list = []

    for osname in rhel:
        logger.info("rhel version is {}".format(osname))
        tag = cfg.get(osname, 'tagname').split()
        logger.info("virtio_win tag is {}".format(tag))
        if osname.find('RHEL7') != -1:
            virtio_win_version = 'el7'
            logger.info('virtio_win_version is {}'.format(virtio_win_version))
        if osname.find('RHEL6') != -1:
            virtio_win_version = 'el6'
            logger.info('virtio_win_version is {}'.format(virtio_win_version))

        update_virtio_win_package = UpdateVirtioWin(
            tag, packagename, virtio_win_version, nfspath, workdir, nfsserver, decompressed_dir)
        update_virtio_win_package.update_virtio_win()
        content = content.replace('NFS_SERVER', update_virtio_win_package.nfsserver)
        name_list = update_virtio_win_package.virtio_win_name_list

    if name_list:
        content = content.replace('VIRTIO_WIN', ' '.join(name_list))
        mail_sent(notification_list, subject, content, sender)


if __name__ == '__main__':
    logcfgfile = 'logfile.cfg'
    logging.config.fileConfig(os.path.join(os.path.dirname(__file__), logcfgfile))
    logger = logging.getLogger('root')
    main()
