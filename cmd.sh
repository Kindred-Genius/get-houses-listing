
sudo yum update
sudo yum install git

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh

conda create --name gethouses python=3.10
conda activate gethouses

conda install beautifulsoup4 requests selenium -y 

wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux-aarch64.tar.gz

git clone https://github.com/Kindred-Genius/get-houses-listing.git