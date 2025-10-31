# A script to install mac deps in /usr/local
set -e -x

bash ./clean_usr_local.sh
sudo python3 install_mac_deps.py ${GITHUB_WORKSPACE}/pygame_mac_deps \
    ${GITHUB_WORKSPACE}/pygame_mac_deps_x86_64 \
    ${GITHUB_WORKSPACE}/pygame_mac_deps_arm64
