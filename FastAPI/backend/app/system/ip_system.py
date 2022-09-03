import ruamel.yaml
from ruamel.yaml import YAML
import os
yaml=YAML()

file_name = '/etc/netplan/00-installer-config.yaml'
#file_name = '/home/trungnam/Documents/workspace/test_ip/ip.yaml'
config, ind, bsi = ruamel.yaml.util.load_yaml_guess_indent(open(file_name))

class IP():
    def change_ip(new_ip):
        instances = config['network']
        eth = instances['ethernets']
        lan = eth['enp3s0']
        try:
            lan['addresses'][0]= new_ip
            yaml.indent(mapping=ind, sequence=ind, offset=bsi)  
            with open(file_name, 'w') as fp:
                yaml.dump(config, fp)
        except:
            return "Error"
    def update_ip():
        os.system('sudo netplan apply')
        print("SUCCESSFULL")
