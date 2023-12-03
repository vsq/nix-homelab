#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import math
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any
from typing import Callable
from typing import IO
from typing import List

import xmltodict
from deploykit import DeployGroup
from deploykit import DeployHost
from deploykit import HostKeyCheck
from invoke import Collection
from invoke import run
from invoke import task

import taskslib

ROOT = Path(__file__).parent.resolve()
os.chdir(ROOT)


RSYNC_EXCLUDES = [".git"]

# NOTE: Array order is important (Config section must be computed first)
OSSCAN = {
    "NixOS": ["Role", "Scan", "Config", "Topologie", "Hardwares", "Nix"],
    "Nix": ["Scan", "Config", "Topologie", "Hardwares", "Nix"],
    "TrueNAS": [
        "Scan",
    ],
    "TrueNAS_jail": [
        "Scan",
    ],
    "Switch": [
        "Scan",
    ],
    "XCP-ng": [
        "Scan",
    ],
    "HAOS": [
        "Scan",
    ],
    "VoidLinux": [
        "Scan",
    ],
    "ArchLinux": [
        "Scan",
    ],
    "Debian": [
        "Scan",
    ],
    "iLO4": [
        "Scan",
    ],
    "IPMI": [
        "Scan",
    ],
    "nix-darwin": [
        "Scan",
    ],
    "Android": [
        "Scan",
    ],
    "iPhone": [
        "Scan",
    ],
    "Chromecast": [
        "Scan",
    ],
    "Bridge": [
        "Scan",
    ],
    "Arris": [
        "Scan",
    ],
    "Raspbian": [
        "Scan",
    ],
    "Harmony": [
        "Scan",
    ],
    "MikroTik": [
        "Scan",
    ],
}


def get_hosts(hosts: str) -> List[DeployHost]:
    return [DeployHost(h, user="root") for h in hosts.split(",")]


def get_deploylist_from_homelab(username: str, hosts: str) -> List[DeployHost]:
    with open("homelab.json", "r") as fh:
        jinfo = json.load(fh)
        hostslist = jinfo["hosts"]

        if hosts == "":
            hostnames = hostslist.keys()
        else:
            hostnames = hosts.split(",")

        deploylist = []
        for hn in hostnames:
            dh = DeployHost(
                hostslist[hn]["ipv4"],
                user=username,
                host_key_check=HostKeyCheck.NONE,
                meta=dict(hostname=hn, os=hostslist[hn]["os"]),
            )
            deploylist.append(dh)

    return deploylist


def get_deploylist_from_role(role: str) -> List[DeployHost]:
    with open("homelab.json", "r") as fh:
        jinfo = json.load(fh)
        hostslist = jinfo["hosts"]
        hostnames = hostslist.keys()

        deploylist = []
        for hn in hostnames:
            if "roles" in hostslist[hn] and role in hostslist[hn]["roles"]:
                dh = DeployHost(
                    hostslist[hn]["ipv4"],
                    user="root",
                    meta=dict(hostname=hn, os=hostslist[hn]["os"]),
                )
                deploylist.append(dh)

    return deploylist


def color_text(code: int, file: IO[Any] = sys.stdout) -> Callable[[str], None]:
    def wrapper(text: str) -> None:
        if sys.stderr.isatty():
            print(f"\x1b[{code}m{text}\x1b[0m", file=file)
        else:
            print(text, file=file)

    return wrapper


warn = color_text(31, file=sys.stderr)
info = color_text(32)


##############################################################################
# Tasks
##############################################################################


@task
def firmware_rpi_update(c, hosts):
    for h in get_hosts(hosts):
        _firmware_rpi_update(h)


@task
def ssh_init_host_key(c, hosts, hostnames):
    """
    Init ssh host key from nixos installation
    """
    h = get_hosts(hosts)
    hn = hostnames.split(",")

    for idx in range(len(h)):
        _ssh_init_host_key(h[idx], hn[idx])


@task(name="keys")
def wireguard_keys(c, hostname):
    """
    Generate wireguard private key for <hostname>
    """

    _wireguard_keys(hostname)


# @task(name="gen-pub")
# def wireguard_gen_public_key(c, private=""):
#     """
#     Generate wireguard public key

#     If the private key is not provided,
#     it is recovered from hosts/secrets.yml
#     """

#     _wireguard_genpub(private)


# wg = Collection("wireguard")
# wg.add_task(wireguard_keys)


@task
def disk_format(c, hosts, disk, mirror="", mode="GPT", password=""):
    """
    Format disks with zfs
    """

    for h in get_hosts(hosts):
        _format_disks(h, disk, mirror, mode, password)
        _disk_mount(h, mirror, password)


@task
def disk_mount(c, hosts, mirror="", password=""):
    """
    Mount disks from the installer
    """
    for h in get_hosts(hosts):
        _disk_mount(h, mirror, password)


@task
def sync_homelab(c, hosts):
    """
    rsync currently local homelab project to future nixos installation
    """
    for h in get_hosts(hosts):
        _sync_homelab({h.host})


