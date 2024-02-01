#!/usr/bin/env bash
# Install Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'
# Create necessary folders if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file with content
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# create a symbolic link
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# ensure right permissions given
sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

# restart nginx
sudo service nginx restart
