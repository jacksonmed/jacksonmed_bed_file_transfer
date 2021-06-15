import paramiko
from scp import SCPClient
import yaml

stream = open("config.yaml", 'r')
configuration = yaml.load(stream)


class Transfer:
    def __init__(self, server, port, user, password, file_path):
        self.client = createSSHClient(server, port, user, password)
        self.ssh = createSSHClient(server, port, user, password)
        self.scp = SCPClient(self.ssh.get_transport())
        self.file_path = file_path

    def scp_get(self):
        self.scp.get()
        return

    def scp_put(self):
        self.scp.put(self.file_path, configuration['RASPBERRY_PI']['DESTINATION_PATH'])
        return


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client