@task
def nixos_generate_config(c, hosts, hostnames):
    """
    Generate hardware configuration for the host
    """

    h = get_hosts(hosts)
    hn = hostnames.split(",")

    for idx in range(len(h)):
        _nixos_generate_config(h[idx], hn[idx])


##############################################################################
# Nixos
##############################################################################


@task
def nixos_install(c, hosts, flakeattr):
    """
    install nixos
    """
    for h in get_hosts(hosts):
        # Sync project
        info("Sync homelab project")
        _sync_homelab(h)

        # Install nixos
        info("Install NixOS")
        h.run(
            f"cd /mnt/nix-homelab && nix --extra-experimental-features \
            'nix-command flakes' shell nixpkgs#git -c nixos-install \
            --verbose --flake .#{flakeattr} && sync"
        )


@task(
    name="build",
    help={
        "cache": "Use binary cache from flake extra-substituers section",
        "keeperror": "Continue, if error",
        "showtrace": "Show trace on error",
    },
)
def nix_build(c, hostnames="", cache=True, keeperror=True, showtrace=False):
    """
    Test to <hostnames> server

    if <hostnames> is empty, deploy to all nix homelab server

    """
    _execute_nixos_rebuild(
        "build", hostnames, False, cache, keeperror, showtrace
    )


@task(
    name="test",
    help={
        "discovery": "get host information after deployment",
        "cache": "Use binary cache from flake extra-substituers section",
        "keeperror": "Continue, if error",
        "showtrace": "Show trace on error",
    },
)
def nix_test(
    c,
    hostnames="",
    discovery=True,
    cache=True,
    keeperror=True,
    showtrace=False,
):
    """
    Test to <hostnames> server

    if <hostnames> is empty, deploy to all nix homelab server

    """
    _execute_nixos_rebuild(
        "test", hostnames, discovery, cache, keeperror, showtrace
    )


@task(
    name="deploy",
    help={
        "discovery": "get host information after deployment",
        "cache": "Use binary cache from flake extra-substituers section",
        "keeperror": "Continue, if error",
        "showtrace": "Show trace on error",
    },
)
def nix_deploy(
    c,
    hostnames="",
    discovery=True,
    cache=True,
    keeperror=True,
    showtrace=False,
):
    """
    Deploy to <hostnames> server

    if <hostnames> is empty, deploy to all nix homelab server

    """
    _execute_nixos_rebuild(
        "switch", hostnames, discovery, cache, keeperror, showtrace
    )


@task(
    name="boot",
    help={
        "discovery": "get host information after deployment",
        "cache": "Use binary cache from flake extra-substituers section",
        "keeperror": "Continue, if error",
        "showtrace": "Show trace on error",
    },
)
def nix_boot(
    c,
    hostnames="",
    discovery=True,
    cache=True,
    keeperror=True,
    showtrace=False,
):
    """
    rebuild boot to <hostnames> server

    if <hostnames> is empty, deploy to all nix homelab server

    """
    _execute_nixos_rebuild(
        "boot", hostnames, discovery, cache, keeperror, showtrace
    )


nixos = Collection("nixos")
nixos.add_task(nix_deploy)
nixos.add_task(nix_test)
nixos.add_task(nix_build)
nixos.add_task(nix_boot)

##############################################################################
# Home-manager (user)
##############################################################################


@task(
    name="build",
    help={
        "cache": "Use binary cache from flake extra-substituers section",
        "keeperror": "Continue, if error",
        "showtrace": "Show trace on error",
    },
)
def home_build(
    c, username="", hostnames="", cache=True, keeperror=True, showtrace=False
):
    """
    Test to <hostnames> server

    if <hostnames> is empty, deploy to all nix homelab server

    """
    _execute_home_remote_deploy(
        "build", username, hostnames, cache, keeperror, showtrace
    )


@task(
    name="deploy",
    help={
        "cache": "Use binary cache from flake extra-substituers section",
        "keeperror": "Continue, if error",
        "showtrace": "Show trace on error",
    },
)
def home_deploy(
    c,
    username="",
    hostnames="",
    cache=True,
    keeperror=True,
    showtrace=False,
):
    """
    Deploy to <hostnames> server

    if <hostnames> is empty, deploy to all nix homelab server

    """
    _execute_home_remote_deploy(
        "switch", username, hostnames, cache, keeperror, showtrace
    )


home = Collection("home")
home.add_task(home_deploy)
home.add_task(home_build)


@task(
    name="build",
    help={
        "cache": "Use binary cache from flake extra-substituers section",
        "keeperror": "Continue, if error",
        "showtrace": "Show trace on error",
    },
)
def role_build(c, role, cache=True, keeperror=True, showtrace=False):
    """
    Build for all hosts contains the role
    """

    deploylist = get_deploylist_from_role(role)
    _nixos_rebuild(deploylist, "build", False, cache, keeperror, showtrace)


