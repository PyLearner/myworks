import logging
import os
import re

from autotest.client.shared import data_dir
from autotest.client.shared import error
from avocado.core import exceptions
from avocado.utils import process
from virttest import env_process
from virttest import storage


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

    # Boot up vm to make sure the guest image exists
    def test_vm():
        vm_name = params["main_vm"]
        params["start_vm"] = "yes"
        env_process.preprocess_vm(test, params, env, vm_name)
        vm = env.get_vm(vm_name)
        vm.verify_alive()

    test_vm()
    yum_cmd = params.get("yum_cmd")
    params["base_file"] = storage.get_image_filename(
        params, data_dir.get_data_dir())
    base_file = params["base_file"]

    @error.context_aware
    def create_ssh_test():
        logging.info("Prepare ssh login environment.")
        process.system(yum_cmd)
        if not os.path.exists("/usr/bin/sshpass"):
            raise exceptions.TestError(
                "Failed to install using {}".format(yum_cmd))
        logging.info("Create ssh key & copy it using ssh-copy-id")
        process.system(params.get("create_ssh_key_cmd"), shell=True)
        process.system(params.get("copy_pub_key_cmd"), shell=True)
        logging.info("Start to create snapshot based on {}".format(base_file))
        process.system(params.get("create_snapshot_cmd"), shell=True)
        params["images"] = params.get("snapshot_image")
        test_vm()

    @error.context_aware
    def create_https_test():
        logging.info("Start httpd service")
        process.system(params.get("http_conf_cmd"), shell=True)
        process.system(params.get("httpd_start_cmd"), shell=True)
        out = process.system_output(params.get("httpd_status_cmd"))
        if not re.search(params.get("httpd_status_re"), out):
            exceptions.TestError(
                "Http server fails to start, because of {}".format(out))
        logging.info("Start to create snapshot based on {}".format(base_file))
        process.system(params.get("create_snapshot_cmd"), shell=True)
        params["images"] = params.get("snapshot_image")
        test_vm()

    subcommand = params.get("subcommand")
    eval("%s_test()" % subcommand)
