from sys import argv

from netmiko import ConnectHandler
import re
from datetime import datetime


# TODO parsing arguments and overwrite parameters from config files
# if len(argv) > 1:
#     pass
# print(len(argv), ', ',argv)
# exit(1)


def getbworkdata(net_connect):
    output = net_connect.send_command('display current-configuration ')
    m = re.search('sysname ([\S]+)', output)
    if m:
        sysname = m.group(1)
    else:
        sysname = ip

    config_file = DIR + sysname + '_config_' + timestamp + '.txt'
    with open(config_file, 'w') as f:
        f.write(output)
    print('zapisalem ', config_file)

    output = net_connect.send_command('display ont info summary 0')
    find  = re.findall('[0-9]+\s+(48[0-9A-F]+\s\S+\s+[0-9]+\s+\S+\s+\S+)', output)
    print (sysname, '@', ip, ' znalazlem aktywnych ont: ', str(len(find)))
    active_file = DIR + sysname + '_active_' + timestamp + '.txt'
    with open(active_file,'w') as f:
        f.write('found active onts: ' + str(len(find)) + '\n')
        for m in find:
            f.write(m + '\n')

    print('zapisalem ', active_file)

for ip in device_ips:
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    olt = {
        'device_type': 'huawei_olt',
        'host': ip,
        'username': USERNAME,
        'password': PASSWORD,
    }
    net_connect = ConnectHandler(**olt)
    net_connect.enable()

    # pobranie versji i wyswietlenie części version / patch / product
    output = net_connect.send_command('display version ')
    re.findall(output, '')