@task(
    name="test",
    help={
        "discovery": "get host information after deployment",
        "cache": "Use binary cache from flake extra-substituers section",
        "keeperror": "Continue, if error",
        "showtrace": "Show trace on error",
    },
)
def role_test(
    c, role, discovery=True, cache=True, keeperror=True, showtrace=False
):
    """
    Test for all hosts contains the role
    """

    deploylist = get_deploylist_from_role(role)
    _nixos_rebuild(deploylist, "test", discovery, cache, keeperror, showtrace)


@task(
    name="deploy",
    help={
        "discovery": "get host information after deployment",
        "cache": "Use binary cache from flake extra-substituers section",
        "keeperror": "Continue, if error",
        "showtrace": "Show trace on error",
    },
)
def role_deploy(
    c, role, discovery=True, cache=True, keeperror=True, showtrace=False
):
    """
    Deploy for all hosts contains the role
    """

    deploylist = get_deploylist_from_role(role)
    _nixos_rebuild(
        deploylist, "switch", discovery, cache, keeperror, showtrace
    )


role = Collection("role")
role.add_task(role_deploy)
role.add_task(role_test)
role.add_task(role_build)


@task(name="nix-serve")
def init_nix_serve(c, hosts, hostnames):
    """
    Init nix binary cache server <hostname> nix-serve private & public key
    """

    h = get_hosts(hosts)
    hn = hostnames.split(",")

    for idx in range(len(h)):
        taskslib._init_nix_serve(h[idx], hn[idx])


@task(name="domain-cert")
def cert_init_cert_domain(c):
    """
    Init domain certificate
    """
    taskslib._cert_init_cert_domain()


init = Collection("init")
init.add_task(disk_format)
init.add_task(disk_mount)
init.add_task(init_nix_serve)
init.add_task(cert_init_cert_domain)
init.add_task(ssh_init_host_key)
init.add_task(nixos_generate_config)
init.add_task(nixos_install)


@task(name="all_pages")
def doc_generate_all_pages(c):
    """
    generate all homelab documentation
    """

    _doc_update_hosts_pages()
    taskslib._doc_update_main_project_page()


@task(name="main_page")
def doc_generate_main_page(c):
    """
    generate main homelab page
    """

    taskslib._doc_update_main_project_page()


@task(name="host_pages")
def doc_generate_hosts_pages(c):
    """
    generate all homelab hosts page
    """

    _doc_update_hosts_pages()


@task(name="scan_all_hosts")
def doc_scan_all_hosts(c, hosts=""):
    """
    Retrieve all hosts system infromations
    """
    deploylist = get_deploylist_from_homelab("root", hosts)
    _scan_all_hosts(deploylist)


docs = Collection("docs")
docs.add_task(doc_generate_all_pages)
docs.add_task(doc_generate_main_page)
docs.add_task(doc_generate_hosts_pages)
docs.add_task(doc_scan_all_hosts)


##############################################################################
# Functions
##############################################################################


def _format_disks(
    host: DeployHost, disk: str, mirror: str, mode: str, zfspassphrase: str
) -> None:
    # format disk in hybrid mode (GPT and MBR) with as follow :
    # - partition 1 MBR/EFI boot partition
    # - partition 2 swap partition for system with few RAM
    # - partition 3 zfs partition

    if mode not in ["MBR", "EFI"]:
        print("Please choose MBR or EFI partition mode")
        sys.exit(1)

    diskprefix = ""

    if "nvme" in disk:
        diskprefix = "p"

    # Umount all /mnt
    host.run("umount -R /mnt", check=False)

    # swapoff
    host.run(f"swapoff {disk}{diskprefix}2", check=False)
    if mirror:
        host.run(f"swapoff {mirror}2", check=False)

    # Check previous zfs volumes
    r = host.run("zpool list | grep 'zroot'", check=False)
    if r.returncode == 0:
        host.run(
            """
        zfs destroy -r zroot
        zpool destroy zroot
        """
        )

    # Wipe & Partitioning
    host.run(
        f"sgdisk -Z -n 1:2048:+1G -n 2:+0:+8G -N 3 -t 1:ef00 -t 2:8200 -t 3:8304 {disk}"  # noqa: E501
    )

    # For legacy bios
    if mode == "MBR":
        host.run(f"sgdisk -m 1:2:3 {disk}")

    # Clone partition [If mirror mode]
    if mirror:
        host.run(f"sfdisk --dump {disk} | sfdisk {mirror}")
        zdisks = f"{disk}{diskprefix}3 {mirror}{diskprefix}3".strip()
    else:
        zdisks = f"{disk}{diskprefix}3".strip()
    # Create ZFS pool
    if mirror:
        host.run(
            f"zpool create -f -o ashift=12 -O mountpoint=none zroot mirror {zdisks}"  # noqa: E501
        )
    else:
        host.run(
            f"zpool create -f -o ashift=12 -O mountpoint=none zroot {zdisks}"
        )

    # Format boot
    host.run(
        f"""
    mkfs.vfat {disk}{diskprefix}1 -n BOOT_1ST
    test -n "{mirror}" && mkfs.vfat {mirror}{diskprefix}1 -n BOOT_2ND || true
    """
    )

    # swap
    host.run(
        f"""
    mkswap {disk}{diskprefix}2 -L SWAP_1ST
    test -n "{mirror}" && mkswap {mirror}{diskprefix}2 -L SWAP_2ND || true
    """
    )

    # public volumes
    host.run(
        """
    zfs create -o mountpoint=none -o canmount=off zroot/public
    zfs create -o mountpoint=legacy -o canmount=on -o atime=off zroot/public/nix
    zfs create -o mountpoint=legacy -o canmount=on -o atime=off zroot/public/nix-homelab
    """  # noqa: E501
    )

    # private volumes(encrypted)
    zfspool = "public"
    if zfspassphrase:
        host.run(
            f"echo '{zfspassphrase}' | zfs create -o mountpoint=none -o canmount=off -o encryption=aes-256-gcm -o keyformat=passphrase -o keylocation=prompt zroot/private"  # noqa: E501
        )
        zfspool = "private"

    # Create private or public volume
    host.run(
        f"""
    zfs create -o mountpoint=legacy -o canmount=on zroot/{zfspool}/root
    zfs create -o mountpoint=legacy -o canmount=on zroot/{zfspool}/data
    zfs create -o mountpoint=legacy -o canmount=off zroot/{zfspool}/persist
    zfs create -o mountpoint=legacy -o canmount=on zroot/{zfspool}/persist/host
    zfs create -o mountpoint=legacy -o canmount=on zroot/{zfspool}/persist/user
    """  # noqa: E501
    )

    # Show encrypted volumes
    host.run("zfs get encryption")


