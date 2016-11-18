external_snapshot_protocol = "ssh"
file_host = "localhost"
file_path = "/home"
file_host_key_check = "off"

jdict = '{{"file.driver": "{}", "file.host": "{}", '
jdict += '"file.path": "{}", "file.host_key_check": "{}"}}'
jdict = jdict.format(external_snapshot_protocol,
                     file_host,
                     file_path,
                     file_host_key_check)

jdict = '{{"file.driver": "{}", "file.host": "{}", '
jdict += '"file.path": "{}", "file.host_key_check": "{}"}}'
jdict = jdict.format(external_snapshot_protocol,
                     file_host,
                     file_path,
                     file_host_key_check)
jdict = "\'json: {}\'".format(jdict)
print(jdict)