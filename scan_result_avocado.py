#!/usr/bin/python

"""
Program that parses the avocado results ,will use the results.json
file as the input filename, the defualt dir is ~/avocado/job-results/latest/,
or you could specify it .

"""
__version__ = '1.1'

import os
import json
import argparse
from avocado.core import data_dir

def parse_result(resultfile):
    with open(resultfile, 'r') as f:
        data = json.load(f)

    max_width = 0
    for i in data['tests']:
        max_width = max(max_width,len(i['test']))

    nice_results(max_width, "Test", "Status", "Seconds", "Info")
    nice_results(max_width, "----", "------", "-------", "----")
    for i in data['tests']:
        if i['fail_reason'] == 'None':
            nice_results(max_width, i['test'], i['status'], round(i['time']), '')
        else:
            nice_results(max_width, i['test'], i['status'], round(i['time']),
                         i['fail_reason'])

def nice_results(max_width, casename, status, seconds, reason=''):
    # TODO: how to make the results look more beautiful
    print_format = '%%-%ds    %%-8s  %%-10s %%-8s' % max_width
    print print_format % (casename, status, seconds, reason)

if __name__ == '__main__':
    # Default to use the directory latest
    statusfile = 'results.json'
    log_dir = data_dir.get_logs_dir()
    result_file = os.path.join(log_dir, "latest/", statusfile)

    parser_a = argparse.ArgumentParser(description="show avocado results.")
    parser_a.add_argument('-f', '--filepath',
                          help='path of the results file results.json',
                          dest='filepath', action='store')

    arguments = parser_a.parse_args()

    if arguments.filepath is None:
        parse_result(result_file)
    elif os.path.exists(os.path.join(arguments.filepath, statusfile)):
        parse_result(os.path.join(arguments.filepath, statusfile))
    else:
        print "Input filepath is wrong ,please check it"
