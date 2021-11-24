import mysql.connector as mysqlcon
import fire
import subprocess

# DB = mysqlcon.connect(host="localhost", user="root", password="", database="guestbook_portal")

# EXAMPLE TO USE .
# domain = "irwanyukino-wedding.xyz"
# path = "demos.migunesia.com/wedinv-999"
# event_id = 3
# python3 ww-assistant.py vhost --domain=theweddingofcitrabayu.xyz --path=demos.migunesia.com/wedinv-999 --event_id=
def vhost(domain, path, event_id, rewrite = False, protocol = 'http'):
    # update database
    sqlcursor = DB.cursor()
    sqlcursor.execute("UPDATE web_preferences SET pref_value = %s WHERE pref_group = 'general' AND pref_key = 'link' AND event_id = %s", (protocol + "://" + domain, event_id))
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
    """

    if protocol == 'https':
        vfilestr = vfilestr + """
        RewriteEngine on
        RewriteCond %{SERVER_NAME} =www."""+ domain +""" [OR]
        RewriteCond %{SERVER_NAME} ="""+ domain +"""
        RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
        """

    vfilestr = vfilestr + "</VirtualHost>"

    vfile = open("/etc/apache2/sites-available/" + domain + ".conf", "w")
    vfile.write(vfilestr.strip())

    # ini pake lets encrypt
    if protocol == "https":
        vfile_ssl_str = """
            <IfModule mod_ssl.c>
            <VirtualHost *:443>
                ServerAdmin webmaster@localhost
                ServerName """+ domain +"""
                ServerAlias www."""+ domain +"""
                DocumentRoot /var/www/"""+ path +"""
                ErrorLog ${APACHE_LOG_DIR}/error.log
                CustomLog ${APACHE_LOG_DIR}/access.log combined
            SSLCertificateFile /etc/letsencrypt/live/"""+ domain +"""/fullchain.pem
            SSLCertificateKeyFile /etc/letsencrypt/live/"""+ domain +"""/privkey.pem
            Include /etc/letsencrypt/options-ssl-apache.conf
            </VirtualHost>
            </IfModule>
        """
        vfile_ssl = open("/etc/apache2/sites-available/" + domain + "-le-ssl.conf", "w")
        vfile_ssl.write(vfile_ssl_str.strip())

    # reload apache2
    if rewrite:
        subprocess.call(["a2dissite", domain])
        subprocess.call(["a2ensite", domain])
        subprocess.call(["systemctl", "reload", "apache2"])
    else:
        subprocess.call(["a2ensite", domain])
        subprocess.call(["systemctl", "reload", "apache2"])

if __name__ == '__main__':
    fire.Fire()