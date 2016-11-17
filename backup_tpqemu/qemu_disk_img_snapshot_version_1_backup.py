import logging
import os
import re
import shutil

from autotest.client.shared import error

from avocado.core import exceptions
from avocado.utils import process

from virttest import data_dir
from virttest import env_process
from virttest import storage
from qemu.tests import qemu_disk_img


def run(test, params, env):
    """
    live_snapshot test:
    1). Create live snapshot during big file creating
    2). Create live snapshot when guest reboot
    3). Check if live snapshot is created
    4). Shutdown guest

    :param test: Kvm test object
    :param params: Dictionary with the test parameters
    :param env: Dictionary with test environment.
    """

    def create_cmd(protocol, base_f):
        file_driver = params.get("file_driver")
        jdict = ""

        if protocol == "https":
            file_ssl_verify = params.get("file_sslverify")
            file_readahead = params.get("file_readahead")
            base_f = os.path.basename(base_f)
            file_url = "{}://{}/{}".format(
                file_driver, params.get("remote_host"), base_f)
            jdict = '{"file.driver": %s, "file.url": %s, '
            jdict += '"file.sslverify": %s, "file.readahead": %s}'
            jdict = jdict % ('\"%s\"' % file_driver,
                             '\"%s\"' % file_url,
                             '\"%s\"' % file_ssl_verify,
                             '\"%s\"' % file_readahead)
        elif protocol == "ssh":
            file_host = params.get("remote_host")
            file_path = base_f
            file_host_key_check = params.get("file_host_key_check")
            jdict = '{"file.driver": %s, "file.host": %s, '
            jdict += '"file.path": %s, "file.host_key_check": %s}'
            jdict = jdict % ('\"%s\"' % file_driver,
                             '\"%s\"' % file_host,
                             '\"%s\"' % file_path,
                             '\"%s\"' % file_host_key_check)
        create_snapshot_cmd = params.get("create_snapshot_cmd").replace(
            "JDICT", "\'json: {}\'".format(jdict))

        return create_snapshot_cmd

    def get_vm():
        vm_name = params["main_vm"]
        params["start_vm"] = "yes"
        env_process.preprocess_vm(test, params, env, vm_name)
        vm = env.get_vm(vm_name)
        vm.verify_alive()
        session = vm.wait_for_login()

        return session

    session = get_vm()
    session.close()
    yum_cmd = params.get("yum_cmd")
    params["base_file"] = storage.get_image_filename(
        params, data_dir.get_data_dir())
    base_file = params["base_file"]

    @error.context_aware
    def create_ssh_test():
        logging.info("Prepare ssh login environment.")
        copy_pub_key_cmd = params.get("copy_pub_key_cmd")
        copy_pub_key_cmd = copy_pub_key_cmd.replace(
            "host_password", params.get("host_password"))
        user_profile = params.get("user_profile")
        user_profile_backup = params.get("user_profile_backup")

        process.system(yum_cmd)
        if not os.path.exists("/usr/bin/sshpass"):
            raise exceptions.TestError(
               "Failed to install using {}".format(yum_cmd))

        process.system("rm -rf /root/.ssh/id*", shell=True)
        logging.info("Create ssh key & copy it using ssh-copy-id")
        process.system(params.get("create_ssh_key_cmd"), shell=True)
        logging.info("Copy the ssh public key to remote host")
        process.system(copy_pub_key_cmd, shell=True, env=os.environ)
        logging.info("backup the profile {}".format(user_profile))
        shutil.copy(user_profile, user_profile_backup)

        try:
            logging.info("Start to create snapshot based on {}".format(base_file))
            create_snapshot_cmd = create_cmd(params.get("file_driver"), base_file)
            process.system(create_snapshot_cmd, shell=True)
            params["image_name"] = params.get("snapshot_image")
            params["image_raw_device"] = "yes"
            ssh_cfg = process.system_output("cat /root/.bash_profile", shell=True)
            ssh_sock = re.search("(SSH_AUTH_SOCK)=(.*?);", ssh_cfg)
            ssh_pid = re.search("(SSH_AGENT_PID)=(\d+);", ssh_cfg)
            command_prefix = "%s=%s;export %s;"
            command_prefix += "%s=%s;export %s;"
            ssh_auth_sock = ssh_sock.group(1)
            ssh_sock_path = ssh_sock.group(2)
            ssh_agent_pid = ssh_pid.group(1)
            ssh_pid_num = ssh_pid.group(2)

            params["qemu_command_prefix"] = command_prefix % (
                                                ssh_auth_sock,
                                                ssh_sock_path,
                                                ssh_auth_sock,
                                                ssh_agent_pid,
                                                ssh_pid_num,
                                                ssh_agent_pid)

            session = get_vm()
            snapshot_md5 = get_md5(session)
            session.close()
            compare_md5(base_md5, snapshot_md5)
        finally:
            shutil.copy(user_profile_backup, user_profile)
            process.kill_process_by_pattern("ssh-agent")

    @error.context_aware
    def create_https_test():
        process.system("yum install -y mod_ssl")
        logging.info("Start httpd service")
        process.system(params.get("http_conf_cmd"), shell=True)
        process.system(params.get("httpd_start_cmd"), shell=True)
        out = process.system_output(params.get("httpd_status_cmd"))
        if not re.search(params.get("httpd_status_re"), out):
            err = "Http server fails to start, because of {}".format(out)
            exceptions.TestError(err)
        logging.info("Start to create snapshot based on {}".format(base_file))

        create_snapshot_cmd = create_cmd(params.get("file_driver"), base_file)
        output = ""
        try:
            output = process.system_output(create_snapshot_cmd, shell=True)
        except:
            raise exceptions.TestFail("Fail to create snapshot images: {}".format(output))
        session = get_vm()
        snapshot_md5 = get_md5(session)
        session.close()
        compare_md5(base_md5, snapshot_md5)

    subcommand = params.get("subcommand")
    eval("%s_test()" % subcommand)
