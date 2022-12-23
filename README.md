[ ] Filtrer le contenu json des nmap
[ ] Utiliser les fonctions python au lieu d'utiliser run()

# nix-homelab
NixOS homelab

## Hosts

This page generated by `inv doc-generate`

[comment]: (>>HOSTS)

<table>
    <tr>
        <th>Logo</th>
        <th>Name</th>
        <th>Arch</th>
        <th>OS</th>
        <th>CPU</th>
        <th>Memory</th>
        <th>Disk</th>
        <th>Description</th>
    </tr><tr>
        <td><a href="./docs/hosts/box.md"><img width="32" src="https://logos-marques.com/wp-content/uploads/2022/03/SFR-Logo-1994.png"></a></td>
        <td><a href="./docs/hosts/box.md">box</a>&nbsp;(192.168.0.1)</td>
        <td></td>
        <td>Sagem</td>
        <td></td>
        <td></td>
        <td></td>
        <td>SFR internet box</td>
    </tr><tr>
        <td><a href="./docs/hosts/router-ext.md"><img width="32" src="https://cdn.shopify.com/s/files/1/0653/8759/3953/files/512.png?v=1657867177&width=32"></a></td>
        <td><a href="./docs/hosts/router-ext.md">router-ext</a>&nbsp;(192.168.0.10)</td>
        <td></td>
        <td>RouterOS</td>
        <td></td>
        <td></td>
        <td></td>
        <td>External home mikrotik router</td>
    </tr><tr>
        <td><a href="./docs/hosts/router-int.md"><img width="32" src="https://cdn.shopify.com/s/files/1/0653/8759/3953/files/512.png?v=1657867177&width=32"></a></td>
        <td><a href="./docs/hosts/router-int.md">router-int</a>&nbsp;(192.168.254.254)</td>
        <td></td>
        <td>RouterOS</td>
        <td></td>
        <td></td>
        <td></td>
        <td>Internal home mikrotik router</td>
    </tr><tr>
        <td><a href="./docs/hosts/sam.md"><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Xfce_logo-footprint.svg/32px-Xfce_logo-footprint.svg.png"></a></td>
        <td><a href="./docs/hosts/sam.md">sam</a>&nbsp;(192.168.0.18)</td>
        <td></td>
        <td>NixOs</td>
        <td></td>
        <td></td>
        <td></td>
        <td>Samsung N110 Latop</td>
    </tr><tr>
        <td><a href="./docs/hosts/latino.md"><img width="32" src="https://styles.redditmedia.com/t5_6sciw0/styles/communityIcon_h3cvittvupi91.png"></a></td>
        <td><a href="./docs/hosts/latino.md">latino</a>&nbsp;(192.168.254.152)</td>
        <td>x86_64</td>
        <td>NixOs</td>
        <td>4</td>
        <td>8 Go</td>
        <td>465.76 GiB</td>
        <td>Dell Latitude E5540 Latop</td>
    </tr><tr>
        <td><a href="./docs/hosts/rpi40.md"><img width="32" src="https://upload.wikimedia.org/wikipedia/fr/thumb/3/3b/Raspberry_Pi_logo.svg/32px-Raspberry_Pi_logo.svg.png"></a></td>
        <td><a href="./docs/hosts/rpi40.md">rpi40</a>&nbsp;(192.168.0.17)</td>
        <td>aarch64</td>
        <td>NixOs</td>
        <td>4</td>
        <td>8 Go</td>
        <td>495.48 GiB</td>
        <td>The Raspberry PI 4 storage server</td>
    </tr><tr>
        <td><a href="./docs/hosts/bootstore.md"><img width="32" src="https://simpleicons.org/icons/databricks.svg"></a></td>
        <td><a href="./docs/hosts/bootstore.md">bootstore</a>&nbsp;(192.168.0.29)</td>
        <td>x86_64</td>
        <td>NixOs</td>
        <td>2</td>
        <td>8 Go</td>
        <td>3.64 TiB</td>
        <td>HP Proliant Microserver N40L storage server</td>
    </tr><tr>
        <td><a href="./docs/hosts/badwork.md"><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/IBM_ThinkPad_logo_askew_badge.svg/32px-IBM_ThinkPad_logo_askew_badge.svg.png"></a></td>
        <td><a href="./docs/hosts/badwork.md">badwork</a>&nbsp;(192.168.254.177)</td>
        <td>x86_64</td>
        <td>Nix</td>
        <td>12</td>
        <td>32 Go</td>
        <td></td>
        <td>A work thinkpad</td>
    </tr></table>

[comment]: (<<HOSTS)

## Commons scratch installation

Boot from NixOS live cd

