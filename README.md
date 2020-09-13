# REPL API

This is a simple API that you can spin up to run snippets of code. It currently supports C, C++, Java, JavaScript, and Python, but additional languages should be relatively simple to support.

## `GET /run`

Heartbeat for server status.

## `POST /run`

Invoke this with a JSON payload that contains a `language` and `code`, where the former is one of `javascript`, `java`, `python`, `c`, `cpp` and `code` is the code itself.

So for example:

```bash
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"language": "python", "code": "print(1)"}' \
    <host>/run
```

## AWS/GCP Deployments

Most VMs don't have the necessary kernel features enabled to enable resource sharing enforcements. Thus, we have to manually configure some options.

Within `/etc/default/grub`, set:

```
GRUB_CMDLINE_LINUX="cgroup_enable=memory cgroup_memory=1 swapaccount=1"
```

Then run `sudo update-grub && sudo reboot`.

### docker-compose

This could be useful for running `docker-compose` without having it installed:

```
echo alias docker-compose="'"'sudo docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:$PWD" \
    -w="$PWD" \
    docker/compose:1.24.0'"'" >> ~/.bashrc

source ~/.bashrc
```

### Swap

Enable swap to eek out a bit more life from the free-tier VMs:

```
# Confirm you have no swap
sudo swapon -s

# Allocate 1GB (or more if you wish) in /swapfile
sudo fallocate -l 1G /swapfile

# Make it secure
sudo chmod 600 /swapfile
ls -lh /swapfile

# Activate it
sudo mkswap /swapfile
sudo swapon /swapfile

# Confirm again there's indeed more memory now
free -m
sudo swapon -s

# Configure fstab to use swap when instance restart
sudo vim /etc/fstab

# Add this line to /etc/fstab, save and exit
/swapfile   none    swap    sw    0   0

# Change swappiness to 20, so that swap is used only when 20% RAM is unused
# The default is too high at 60
echo 20 | sudo tee /proc/sys/vm/swappiness
echo vm.swappiness = 20 | sudo tee -a /etc/sysctl.conf
```