def _disk_mount(host: DeployHost, mirror: str, zfspassphrase: str) -> None:
    # Umount all volumes
    host.run("umount -R /mnt", check=False)

    # Re-import zpool informations
    host.run("zpool import -af")

    zfspool = "public"
    if zfspassphrase:
        host.run(
            f"echo '{zfspassphrase}' | zfs load-key zroot/private", check=False
        )
        zfspool = "private"

    # Import volumes
    host.run(
        f"""
    mount -t zfs zroot/{zfspool}/root /mnt
    mkdir -p /mnt/{{boot,boot-fallback,nix,nix-homelab,data,persist/host,persist/user}}
    mount /dev/disk/by-label/BOOT_1ST /mnt/boot
    test -n "{mirror}" && mount /dev/disk/by-label/BOOT_2ND /mnt/boot-fallback || true
    mount -t zfs zroot/public/nix /mnt/nix
    mount -t zfs zroot/public/nix-homelab /mnt/nix-homelab
    mount -t zfs zroot/{zfspool}/data /mnt/data
    mount -t zfs zroot/{zfspool}/persist/host /mnt/persist/host
    mount -t zfs zroot/{zfspool}/persist/user /mnt/persist/user
    """  # noqa: E501
    )

    # Mount swap
    host.run(
        f"""
swapon /dev/disk/by-label/SWAP_1ST
test -n "{mirror}" && swapon /dev/disk/by-label/SWAP_2ND || true
mount -o remount,nr_inodes=0,size=6G /nix/.rw-store
swapon --show
""",
        check=False,
    )


def _firmware_rpi_update(host: DeployHost) -> None:
    # USB boot configuration

    host.run("mkdir -p /firmware")
    host.run("mount /dev/disk/by-label/FIRMWARE /firmware", check=False)
    host.run(
        """
    nix-shell -p raspberrypi-eeprom --run "BOOTFS=/firmware FIRMWARE_RELEASE_STATUS=stable rpi-eeprom-update -d -a"
    cat <<EOF > /tmp/boot_nixos.conf
[all]
BOOT_UART=0
WAKE_ON_GPIO=1
POWER_OFF_ON_HALT=0
BOOT_ORDER=0xf14
EOF

    nix-shell -p raspberrypi-eeprom --run "BOOTFS=/firmware FIRMWARE_RELEASE_STATUS=stable rpi-eeprom-update --apply /tmp/boot_nixos.conf"
    """  # noqa: E501
    )


def _ssh_init_host_key(host: DeployHost, hostname: str) -> None:
    # Copy to nixos system
    host.run(
        """
    install -m400 --target /mnt/etc/ssh -D /etc/ssh/ssh_host_*
    chmod 444 /mnt/etc/ssh/ssh_host_*.pub
    """
    )
    # host.run("chmod 444 /mnt/etc/ssh/ssh_host_*.pub")

    # Generate age key
    host.run(
        """
        nix-shell -p ssh-to-age --command "ssh-to-age -i /mnt/etc/ssh/ssh_host_ed25519_key.pub -o /tmp/ssh-to-age.txt"
    """  # noqa: E501
    )

    # Copy ssh pub to git repository
    info("copy public ssh & age key")
    run(
        f"""
    mkdir -p ./hosts/{hostname}
    scp root@{host.host}:/mnt/etc/ssh/ssh_host_*.pub ./hosts/{hostname}
    scp root@{host.host}:/tmp/ssh-to-age.txt ./hosts/{hostname}
    """  # noqa: E501
    )