```
##########################################################
# NixOS installation configuration
##########################################################

# Change keymap & root password
sudo -i
loadkeys fr
passwd 

# From other computer, enter to deploy environment
# NOTE: Use <SPACE> before command for not storing command in bash history (for secure your passwords)
nix develop
export TARGETIP=<hostip>
export TARGETNAME=<hostname>

ssh-copy-id root@${TARGETIP}
 inv disk-format --hosts ${TARGETIP} --disk /dev/sda --mirror /dev/sdb --mode MBR
 [Optional] inv disk-mount --hosts ${TARGETIP} --mirror true --password "<zfspassword>"
inv ssh-init-host-key --hosts ${TARGETIP} --hostnames ${TARGETNAME}
inv nixos-generate-config --hosts ${TARGETIP} --hostnames ${TARGETNAME} --name hp-proliant-microserver-n40l

# Add hosts/bootstore/ssh-to-age.txt content to .sops.yaml
# Add root password key to ./hosts/bootstore/secrets.yml 
echo 'yourpassword' | mkpasswd -m sha-512 -s

# Re-encrypt all keys for the previous host
sops updatekeys ./hosts/${TARGETNAME}/secrets.yml

####################################################
# Execute your custom task here, exemple:
# - Restore persist borgbackup
# - Configure some program (private key generation)
####################################################

# Add hostname in configurations.nix with minimalModules
# Configure hosts/<hostname>/default.nix

# NixOS installation
inv nixos-install --hosts ${TARGETIP} --flakeattr ${TARGETNAME}
```

## Update nixos

```
inv deploy --hosts bootstore
```


## Folders

[comment]: (>>FOLDERS)

```
.
├── configurations.nix
├── docs
│   └── hosts
│       ├── badwork
│       │   ├── cpu.txt
│       │   ├── hardwares.txt
│       │   ├── nix.txt
│       │   ├── summaries.json
│       │   └── topologie.svg
│       ├── badwork.md
│       ├── bootstore
│       │   ├── cpu.txt
│       │   ├── hardwares.txt
│       │   ├── nix.txt
│       │   ├── services.json
│       │   ├── summaries.json
│       │   └── topologie.svg
│       ├── bootstore.md
│       ├── box
│       │   ├── services.json
│       │   └── summaries.json
│       ├── box.md
│       ├── host.tpl
│       ├── latino
│       │   ├── cpu.txt
│       │   ├── hardwares.txt
│       │   ├── nix.txt
│       ��   ├── services.json
│       │   ├── summaries.json
│       │   └── topologie.svg
│       ├── latino.md
│       ├── router-ext
│       │   ├── services.json
│       │   └── summaries.json
│       ├── router-ext.md
│       ├── router-int
│       │   ├── services.json
│       │   └── summaries.json
│       ├── router-int.md
│       ├── rpi40
│       │   ├── cpu.txt
│       │   ├── hardwares.txt
│       │   ├── nix.txt
│       │   ├── services.json
│       │   ├── summaries.json
│       │   └── topologie.svg
│       ├── rpi40.md
│       ├── sam
│       │   └── summaries.json
│       └── sam.md
├── flake.lock
├── flake.nix
├── homelab.json
├── hosts
│   ├── bootstore
│   │   ├── default.nix
│   │   ├── secrets.yml
│   │   ├── ssh_host_ed25519_key.pub
│   │   ├── ssh_host_rsa_key.pub
│   │   └── ssh-to-age.txt
│   ├── rpi40
│   │   ├── default.nix
│   │   ├── secrets.yml
│   │   ├── ssh_host_ed25519_key.pub
│   │   ├── ssh_host_rsa_key.pub
│   │   └── ssh-to-age.txt
│   ├── sam
│   │   ├── default.nix
│   │   ├── secrets.yml
│   │   ├── ssh_host_ed25519_key.pub
│   │   ├── ssh_host_rsa_key.pub
│   │   └── ssh-to-age.txt
│   └── secrets.yml
├── LICENSE
├── modules
│   ├── hardware
│   │   ├── hp-proliant-microserver-n40l.nix
│   │   ├── rpi4-usb-boot.nix
│   │   └── samsung-n210.nix
│   ├── system
│   │   ├── hosts.nix
│   │   ├── networking.nix
│   │   ├── nfs
│   │   │   └── server.nix
│   │   ├── nix.nix
│   │   ├── nix-serve.nix
│   │   ├── sshd.nix
│   │   └── zfs.nix
│   └── users.nix
├── README.md
├── tasks.py
└── vscode.code-workspace

```


[comment]: (<<FOLDERS)


# A big thanks ❤️

A big thank to the contributors of OpenSource projects in particular :
- [doctor-cluster-config](https://github.com/TUM-DSE/doctor-cluster-config) from German TUM School of Computation
- [Mic92](https://github.com/Mic92/dotfiles) and for his some nix contributions
- [Misterio77](https://github.com/Misterio77/nix-config) and for his some nix contributions