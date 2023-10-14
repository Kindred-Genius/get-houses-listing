

sudo apt-get update && sudo apt-get upgrade -y

sudo apt install git unzip wget curl firefox -y

curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64-2.0.30.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh

conda create --name gethouses python=3.10

conda activate gethouses

conda install beautifulsoup4 requests selenium boto3 pandas -y 

wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux-aarch64.tar.gz
wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip

git clone https://github.com/Kindred-Genius/get-houses-listing.git




ssh-keygen -t rsa -b 4096 -C "emailaddress@example.com"

export PATH="$PATH:/home/ubuntu/firefoxdriver"
export PATH="$PATH:/Users/aba/home/utils/firefoxdriver"
export PATH="$PATH:/Users/aba/home/utils/chromedriver"

sudo yum update
sudo yum install git
chromium --headless --dump-dom 'https://www.orpi.com/recherche/buy?realEstateTypes[]=maison&locations[0][value]=vernon&locations[0][label]=Vernon (27200)&sort=date-down&layoutType=mixte&recentlySold=false' > ~/orpi.html