def _wireguard_keys(hostname: str) -> None:
    # Private key
    res = run(
        f"""
    mkdir -p ./hosts/{hostname}
    wg genkey
    """,
        hide=True,
    )
    private = res.stdout.strip()

    # pub key
    res = run(
        f"echo '{private}' | wg pubkey > ./hosts/{hostname}/wireguard.pub",
        hide=True,
    )

    info(f"wireguard-priv-key: {private}")


def _execute_nixos_rebuild(
    action: str,
    hostnames: str,
    discovery: bool,
    cache: bool,
    keeperror: bool,
    showtrace: bool,
):
    if hostnames != "":
        # Remote deploy
        deploylist = get_deploylist_from_homelab("root", hostnames)
        _nixos_rebuild(
            deploylist, action, discovery, cache, keeperror, showtrace
        )
    else:
        # Local deploy
        _nix_local_deploy(action, discovery, cache, keeperror, showtrace)


def _execute_home_remote_deploy(
    action: str,
    username: str,
    hostnames: str,
    cache: bool,
    keeperror: bool,
    showtrace: bool,
):
    if hostnames != "":
        # Remote deploy
        deploylist = get_deploylist_from_homelab(username, hostnames)

        _home_remote_deploy(
            username, deploylist, action, cache, keeperror, showtrace
        )
    else:
        # Local deploy
        _home_local_deploy(action, cache, keeperror, showtrace)


def _nixos_generate_config(host: DeployHost, hostname: str) -> None:
    confpath = f"hosts/{hostname}/hardware-configuration.nix"

    os.makedirs(f"hosts/{hostname}", exist_ok=True)
    if not os.path.exists(confpath):
        host.run(
            """
        nixos-generate-config --dir /tmp/hw --root /mnt
        """
        )

        info(f"copy hardware-configuration.nix to {confpath}")
        run(
            f"""
        scp root@{host.host}:/tmp/hw/hardware-configuration.nix {confpath}
        """
        )


# Remove .git (for ignoring dirty message), no git add needed :)
def _sync_homelab(host: DeployHost) -> None:
    run(
        f"rsync --delete {' --exclude '.join([''] + RSYNC_EXCLUDES)} -ar . root@{host.host}:/mnt/nix-homelab/"  # noqa: E501
    )


def _host_hardware_discovery(h: DeployHost) -> None:
    with open("homelab.json", "r") as fr:
        jinfo = json.load(fr)
        hosts = jinfo["hosts"]

        # Create
        hn = h.meta.get("hostname")
        run(f"mkdir -p docs/hosts/{hn}")

        if not os.system(f"ping -c 1 -w 1 {h.host}"):
            if hn and h.meta.get("os") in ["NixOS", "Nix"]:
                h.run(
                    """
                rm -rf /tmp/hw
                mkdir -p /tmp/hw
                """,
                    check=False,
                )

            for dn in OSSCAN[hosts[hn]["os"]]:
                # For non NixOS installation
                # TODO: find beautifull solution (.bash_profile & co)
                PREFIX_COMMAND = "source /etc/bashrc ; LC_ALL=C"
                SSH_OPTS = '-o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no"'  # noqa: E501
                match dn:
                    case "Nix" | "NixOS":
                        h.run(
                            f"{PREFIX_COMMAND} nix-shell -p nix-info --run 'nix-info -m' > /tmp/hw/{dn}.txt"  # noqa: E501
                        )
                        run(
                            f"scp {SSH_OPTS} root@{h.host}:/tmp/hw/{dn}.txt docs/hosts/{hn}/{dn.lower()}.txt"  # noqa: E501
                        )
                    case "Hardwares":
                        h.run(
                            f"{PREFIX_COMMAND} nix-shell -p 'inxi.override {{ withRecommends = true; }}' --run 'sudo inxi -F -a -i --slots -xxx -c0 -i -m --filter' > /tmp/hw/{dn}.txt"  # noqa: E501
                        )
                        run(
                            f"scp {SSH_OPTS} root@{h.host}:/tmp/hw/{dn}.txt docs/hosts/{hn}/{dn.lower()}.txt"  # noqa: E501
                        )
                    case "CPU":
                        h.run(f"{PREFIX_COMMAND} lscpu > /tmp/hw/{dn}.txt")
                        run(
                            f"scp {SSH_OPTS} root@{h.host}:/tmp/hw/{dn}.txt docs/hosts/{hn}/{dn.lower()}.txt"  # noqa: E501
                        )
                    case "Topologie":
                        res = h.run(
                            f"{PREFIX_COMMAND} nix-shell -p hwloc --run 'sudo lstopo -f /tmp/hw/{hn}.lstopo.svg'"  # noqa: E501
                        )
                        run(
                            f"scp {SSH_OPTS} root@{hosts[hn]['ipv4']}:/tmp/hw/{hn}.lstopo.svg docs/hosts/{hn}/{dn.lower()}.svg"  # noqa: E501
                        )
                    case "Scan":
                        res = run(
                            f"{PREFIX_COMMAND} nix-shell -p nmap --run 'sudo nmap --version-intensity 0 -sV {hosts[hn]['ipv4']} -oX -'"  # noqa: E501
                        )

                        # dom = parseString(res.stdout)
                        xpars = xmltodict.parse(res.stdout)
                        try:
                            ports = xpars["nmaprun"]["host"]["ports"]["port"]

                            if isinstance(ports, dict):
                                ports = [ports]

                            # Remove sensible or unimportant values
                            for idx in range(len(ports)):
                                # State
                                if "state" in ports[idx]:
                                    del ports[idx]["state"]

                                # service elements
                                if "service" in ports[idx]:
                                    for value in [
                                        "@version",
                                        "@servicefp",
                                        "@method",
                                        "@conf",
                                        "cpe",
                                    ]:
                                        if value in ports[idx]["service"]:
                                            del ports[idx]["service"][value]

                            jcontent = json.dumps(ports, indent=4)

                            with open(
                                f"docs/hosts/{hn}/{dn.lower()}.json", "w"
                            ) as fw:
                                fw.write(jcontent)
                        except KeyError:
                            pass


