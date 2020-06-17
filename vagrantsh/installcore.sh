# Update apt cache
apt update

# Generic packages
apt -y install wget
apt -y install python3.6
apt -y install python3-pip

# Install quagga
apt -y install quagga

# URL to download core
COREPKG=https://github.com/coreemu/core/archive/release-6.2.0.tar.gz

wget -c $COREPKG

tar -zxf release-6.2.0.tar.gz

python3 -m pip install -r core-release-6.2.0/daemon/requirements.txt

apt -y install git automake pkg-config gcc libev-dev ebtables iproute2 \
    python3.6 python3.6-dev python3-pip python3-tk tk libtk-img ethtool autoconf \
    mgen traceroute snmpd snmp-mibs-downloader snmptrapd \
    mgen-doc make libreadline-dev imagemagick help2man apache2

python3 -m pip install grpcio-tools

# Install wireshark enabled for non-root users
DEBIAN_FRONTEND=noninteractive apt -y install wireshark
echo "wireshark-common wireshark-common/install-setuid boolean true" | debconf-set-selections
DEBIAN_FRONTEND=noninteractive dpkg-reconfigure wireshark-common
usermod -a -G wireshark vagrant

cd core-release-6.2.0
./bootstrap.sh
./configure
make
make install

systemctl daemon-reload
systemctl start core-daemon
