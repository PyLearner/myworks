import logging
import os
import json
import re

from autotest.client.shared import error

from avocado.core import exceptions
from avocado.utils import process

from virttest import data_dir
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

    def create_cmd(protocol, base_file):
        file_driver = params.get("file_driver")
        jdict = ""

        if protocol == "https":
            file_ssl_verify = params.get("file_sslverify ")
            file_readahead = params.get("file_readahead")
            base_file = os.path.basename(base_file)
            file_url = "{}://{}/base_file".format(
                file_driver, params.get("remote_host"), base_file
            )
            jdict = {"file.driver": file_driver,
                     "file.url": file_url,
                     "file.sslverify": file_ssl_verify,
                     "file.readahead": file_readahead
                     }
        elif protocol == "ssh":
            file_host = params.get("remote_host")
            file_path = base_file
            file_host_key_check = params.get("file_host_key_check")
            jdict = {"file.driver": file_driver,
                     "file.host": file_host,
                     "file.path": file_path,
                     "file.host_key_check": file_host_key_check
                     }

        create_snapshot_cmd = params.get("create_snapshot_cmd").replace(
            "JDICT", "json: {}".format(jdict))
        # jdict = json.loads(json.dumps(jdict))
        # create_snapshot_cmd = params.get("create_snapshot_cmd")
        # new_jdict = "\'json: {}\'".format(jdict.replace("\'", "\""))
        # return create_snapshot_cmd + ' ' + new_jdict
        return create_snapshot_cmd

    print(create_cmd("ssh", "/home/1.vm"))
"""
    # Boot up vm to make sure the guest image exists
    def test_vm(params):
        vm_name = params["main_vm"]
        params["start_vm"] = "yes"
        env_process.preprocess_vm(test, params, env, vm_name)
        vm = env.get_vm(vm_name)
        vm.verify_alive()
        vm.destroy()

    test_vm(params)
    yum_cmd = params.get("yum_cmd")
    params["base_file"] = storage.get_image_filename(
        params, data_dir.get_data_dir())
    base_file = params["base_file"]
    print "meyang %s" % base_file

    @error.context_aware
    def create_ssh_test():
        logging.info("Prepare ssh login environment.")
        copy_pub_key_cmd = params.get("copy_pub_key_cmd")
        copy_pub_key_cmd = copy_pub_key_cmd.replace(
            "host_password", params.get("host_password"))
        process.system(yum_cmd)
        if not os.path.exists("/usr/bin/sshpass"):
            raise exceptions.TestError(
               "Failed to install using {}".format(yum_cmd))
        process.system("rm -rf /root/.ssh/id*", shell=True)
        logging.info("Create ssh key & copy it using ssh-copy-id")
        process.system(params.get("create_ssh_key_cmd"), shell=True)
        process.system(copy_pub_key_cmd, shell=True)
        process.system(params.get("ssh_agent_cmd"), shell=True)
        logging.info("Start to create snapshot based on {}".format(base_file))
        # params["images"] = "images/{}".format(params.get("snapshot_image"))
        process.system(create_cmd(params.get("file_driver"), base_file), shell=True)
        params["image_name"] = params.get("snapshot_image")
        params["image_raw_device"] = "yes"
        test_vm(params)

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

        # params["images"] = "images/{}".format(params.get("snapshot_image"))
        test_vm(params)

    subcommand = params.get("subcommand")
    eval("%s_test()" % subcommand)
"""