def _nixos_rebuild(
    hosts: List[DeployHost],
    action: str,
    discovery: bool,
    cache: bool,
    keeperror: bool,
    showtrace: bool,
) -> None:
    """
    Deploy to all hosts in parallel
    """
    g = DeployGroup(hosts)

    def deploy(h: DeployHost) -> None:
        with open("homelab.json", "r") as f:
            jinfo = json.load(f)
            hosts = jinfo["hosts"]

            # Search host by ip
            hostname = None
            for hn in hosts:
                if "ipv4" in hosts[hn] and hosts[hn]["ipv4"] == h.host:
                    hostname = hn
                    break

        h.run_local(
            f"rsync --delete {' --exclude '.join([''] + RSYNC_EXCLUDES)} -ar . {h.user}@{h.host}:/nix-homelab/"  # noqa: E501
        )

        if hostname:
            cache_opts = ""
            if not cache:
                cache_opts = "--fallback --option binary-caches https://cache.nixos.org/"  # noqa: E501

            keeperror_opts = ""
            if keeperror:
                keeperror_opts = "--option keep-going true"

            showtrace_opts = ""
            if showtrace:
                showtrace_opts = "--show-trace"

            cmd = f"cd /nix-homelab && nixos-rebuild -v {action} {showtrace_opts} {cache_opts} {keeperror_opts} --fast --option accept-flake-config true --flake .#{hostname}"  # noqa: E501
            h.run(cmd)

            if action == "build":
                print("#####################################################")
                print(
                    "# You can see the build result at"
                    f"{h.user}@{h.host}:/nix-homelab/result"
                )
                print("#####################################################")

            if discovery:
                h.meta["hostname"] = hostname
                _host_hardware_discovery(h)

    g.run_function(deploy)


def _home_remote_deploy(
    username: str,
    hosts: List[DeployHost],
    action: str,
    cache: bool,
    keeperror: bool,
    showtrace: bool,
) -> None:
    """
    Deploy to all hosts in parallel
    """
    g = DeployGroup(hosts)

    def deploy(h: DeployHost) -> None:
        with open("homelab.json", "r") as f:
            jinfo = json.load(f)
            hosts = jinfo["hosts"]

            # Search host by ip
            hostname = None
            for hn in hosts:
                if "ipv4" in hosts[hn] and hosts[hn]["ipv4"] == h.host:
                    hostname = hn
                    break

        h.run_local(
            f"rsync --delete {' --exclude '.join([''] + RSYNC_EXCLUDES)} -ar . {h.user}@{h.host}:~/nix-homelab/"  # noqa: E501
        )

        if hostname:
            cache_opts = ""
            if not cache:
                cache_opts = "--fallback --option binary-caches https://cache.nixos.org/"  # noqa: E501

            keeperror_opts = ""
            if keeperror:
                keeperror_opts = "--option keep-going true"

            showtrace_opts = ""
            if showtrace:
                showtrace_opts = "--show-trace"

            # Create missing user profile
            h.run(
                "mkdir -p ~/.local/state/nix/profiles && home-manager init"
            )  # noqa: E501
            # h.run(f"sudo mkdir -p /nix/var/nix/profiles/per-user/{h.user}")
            # h.run(
            #    f"sudo chown {h.user} /nix/var/nix/profiles/per-user/{h.user}"
            # )

            # homemanager deployment
            cmd = f"cd ~/nix-homelab && home-manager -v {action} {showtrace_opts} {cache_opts} {keeperror_opts} --option accept-flake-config true --flake .#{username}@{hostname}"  # noqa: E501
            h.run(cmd)

    g.run_function(deploy)


