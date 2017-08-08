set -e -x

git submodule init
git submodule update
git remote set-url origin https://github.com/coala/corobo.git
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install -y gcc-4.9 g++-4.9
sudo rm /usr/bin/x86_64-linux-gnu-gcc
sudo ln -s `which gcc-4.9` /usr/bin/x86_64-linux-gnu-gcc
