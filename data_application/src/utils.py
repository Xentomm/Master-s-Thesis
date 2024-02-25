import json


'''
Needs config.json created
{
  "server_ip": "ip",
  "server_port": port
}
'''
def read_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config