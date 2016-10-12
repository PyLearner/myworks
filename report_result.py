#!/usr/bin/python

import json
import os
import subprocess
import time

caselog = "/home/log_file.html"
job_id_file = '/home/job_env.txt'
log_nfs_mount_dir = '/tmp/LOG'
result_src_dir = '/root/avocado/job-results/latest'
parse_file = '%s/results.json' % result_src_dir
result_src_case_dir = '%s/test-results' % result_src_dir
number = 1
with open(job_id_file, 'r') as job_f:
    job_id = job_f.read().strip()
    # hide the url
    log_nfs_url =  '%s' % job_id
    result_dst_dir = '%s/%s' % (log_nfs_mount_dir, job_id)
    if not os.path.exists(result_dst_dir):
        p1 = subprocess.Popen('mkdir %s' % result_dst_dir, shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        p1.communicate()
        if p1.returncode != 0:
            print p1.returncode
            print "mkdir failed"

#submit case results to beaker
def submit_result(number, casename, result, caselog, time=None):
    # copy log to log_nfs_mount_dir
    # copy_log_cmd = 'cp -r %s/%s %s' % (result_src_case_dir, casename, result_dst_dir)
    # print "copy_log_cmd %s" % copy_log_cmd
    # u1 = subprocess.Popen(copy_log_cmd, shell=True, stdout=subprocess.PIPE,
    #                       stderr=subprocess.PIPE)
    # u1.communicate()
    # if u1.returncode != 0:
    #     print "copy case to nfs mount directory [ %s ] failed !" % result_dst_dir

    case_url = "%s/%s" % (log_nfs_url, casename)
    submit_to_beaker_cmd = "rhts-report-result"
    submit_to_beaker_cmd += " %s.%s %s %s %s" % (number, casename, result, caselog, time)
    f = open(caselog, 'w+')
    f.write(case_url)
    f.close()
    f1 = subprocess.Popen(submit_to_beaker_cmd, shell=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    f1.communicate()
    if f1.returncode != 0:
        print "submit failed!"

while True:
    if os.path.exists(parse_file):
        break
    time.sleep(10)


with open(parse_file) as status_f:
    result_json = json.load(status_f)
    all_test_case = result_json['tests']
for i in all_test_case:
    if i['status'] != 'PASS':
        i['status'] = 'FAIL'
    submit_result(number, i['test'], i['status'], caselog, i['start'])
    number = number + 1
# scan the results.json,the results.json file will be generated when the whole test
# is complete
# submitted_test = []
# while True:
#     with open(parse_file) as status_f:
#         result_json = json.load(status_f)
#         all_test_case = result_json['tests']
#
#     for i in all_test_case:
#         if submitted_test.count(i['test']) == 0:
#             if i['status'] != 'PASS':
#                 i['status'] = 'FAIL'
#             submit_result(number, i['test'], i['status'], caselog, i['start'])
#             print "status: %s" % i['status']
#             number = number + 1
#             submitted_test.append(i['test'])
