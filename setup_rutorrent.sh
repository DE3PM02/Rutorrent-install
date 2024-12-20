#!/bin/bash

# Update and upgrade the system
echo "Updating the system..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "Installing required packages..."
sudo apt install -y apache2 php php-cli php-curl php-xml php-json php-mbstring php-intl curl unzip git libapache2-mod-scgi mediainfo ffmpeg rtorrent

# Configure rTorrent
echo "Configuring rTorrent..."
cat <<EOF > ~/.rtorrent.rc
# Directory for downloads
directory = ~/Downloads

# Session directory
session = ~/.session

# SCGI Port for ruTorrent
scgi_port = 127.0.0.1:5000

# Encryption settings
encryption = allow_incoming,try_outgoing,enable_retry
EOF

# Create necessary directories for rTorrent
mkdir -p ~/Downloads ~/.session

# Download and set up ruTorrent
echo "Downloading ruTorrent v4.3.8..."
cd /var/www/html
sudo wget https://github.com/Novik/ruTorrent/archive/refs/tags/v4.3.8.tar.gz
sudo tar -xvzf v4.3.8.tar.gz
sudo mv ruTorrent-4.3.8 rutorrent
sudo rm v4.3.8.tar.gz

# Set permissions for ruTorrent
echo "Setting permissions for ruTorrent..."
sudo chown -R www-data:www-data rutorrent
sudo chmod -R 775 rutorrent

# Configure Apache for ruTorrent
echo "Configuring Apache for ruTorrent..."
cat <<EOF | sudo tee /etc/apache2/sites-available/rutorrent.conf
<VirtualHost *:80>
    ServerName localhost
    DocumentRoot /var/www/html/rutorrent

    <Directory /var/www/html/rutorrent>
        Options FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    SCGIMount /RPC2 127.0.0.1:5000
    ErrorLog \${APACHE_LOG_DIR}/rutorrent_error.log
    CustomLog \${APACHE_LOG_DIR}/rutorrent_access.log combined
</VirtualHost>
EOF

# Enable Apache modules and site
sudo a2enmod scgi
sudo a2ensite rutorrent.conf
sudo systemctl restart apache2

# Create systemd service for rTorrent
echo "Creating systemd service for rTorrent..."
cat <<EOF | sudo tee /etc/systemd/system/rtorrent.service
[Unit]
Description=rTorrent
After=network.target

[Service]
User=$USER
Type=simple
ExecStart=/usr/bin/rtorrent
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the rTorrent service
sudo systemctl enable rtorrent
sudo systemctl start rtorrent

# Final message
echo "ruTorrent setup completed. Access it at http://localhost/rutorrent"
