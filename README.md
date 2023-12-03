# nix-homelab

This homelab entirelly managed by [NixOS](https://nixos.org/) 

All the configuration is stored on `homelab.json` file, you can do:
- Define network CIDR
- Define hosts
- Define the roles installed for selected hosts
- Define services descriptions
- etc ...

This documentation is generated from `homelab.json` file content 

<img width="100%" src="./docs/nixos.gif" />

## Roles

The main roles used in this home lab

This list generated with `inv docs.all-pages` command

[comment]: (>>ROLES)

<table>
    <tr>
        <th>Logo</th>
        <th>Module</th>
        <th>Hosts</th>
        <th>Description</th>
    </tr><tr>
            <td><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Home_Assistant_Logo.svg/32px-Home_Assistant_Logo.svg.png"></td>
            <td>pi-hole</td>
            <td>pihole</td>
        <td>Pi-hole</td>
        <tr>
            <td><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Home_Assistant_Logo.svg/32px-Home_Assistant_Logo.svg.png"></td>
            <td>ipmi</td>
            <td>microserver-fw, monster-fw</td>
        <td>IPMI</td>
        <tr>
            <td><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Home_Assistant_Logo.svg/32px-Home_Assistant_Logo.svg.png"></td>
            <td>truenas</td>
            <td>microserver</td>
        <td>truenas</td>
        <tr>
            <td><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Home_Assistant_Logo.svg/32px-Home_Assistant_Logo.svg.png"></td>
            <td>nextcloud</td>
            <td>jail1</td>
        <td>NextCloud</td>
        <tr>
            <td><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Home_Assistant_Logo.svg/32px-Home_Assistant_Logo.svg.png"></td>
            <td>syncthing</td>
            <td>jail2</td>
        <td>Syncthing</td>
        <tr>
            <td><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Home_Assistant_Logo.svg/32px-Home_Assistant_Logo.svg.png"></td>
            <td>ssh</td>
            <td>xcp-ng-monster, xcp-ng-vm1, xcp-ng-vm3</td>
        <td>ssh</td>
        <tr>
            <td><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Home_Assistant_Logo.svg/32px-Home_Assistant_Logo.svg.png"></td>
            <td>xcp-ng</td>
            <td>xcp-ng-monster</td>
        <td>XCP-ng</td>
        <tr>
            <td><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Home_Assistant_Logo.svg/32px-Home_Assistant_Logo.svg.png"></td>
            <td>xolite</td>
            <td>xcp-ng-monster</td>
        <td>XCP-ng web-gui</td>
        <tr>
            <td><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Home_Assistant_Logo.svg/32px-Home_Assistant_Logo.svg.png"></td>
            <td>home-assistant</td>
            <td>xcp-ng-vm1, v-puhelin</td>
        <td>Open source home automation [service port 8123]</td>
        <tr>
            <td><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Home_Assistant_Logo.svg/32px-Home_Assistant_Logo.svg.png"></td>
            <td>xoa</td>
            <td>xcp-ng-vm2</td>
        <td>Xen Orchestra Appliance</td>
        <tr>
            <td><img width="32" src="https://dashy.to/img/dashy.png"></td>
            <td>dashy</td>
            <td>xcp-ng-vm3</td>
        <td>The Ultimate Homepage for your Homelab [service port 8081]</td>
        <tr>
            <td><img width="32" src="https://dashy.to/img/dashy.png"></td>
            <td>diyhue</td>
            <td>rpi3</td>
        <td>diyHue</td>
        <tr>
            <td><img width="32" src="https://developer.community.boschrexroth.com/t5/image/serverpage/image-id/13467i19FDFA6E5DC7C260?v=v2"></td>
            <td>mosquitto</td>
            <td>rpi3</td>
        <td>A mqtt broker [service port 1883]</td>
        <tr>
            <td><a href="./docs/zigbee2mqtt.md"><img width="32" src="https://www.zigbee2mqtt.io/logo.png"></a></td>
            <td><a href="./docs/zigbee2mqtt.md">zigbee2mqtt</a></td>
            <td>rpi3</td>
        <td>A zigbee2mqtt [service port 8080]</td>
        <tr>
            <td><img width="32" src="https://www.zigbee2mqtt.io/logo.png"></td>
            <td>zwave-js-ui</td>
            <td>rpi3</td>
        <td>ZWave server</td>
        <tr>
            <td><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Home_Assistant_Logo.svg/32px-Home_Assistant_Logo.svg.png"></td>
            <td>harmony</td>
            <td>harmony, v-puhelin</td>
        <td>Logitech Harmony</td>
        </table>

[comment]: (<<ROLES)

## User programs

<table>
    <tr>
        <th>Logo</th>
        <th>Name</th>
        <th>Description</th>
    </tr><tr>
            <td><a href="https://github.com/badele/nix-homelab"><img width="32" src="https://user-images.githubusercontent.com/28633984/66519056-2e840c80-eaef-11e9-8670-c767213c26ba.png"></a></td>
            <td>Neovim</td>
            <td>Moved to <a href="https://github.com/badele/vide">badele/vide</td>
</table>



## Hosts

List of hosts composing the home lab

This list generated with `inv docs.all-pages` command

[comment]: (>>HOSTS)

<table>
    <tr>
        <th>Logo</th>
        <th>Name</th>
        <th>OS</th>
        <th>Description</th>
    </tr><tr>
            <td><a href="./docs/hosts/box.md"><img width="32" src="https://logos-marques.com/wp-content/uploads/2022/03/SFR-Logo-1994.png"></a></td>
            <td><a href="./docs/hosts/box.md">box</a>&nbsp;(192.168.0.1)</td>
            <td>Sagem</td>
            <td>SFR internet box</td>
        </tr><tr>
            <td><a href="./docs/hosts/router-living.md"><img width="32" src="https://cdn.shopify.com/s/files/1/0653/8759/3953/files/512.png?v=1657867177&width=32"></a></td>
            <td><a href="./docs/hosts/router-living.md">router-living</a>&nbsp;(192.168.254.254)</td>
            <td>MikroTik</td>
            <td>Livingroom home mikrotik router</td>
        </tr><tr>
            <td><a href="./docs/hosts/router-bedroom.md"><img width="32" src="https://cdn.shopify.com/s/files/1/0653/8759/3953/files/512.png?v=1657867177&width=32"></a></td>
            <td><a href="./docs/hosts/router-bedroom.md">router-bedroom</a>&nbsp;(192.168.254.253)</td>
            <td>MikroTik</td>
            <td>Bedroom home mikrotik router</td>
        </tr><tr>
            <td><a href="./docs/hosts/router-homeoffice.md"><img width="32" src="https://cdn.shopify.com/s/files/1/0653/8759/3953/files/512.png?v=1657867177&width=32"></a></td>
            <td><a href="./docs/hosts/router-homeoffice.md">router-homeoffice</a>&nbsp;(192.168.254.252)</td>
            <td>MikroTik</td>
            <td>Office home mikrotik router</td>
        </tr><tr>
            <td><a href="./docs/hosts/sam.md"><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Xfce_logo-footprint.svg/32px-Xfce_logo-footprint.svg.png"></a></td>
            <td><a href="./docs/hosts/sam.md">sam</a>&nbsp;(192.168.0.18)</td>
            <td>NixOS</td>
            <td>Samsung N110 Latop</td>
        </tr><tr>
            <td><a href="./docs/hosts/latino.md"><img width="32" src="https://styles.redditmedia.com/t5_6sciw0/styles/communityIcon_h3cvittvupi91.png"></a></td>
            <td><a href="./docs/hosts/latino.md">latino</a>&nbsp;(192.168.254.200)</td>
            <td>NixOS</td>
            <td>Dell Latitude E5540 Latop</td>
        </tr><tr>
            <td><a href="./docs/hosts/rpi40.md"><img width="32" src="https://upload.wikimedia.org/wikipedia/fr/thumb/3/3b/Raspberry_Pi_logo.svg/32px-Raspberry_Pi_logo.svg.png"></a></td>
            <td><a href="./docs/hosts/rpi40.md">rpi40</a>&nbsp;(192.168.254.101)</td>
            <td>NixOS</td>
            <td>The Raspberry PI 4 storage server</td>
        </tr><tr>
            <td><a href="./docs/hosts/bootstore.md"><img width="32" src="https://simpleicons.org/icons/databricks.svg"></a></td>
            <td><a href="./docs/hosts/bootstore.md">bootstore</a>&nbsp;(192.168.254.100)</td>
            <td>NixOS</td>
            <td>HP Proliant Microserver N40L storage server</td>
        </tr><tr>
            <td><a href="./docs/hosts/badwork.md"><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/IBM_ThinkPad_logo_askew_badge.svg/32px-IBM_ThinkPad_logo_askew_badge.svg.png"></a></td>
            <td><a href="./docs/hosts/badwork.md">badwork</a>&nbsp;(192.168.254.189)</td>
            <td>Nix</td>
            <td>A work thinkpad</td>
        </tr><tr>
            <td><a href="./docs/hosts/badwork-eth.md"><img width="32" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/IBM_ThinkPad_logo_askew_badge.svg/32px-IBM_ThinkPad_logo_askew_badge.svg.png"></a></td>
            <td><a href="./docs/hosts/badwork-eth.md">badwork-eth</a>&nbsp;(192.168.254.102)</td>
            <td>Nix</td>
            <td>A ethernet work thinkpad</td>
        </tr><tr>
            <td><a href="./docs/hosts/badphone.md"><img width="32" src="https://cdn-icons-png.flaticon.com/512/38/38002.png"></a></td>
            <td><a href="./docs/hosts/badphone.md">badphone</a>&nbsp;(192.168.254.194)</td>
            <td>Android</td>
            <td>Bruno's phone</td>
        </tr><tr>
            <td><a href="./docs/hosts/ladphone.md"><img width="32" src="https://cdn-icons-png.flaticon.com/512/38/38002.png"></a></td>
            <td><a href="./docs/hosts/ladphone.md">ladphone</a>&nbsp;(192.168.254.184)</td>
            <td>Android</td>
            <td>Lucas's phone</td>
        </tr><tr>
            <td><a href="./docs/hosts/sadphone.md"><img width="32" src="https://cdn-icons-png.flaticon.com/512/38/38002.png"></a></td>
            <td><a href="./docs/hosts/sadphone.md">sadphone</a>&nbsp;(192.168.254.188)</td>
            <td>Android</td>
            <td>Steph's phone</td>
        </tr><tr>
            <td><a href="./docs/hosts/loadphone.md"><img width="32" src="https://img.freepik.com/icones-gratuites/pomme_318-162866.jpg"></a></td>
            <td><a href="./docs/hosts/loadphone.md">loadphone</a>&nbsp;(192.168.254.199)</td>
            <td>Iphone</td>
            <td>Lou's phone</td>
        </tr><tr>
            <td><a href="./docs/hosts/tv-chromecast.md"><img width="32" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrW-wZZhmKpadJqRe73njFwEDLzh-jIn1XaSbCVhgMmoN46pgj6M4Fq1tWyr5w_z_HcP4&usqp=CAU"></a></td>
            <td><a href="./docs/hosts/tv-chromecast.md">tv-chromecast</a>&nbsp;(192.168.254.105)</td>
            <td>Chromecast</td>
            <td>TV Chromecast</td>
        </tr><tr>
            <td><a href="./docs/hosts/bedroom-googlemini-A.md"><img width="32" src="https://c.clc2l.com/t/g/o/google-home-wxDa7w.png"></a></td>
            <td><a href="./docs/hosts/bedroom-googlemini-A.md">bedroom-googlemini-A</a>&nbsp;(192.168.254.197)</td>
            <td>GoogleMini</td>
            <td>Google Mini room A</td>
        </tr><tr>
            <td><a href="./docs/hosts/bedroom-googlemini-C.md"><img width="32" src="https://c.clc2l.com/t/g/o/google-home-wxDa7w.png"></a></td>
            <td><a href="./docs/hosts/bedroom-googlemini-C.md">bedroom-googlemini-C</a>&nbsp;(192.168.254.196)</td>
            <td>GoogleMini</td>
            <td>Google Mini room C</td>
        </tr><tr>
            <td><a href="./docs/hosts/badxps.md"><img width="32" src="https://ih1.redbubble.net/image.201056839.4943/flat,32x32,075,t.jpg"></a></td>
            <td><a href="./docs/hosts/badxps.md">badxps</a>&nbsp;(192.168.254.114)</td>
            <td>NixOS</td>
            <td>Dell XPS 9570 Latop</td>
        </tr><tr>
            <td><a href="./docs/hosts/bridge-hue.md"><img width="32" src="https://www.daskeyboard.com/images/applets/philips-hue/icon.png"></a></td>
            <td><a href="./docs/hosts/bridge-hue.md">bridge-hue</a>&nbsp;(192.168.254.191)</td>
            <td>Bridge</td>
            <td>Philips Hue bridge</td>
        </tr><tr>
            <td><a href="./docs/hosts/sadhome.md"><img width="32" src="https://cdn.icon-icons.com/icons2/2699/PNG/512/archlinux_logo_icon_167835.png"></a></td>
            <td><a href="./docs/hosts/sadhome.md">sadhome</a>&nbsp;(192.168.254.185)</td>
            <td>ArchLinux</td>
            <td>Stephanie's laptop</td>
        </tr></table>

[comment]: (<<HOSTS)

## Network

[comment]: (>>NETWORK)

```mermaid
 graph BT
 linkStyle default interpolate basis
 internet((Internet))

 arris[<center>Kaapelimodeemi</br>10.0.0.1</center>] --- internet
kytkin-varasto[<center>Varaston HP 1810-8G kytkin</br>10.0.0.2</center>] --- arris
kytkin-olohuone[<center>Olohuoneen HP 1810-8G kytkin</br>10.0.0.3</center>] --- kytkin-varasto
pihole[<center>Raspberry Pi 4 Pi-hole</br>10.0.1.1</center>] --- arris
microserver-fw[<center>HP Microserver Gen8 iLO4</br>10.0.2.1</center>] --- kytkin-varasto
microserver[<center>HP Microserver Gen8 TrueNAS</br>10.0.2.2</center>] --- kytkin-varasto
jail1[<center>TrueNAS NextCloud jail</br>10.0.2.3</center>] --- microserver
jail2[<center>TrueNAS Syncthing jail</br>10.0.2.4</center>] --- microserver
monster-fw[<center>32-core monster IPMI</br>10.0.3.1</center>] --- kytkin-varasto
xcp-ng-monster[<center>32-core monster XCP-ng host</br>10.0.3.2</center>] --- kytkin-varasto
xcp-ng-vm1[<center>Home Assistant OS VM</br>10.0.2.5</center>] --- xcp-ng-monster
xcp-ng-vm2[<center>XOA VM</br>10.0.3.3</center>] --- xcp-ng-monster
xcp-ng-vm3[<center>Small services NixOS VM</br>10.0.3.4</center>] --- xcp-ng-monster
rpi3[<center>RPI3: zigbee, zwave, hue, mqtt</br>10.0.4.1</center>] --- kytkin-varasto
harmony[<center>Logitech Harmony Hub</br>10.0.10.1</center>] --- aruba-ap15
macbook-g-wifi[<center>Work macbook</br>10.0.100.4</center>] --- aruba-ap15
v-puhelin[<center>V puhelin</br>10.0.100.5</center>] --- aruba-ap15

subgraph office
arris
pihole
macbook-g-wifi
end

subgraph varasto
kytkin-varasto
end

subgraph olohuone
kytkin-olohuone
harmony
end

subgraph nas
microserver-fw
microserver
jail1
jail2
end

subgraph monster
monster-fw
xcp-ng-monster
xcp-ng-vm1
xcp-ng-vm2
xcp-ng-vm3
end

subgraph homeoffice
rpi3
end

```

[comment]: (<<NETWORK)

## Structure

- **Configuration**
    - `homelab.json`: main homelab file configuration (roles servers, network, etc)
    - `hosts`: hosts configuration (system, hardware, host secrets)
        - `*.nix`: user accounts
    - `users`: users configuration (on user environment, user secrets)
- **System**
    - `nix`: all ***.nix** files
        - `home-manager`: All users ***.nix** files (installed on user environment)
        - `modules`: all nix modules
            - `home-manager`: user modules
            - `nixos`: nixos modules (installed on system wide)
                - `host.nix`: host options (custom options for host)
      - `nixos`: all ***.nix** files installed on system wide
      - `overlays`: overlays **nix derivations**
      - `pkgs`: custom nix packages

## Homelab initialisation
```
inv init.domain-cert
```

## NixOS installation & update

See [Commons installation](docs//installation.md)


### Update from you local computer/laptop

```
# Local installation
inv nixos.[build|test|deploy]
inv home.[build|test|deploy]

# Remote installation
inv nixos.[build|test|deploy] --hostnames <hostname>,<hostname>,...
inv home.[build|test|deploy] --username <username> --hostnames <hostname>,<hostname>,...
```

## Update roles or multiple hosts

```
# Simulate deployment(build)
inv role.build --role <rolename>
inv nixos.build --hosts <hostname>,<hostname>

# Install
inv role.deploy --role <rolename>
inv nixos.deploy --hosts <hostname>,<hostname>
```



## Commands

Home lab commands list

This list generated with `inv docs.all-pages` command

[comment]: (>>COMMANDS)

```
Available tasks:

  docs.all-pages               generate all homelab documentation
  docs.host-pages              generate all homelab hosts page
  docs.main-page               generate main homelab page
  docs.scan-all-hosts          Retrieve all hosts system infromations
  home.build                   Test to <hostnames> server
  home.deploy                  Deploy to <hostnames> server
  init.disk-format             Format disks with zfs
  init.disk-mount              Mount disks from the installer
  init.domain-cert             Init domain certificate
  init.nix-serve               Init nix binary cache server <hostname> nix-
                               serve private & public key
  init.nixos-generate-config   Generate hardware configuration for the host
  init.nixos-install           install nixos
  init.ssh-init-host-key       Init ssh host key from nixos installation
  nixos.boot                   rebuild boot to <hostnames> server
  nixos.build                  Test to <hostnames> server
  nixos.deploy                 Deploy to <hostnames> server
  nixos.test                   Test to <hostnames> server
  role.build                   Build for all hosts contains the role
  role.deploy                  Deploy for all hosts contains the role
  role.test                    Test for all hosts contains the role


```


[comment]: (<<COMMANDS)


# A big thanks ❤️

A big thank to the contributors of OpenSource projects in particular :
- [doctor-cluster-config](https://github.com/TUM-DSE/doctor-cluster-config) from German TUM School of Computation
- [Mic92](https://github.com/Mic92/dotfiles) and for his some nix contributions
- [Misterio77](https://github.com/Misterio77/nix-config) and for his some nix contributions
- [longerHV](https://github.com/LongerHV/nixos-configuration) nix configuration file