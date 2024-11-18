
import os
import shutil
import json
import time
import subprocess

# Variables
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

def start_ngrok_http(tunnel_port, ngrok_authtoken):
    # Check if ngrok is installed
    if not shutil.which('ngrok'):
        os.system('wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -P /tmp')
        os.system('tar -xvzf /tmp/ngrok-v3-stable-linux-amd64.tgz -C /tmp')
        os.system('sudo mv /tmp/ngrok /usr/local/bin/')
        os.remove('/tmp/ngrok-v3-stable-linux-amd64.tgz')
        
    # Set ngrok authtoken
    os.system(f'ngrok config add-authtoken "{ngrok_authtoken}"')

    # Start ngrok tunnel
    os.system(f'ngrok http {tunnel_port} &')
    time.sleep(2)  # Wait for ngrok to initialize
    
    # Get the public URL
    try:
        tunnel_url = os.popen('curl -s http://localhost:4040/api/tunnels').read()
        url_data = json.loads(tunnel_url)
        public_url = url_data['tunnels'][0]['public_url']
        return public_url
    except (IndexError, KeyError, json.JSONDecodeError):
        raise Exception("Failed to retrieve the Ngrok public URL. Ensure Ngrok is running properly.")

# Example Usage
if __name__ == "__main__":
    port = 80
    authtoken = "2gynWmWAm7MTaVOHPzAo1eTCbbb_4CtFK6bpGQp6HLwn87Rjm"
    try:
        ngrok_url = start_ngrok_http(port, authtoken)
        print(f"Ngrok public URL: {ngrok_url}")
    except Exception as e:
        print(f"Error: {e}")