def _nix_local_deploy(
    action: str, discovery: bool, cache: bool, keeperror: bool, showtrace: bool
) -> None:
    """
    Deploy to on local compute
    """
    run(
        f"rsync --delete {' --exclude '.join([''] + RSYNC_EXCLUDES)} -ar . /nix-homelab/"  # noqa: E501
    )

    cache_opts = ""
    if not cache:
        cache_opts = (
            "--fallback --option binary-caches https://cache.nixos.org/"
        )

    keeperror_opts = ""
    if keeperror:
        keeperror_opts = "--option keep-going true"

    showtrace_opts = ""
    if showtrace:
        showtrace_opts = "--show-trace"

    cmd = f"cd /nix-homelab && sudo nixos-rebuild -v {action} {showtrace_opts} {cache_opts} {keeperror_opts} --fast --option accept-flake-config true --flake .#"  # noqa: E501
    run(cmd)

    if action == "build":
        print("#####################################################")
        print("# You can see the build result at /nix-homelab/result")
        print("#####################################################")


def _home_local_deploy(
    action: str, cache: bool, keeperror: bool, showtrace: bool
) -> None:
    """
    Deploy to on local compute
    """
    run(
        f"rsync --delete {' --exclude '.join([''] + RSYNC_EXCLUDES)} -ar . ~/nix-homelab/"  # noqa: E501
    )

    cache_opts = ""
    if not cache:
        cache_opts = (
            "--fallback --option binary-caches https://cache.nixos.org/"
        )

    keeperror_opts = ""
    if keeperror:
        keeperror_opts = "--option keep-going true"

    showtrace_opts = ""
    if showtrace:
        showtrace_opts = "--show-trace"

    cmd = f"cd ~/nix-homelab && home-manager {action} {showtrace_opts} {cache_opts} {keeperror_opts} --option accept-flake-config true --flake ."  # noqa: E501
    run(cmd)


# def _nix_build(hosts: List[DeployHost], cache: bool, keeperror: bool, showtrace: bool) -> None:  # noqa: E501
#     """
#     Build for all hosts in parallel
#     """
#     g = DeployGroup(hosts)

#     def deploy(h: DeployHost) -> None:
#         with open('homelab.json', 'r') as f:
#             jinfo = json.load(f)
#             hosts = jinfo['hosts']

#             # Search host by ip
#             hostname = None
#             for hn in hosts:
#                 if 'ipv4' in hosts[hn] and  hosts[hn]['ipv4'] == h.host:
#                     hostname = hn
#                     break

#         h.run_local(
#             f"rsync --delete {' --exclude '.join([''] + RSYNC_EXCLUDES)} -ar . {h.user}@{h.host}:/nix-homelab/"  # noqa: E501
#         )

#         if hostname:
#             cache_opts = ""
#             if not cache:
#                 cache_opts = "--fallback --option binary-caches https://cache.nixos.org/"  # noqa: E501

#             keeperror_opts = ""
#             if keeperror:
#                 keeperror_opts = "--option keep-going true"

#             showtrace_opts = ""
#             if showtrace:
#                 showtrace_opts="--show-trace"

#             cmd = f"cd /nix-homelab && nixos-rebuild -v build {showtrace_opts} {cache_opts} {keeperror_opts} --fast --option accept-flake-config true --option keep-going true --flake .#{hostname}"  # noqa: E501
#             h.run(cmd)

#             h.meta['hostname'] = hostname

#     g.run_function(deploy)


def _scan_all_hosts(deploylist: List[DeployHost]) -> None:
    for dh in deploylist:
        _host_hardware_discovery(dh)


