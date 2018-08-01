from .ssht import Database
import time

if __name__ == '__main__':

     serverTunnel = { 'host': "200.54.242.52",
             'sshUsername': "grojas",
             'sshPKEY': "/Users/grojas/.ssh/id_rsa",
             'remoteBindPort': 3306 }

     s = Database("mysql").connectTunnel(serverTunnel)
     s.start()
     print(s.local_bind_port)  # show assigned local port
     time.sleep(3)

     dbInfo = { 'user':'mobility',
             'host': '127.0.0.1',
             'passwd': 'TIDChile.2017',
             'db': 'mobility_CDR',
             'port': s.local_bind_port }

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
