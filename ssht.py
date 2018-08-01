from sshtunnel import SSHTunnelForwarder
import pymysql
import time
import configparser

class Database:

    server = None
    conn = None
    def __init__(self, motor):
        self.motor = motor

    def connectTunnel(self, serverTunnel):
        server = SSHTunnelForwarder(
            serverTunnel['host'],
            ssh_username=serverTunnel['sshUsername'],
            ssh_pkey=serverTunnel['sshPKEY'],
            remote_bind_address=(serverTunnel['remoteBindAddress'], serverTunnel['remoteBindPort']),
            local_bind_address=(serverTunnel['localBindAddress'], serverTunnel['localBindPort']) # optional line
        )
        return server
    def connectDB(self, dbInfo):
        conn = pymysql.connect(host=dbInfo['host'], user=dbInfo['user'], passwd=dbInfo['passwd'], db = dbInfo['db'], port=dbInfo['port'])
        return conn


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('properties.temp')

    serverTunnel = { 'host': config['sshserver']['Host'],
            'sshUsername': config['sshserver']['SSHUsername'],
            'sshPKEY': config['sshserver']['SSHPKey'],
            'remoteBindPort': int(config['sshserver']['RemoteBindPort']),
            'remoteBindAddress': config['sshserver']['RemoteBindAddress'],
            'localBindAddress': config['sshserver']['LocalBindAddress'],
            'localBindPort': int(config['sshserver']['LocalBindPort'])}

    s = Database("mysql").connectTunnel(serverTunnel)
    s.start()
    # print(s.local_bind_port)  # show assigned local port
    time.sleep(3)

    dbInfo = { 'user': config['mysql']['User'],
            'host': config['mysql']['Host'],
            'passwd': config['mysql']['Passwd'],
            'db': config['mysql']['DB'],
            'port': int(config['sshserver']['LocalBindPort'])}

    c = Database("mysql").connectDB(dbInfo)
    time.sleep(3)

    cur = c.cursor()
    cur.execute("SELECT * FROM DATOMS")
    print(cur.description)

    print()

    for row in cur:
        print(row)

    cur.close()
    c.close()
    s.stop()