def _doc_update_hosts_pages() -> None:
    with open("homelab.json", "r") as fh:
        jinfo = json.load(fh)
        hosts = jinfo["hosts"]

        for hn in hosts:
            # Readme name
            os.makedirs(f"docs/hosts/{hn}", exist_ok=True)
            rname = f"docs/hosts/{hn}.md"

            # Clone template if doc not exists
            if not os.path.exists(rname):
                shutil.copyfile("docs/hosts/host.tpl", rname)

            # Read readme.md content
            with open(rname, "r") as fr:
                content = fr.read().rstrip()

                hinfo = ""
                sinfo = {
                    "memory": "",
                    "disk": "",
                    "kernel": "",
                    "cpu": {
                        "arch": "",
                        "model": "",
                        "nb": "",
                        "bits": 0,
                        "bogomips": 0,
                    },
                }

                for dn in OSSCAN[hosts[hn]["os"]]:
                    output = ""
                    match dn:
                        case "Role":
                            output = taskslib.generateUsedRoles(
                                hostname=hn, rootpath=".."
                            )
                        case "Config":
                            filename = f"docs/hosts/{hn}/cpu.txt"
                            if os.path.exists(filename):
                                output = "```text\n"
                                with open(filename, "r") as fr:
                                    cpu_content = fr.read().strip()

                                    # CPU architecture
                                    m = re.search(
                                        r"Architecture:\s+(.*)",
                                        cpu_content,
                                        flags=re.M,
                                    )
                                    if m:
                                        sinfo["cpu"]["arch"] = m.group(1)
                                        output += f"Arch     : {sinfo['cpu']['arch']}\n"  # noqa: E501

                                    # CPU number
                                    m = re.search(
                                        r"CPU\(s\):\s+([0-9]+)",
                                        cpu_content,
                                        flags=re.M,
                                    )
                                    if m:
                                        sinfo["cpu"]["nb"] = m.group(1)

                                    # CPU model
                                    m = re.search(
                                        r"Model name:\s+(.*)",
                                        cpu_content,
                                        flags=re.M,
                                    )
                                    if m:
                                        sinfo["cpu"]["model"] = m.group(1)
                                        output += f"CPU      : {sinfo['cpu']['nb']} x {sinfo['cpu']['model']}\n"  # noqa: E501

                                    # CPU cores
                                    m = re.search(
                                        r"BogoMIPS:\s+([0-9]+)",
                                        cpu_content,
                                        flags=re.M,
                                    )
                                    if m:
                                        sinfo["cpu"]["bogomips"] = round(
                                            int(m.group(1))
                                        )
                                        output += f"BogoMIPS : {sinfo['cpu']['bogomips']}\n"  # noqa: E501

                            filename = f"docs/hosts/{hn}/hardwares.txt"
                            if os.path.exists(filename):
                                with open(filename, "r") as fr:
                                    hw_content = (
                                        fr.read().strip().replace("\\", "~")
                                    )

                                    # Memory
                                    m = re.search(
                                        r"Memory:.*RAM: total: .*?([0-9]+\.[0-9]+) GiB",  # noqa: E501
                                        hw_content,
                                        flags=re.M,
                                    )
                                    if m:
                                        sinfo[
                                            "memory"
                                        ] = f"{math.floor(float(m.group(1))*1.073741824)} Go"  # noqa: E501
                                        output += f"RAM      : {sinfo['memory']} Go\n"  # noqa: E501

                                    # Disk
                                    m = re.search(
                                        r"Local Storage:.*?total.*?: ([0-9]+\.[0-9]+ \w?iB)",  # noqa: E501
                                        hw_content,
                                        flags=re.M,
                                    )
                                    if m:
                                        sinfo["disk"] = m.group(1)
                                        output += (
                                            f"DISK     : {sinfo['disk']} Go\n"
                                        )

                                    # CPU bits
                                    m = re.search(
                                        r"CPU: .*?bits: (.*?) \w+:",
                                        hw_content,
                                        flags=re.M,
                                    )
                                    if m:
                                        sinfo["cpu"]["bits"] = m.group(1)

                                    # Kernel
                                    m = re.search(
                                        r"System: .*?Kernel: ([0-9]+\.[0-9]+\.[0-9]+)",  # noqa: E501
                                        hw_content,
                                        flags=re.M,
                                    )
                                    if m:
                                        sinfo["kernel"] = m.group(1)
                                        output += (
                                            f"KERNEL   : {sinfo['kernel']}\n"
                                        )

                            if output:
                                output += "```"

                        case "Hardwares":
                            filename = f"docs/hosts/{hn}/{dn.lower()}.txt"
                            if os.path.exists(filename):
                                with open(filename, "r") as fr:
                                    hw_content = (
                                        fr.read().strip().replace("\\", "~")
                                    )

                                    output = f"""```
{hw_content}
```
"""
                        case "Topologie":
                            output = f"""
![hardware topology](https://raw.githubusercontent.com/badele/nix-homelab/master/docs/hosts/{hn}/topologie.svg)
 """  # noqa: E501

                        case "Scan":
                            filename = f"docs/hosts/{hn}/{dn.lower()}.json"

                            if os.path.exists(filename):
                                with open(filename, "r") as fr:
                                    frs = fr.read().strip().replace("\\", "~")
                                    services = json.loads(frs)

                                    output = """| Port | Proto | Service | Product | Extra info |
| ------ | ------ | ------ |------ |------ |
"""  # noqa: E501

                                    for svc in services:
                                        proto = svc["@protocol"]
                                        port = svc["@portid"]

                                        name = svc["service"].get("@name", "")
                                        product = svc["service"].get(
                                            "@product", ""
                                        )
                                        extrainfo = svc["service"].get(
                                            "@extrainfo", ""
                                        )

                                        output += f"|{port}|{proto}|{name}|{product}|{extrainfo}|\n"  # noqa: E501
                                    output += "\n"

                    if output != "":
                        hinfo += f"""
### {dn}

{output}
        """

                with open(f"docs/hosts/{hn}/summaries.json", "w") as fw:
                    fw.write(json.dumps(sinfo, indent=4))

                # Replace content
                newcontent = taskslib._replace_content(
                    content, "HOSTINFOS", hinfo
                )

            # Write new content
            with open(rname, "w") as fw:
                fw.write(newcontent)


##############################################################################
# Menu commands
##############################################################################

ns = Collection()
# ns.add_collection(wg)
ns.add_collection(nixos)
ns.add_collection(home)
ns.add_collection(docs)
ns.add_collection(init)
ns.add_collection(role)
