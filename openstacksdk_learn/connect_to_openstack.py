import sys

from openstack import connection
from openstack import profile
from openstack import utils

# open logging
# utils.enable_logging(debug=True, stream=sys.stdout)

# get the connection to the
def create_connection(auth_url, region, project_name, username, password):
    prof = profile.Profile()
    prof.set_region(profile.Profile.ALL, region)

    return connection.Connection(
        profile=prof,
        user_agent='meyang',
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password
    )

def print_obj_attr(obj):
    for i, j in vars(obj).iteritems():
        print("{}: {}".format(i, j))

region_name = "RegionOne"
auth_url = "http://10.73.196.159:5000/v2.0"
project_name = "demo"
username = "demo"
password = "eff0c92ada2947e9"
# password = "6c09b652e0df4029"
conn = create_connection(auth_url=auth_url,
                         region=region_name,
                         project_name=project_name,
                         username=username,
                         password=password)

# for i in conn.compute.servers():
#     print(i.addresses)
#     print(i.status)
#     print(i.vm_state)
#     for j, k in vars(i).iteritems():
#         print("%s: %s" %(j, k))

for i in conn.compute.servers():
    print(i.to_dict())

for i in conn.block_store.volumes():
    print(i.to_dict())