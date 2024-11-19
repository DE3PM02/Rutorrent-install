#!/bin/bash

# Define variables
USER_NAME=$(whoami)
RUTORRENT_DIR="/var/www/html/rutorrent"
RTORRENT_SESSION="/home/$USER_NAME/.session"

echo "Starting ruTorrent installation..."

# Update the system
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "Installing required packages..."
sudo apt install -y apache2 php php-cli php-curl php-xmlrpc libapache2-mod-php unzip curl ffmpeg mediainfo sox unrar procps python3 build-essential libssl-dev libcurl4-openssl-dev pkg-config libncurses5-dev apache2-utils automake autotools-dev autoconf

# Install rTorrent and libTorrent
echo "Installing rTorrent and libTorrent..."
sudo apt install -y rtorrent

# Create rTorrent session directory
mkdir -p "$RTORRENT_SESSION"
chmod -R 775 "$RTORRENT_SESSION"

# Restart rTorrent
pkill rtorrent 2>/dev/null
nohup rtorrent &

# Install ruTorrent
echo "Installing ruTorrent..."
sudo mkdir -p "$RUTORRENT_DIR
sudo chown -R www-data:www-data "$RUTORRENT_DIR"
cd /var/www/html || exit

# Set permissions for ruTorrent directories
sudo chown -R www-data:www-data "$RUTORRENT_DIR"
sudo chmod -R 775 "$RUTORRENT_DIR"

# Configure Apache for ruTorrent
echo "Configuring Apache..."
sudo a2enmod rewrite ssl
cat <<EOF | sudo tee /etc/apache2/sites-available/rutorrent.conf
<VirtualHost *:80>
    ServerName localhost
    DocumentRoot $RUTORRENT_DIR
    <Directory "$RUTORRENT_DIR">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
EOF
sudo a2ensite rutorrent.conf
sudo systemctl restart apache2

# Final checks
echo "Installation completed! You can access ruTorrent at http://<your-server-ip>/rutorrent"
