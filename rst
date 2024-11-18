#!/bin/bash

# Update the package list
sudo apt update -y && sudo apt upgrade -y

# Install required dependencies
sudo apt install -y apache2 php libapache2-mod-php php-cli php-json php-curl php-xmlrpc php-intl php-mysql php-gd \
php-pear php-xml php-mbstring php-zip unzip curl ffmpeg mediainfo nginx wget git

# Install rTorrent dependencies
sudo apt install -y rtorrent xmlrpc-c libtorrent-dev

# Create directories for ruTorrent and rTorrent
sudo mkdir -p /var/www/rutorrent
sudo mkdir -p ~/.session
sudo mkdir -p ~/Downloads

# Clone the ruTorrent repo
sudo git clone https://github.com/Novik/ruTorrent.git /var/www/rutorrent

# Set proper permissions
sudo chown -R www-data:www-data /var/www/rutorrent
sudo chmod -R 775 /var/www/rutorrent

# Configure rTorrent
cat << EOF > /home/$(whoami)/.rtorrent.rc
# rTorrent configuration file
directory = ~/Downloads
session = ~/.session
port_range = 40000-50000
port_random = yes
dht.mode.set = auto
min_peers = 1
max_peers = 100
min_peers_seed = 1
max_peers_seed = 100
max_downloads_global = 250
max_uploads_global = 250
download_rate = 0
upload_rate = 0
trackers.numwant.set = 100
network.http.max_open.set = 50
network.max_open_files.set = 600
network.max_open_sockets.set = 300
encryption = allow_incoming,try_outgoing,enable_retry
scgi_port = 127.0.0.1:5000
EOF

# Install and configure Nginx
sudo cat << EOF > /etc/nginx/sites-available/rutorrent
server {
    listen 80;

    server_name localhost;

    root /var/www/rutorrent;

    index index.php index.html index.htm;

    location /RPC2 {
        include scgi_params;
        scgi_pass 127.0.0.1:5000;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
        include fastcgi_params;
    }

    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF

# Enable Nginx configuration
sudo ln -s /etc/nginx/sites-available/rutorrent /etc/nginx/sites-enabled/rutorrent
sudo nginx -t
sudo systemctl restart nginx

# Start rTorrent
screen -dmS rtorrent rtorrent

# Install ruTorrent plugins (optional)
cd /var/www/rutorrent/plugins
sudo git clone https://github.com/xombiemp/rutorrentMobile.git mobile

# Finish up
echo "ruTorrent and rTorrent have been installed successfully."
echo "Visit http://localhost/ in your web browser to access ruTorrent."
