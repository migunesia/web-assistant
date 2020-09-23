import mysql.connector as mysqlcon
import fire
import subprocess

DB = mysqlcon.connect(host="localhost", user="root", password="", database="guestbook_portal")

# EXAMPLE TO USE 
# domain = "irwanyukino-wedding.xyz"
# path = "demos.migunesia.com/wedinv-999"
# event_id = 3
# python3 ww-assistant.py vhost --domain=theweddingofcitrabayu.xyz --path=demos.migunesia.com/wedinv-999 --event_id=
def vhost(domain, path, event_id):
    # update database
    sqlcursor = DB.cursor()
    sqlcursor.execute("UPDATE web_preferences SET pref_value = %s WHERE pref_group = 'general' AND pref_key = 'link' AND event_id = %s", ("http://" + domain, event_id))
    DB.commit()

    # create file virtual host for ubuntu 
    vfilestr = """
    <VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName """ + domain + """
    ServerAlias www.""" + domain + """
    DocumentRoot /var/www/""" + path + """
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>"""
    vfile = open("/etc/apache2/sites-available/" + domain + ".conf", "w")
    vfile.write(vfilestr.strip())

    # reload apache2
    subprocess.call(["systemctl", "reload", "apache2"])

if __name__ == '__main__':
    fire.Fire()