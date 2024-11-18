
import os
import shutil
import subprocess

# Variables
tunnel_type = "Ngrok"  # Options: "Ngrok", "Argo Tunnel"
ngrok_authtoken = "2gynWmWAm7MTaVOHPzAo1eTCbbb_4CtFK6bpGQp6HLwn87Rjm"
tunnel_port = 80
RUTorrent_Mobile = True  # Enable ruTorrent Mobile

# Directories
base_dir = os.path.expanduser("~")
downloads_dir = os.path.join(base_dir, "Downloads")
rtorrent_dir = os.path.join(base_dir, "rTorrent")
session_dir = os.path.join(rtorrent_dir, "session")
rutorrent_dir = os.path.join(base_dir, "ruTorrent")

# Create directories
os.makedirs(downloads_dir, exist_ok=True)
os.makedirs(rtorrent_dir, exist_ok=True)
os.makedirs(session_dir, exist_ok=True)
os.makedirs(rutorrent_dir, exist_ok=True)

# Install dependencies
os.system('sudo apt-get install -y rtorrent mediainfo sox screen php php-fpm php-json php-curl php-xml apache2 libapache2-mod-php')

# Install Python dependencies
os.system('pip install cloudscraper')

# Download and configure rTorrent
rtorrent_rc_path = os.path.expanduser("~/.rtorrent.rc")
os.system(f'wget "https://github.com/Monster013/25-63369/raw/refs/heads/main/rtorrent.rc" -O "{rtorrent_rc_path}"')

# Start rTorrent in a detached screen session
subprocess.Popen(['screen', '-d', '-m', '-fa', '-S', 'rtorrent', 'rtorrent'])
print("rTorrent started successfully!")

# Download and setup ruTorrent
print("Downloading ruTorrent...")
os.system('curl -L https://github.com/Novik/ruTorrent/archive/refs/tags/v4.3.8.tar.gz -o v4.3.8.tar.gz')
os.system(f'tar -xzf v4.3.8.tar.gz -C {base_dir}')
os.system(f'mv {os.path.join(base_dir, "ruTorrent-4.3.8")}/* {rutorrent_dir}')
os.remove("v4.3.8.tar.gz")

# Add ruTorrent Mobile plugin
if RUTorrent_Mobile:
    os.system(f'git clone https://github.com/xombiemp/rutorrentMobile.git {os.path.join(rutorrent_dir, "plugins/mobile")}')

# Configure ruTorrent with Apache
print("Setting up ruTorrent with Apache...")
apache_conf_path = os.path.join(base_dir, "rutorrent.conf")
os.system(f'curl -L https://raw.githubusercontent.com/Monster013/25-63369/refs/heads/main/rutorrent.conf -o {apache_conf_path}')
os.system(f'sudo mv {apache_conf_path} /etc/apache2/sites-available/rutorrent.conf')
os.system('sudo a2ensite rutorrent')
os.system('sudo systemctl restart apache2')

# Tunnel setup
if tunnel_type == "Ngrok":
    print("Starting Ngrok Tunnel...")
    os.system(f'ngrok authtoken {ngrok_authtoken}')
    os.system(f'ngrok http {tunnel_port}')
elif tunnel_type == "Argo Tunnel":
    print("Starting Argo Tunnel...")
    os.system(f'cloudflared tunnel --url http://localhost:{tunnel_port}')

print("ruTorrent is ready. Access it via the tunnel URL.")
