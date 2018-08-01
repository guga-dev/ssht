import configparser
from ssht import Database
import time

def main():
     config = configparser.ConfigParser()
     config.read('properties.ini')

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

if __name__ == '__main__':
    main()
