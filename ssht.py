from sshtunnel import SSHTunnelForwarder
import pymysql

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

