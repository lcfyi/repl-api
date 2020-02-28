# REPL API

But not really. 

## VM Deployments

Most containers don't have the necessary kernel features enabled to enable resource sharing enforcements. Thus, we have to manually configure some options. 


Within `/etc/default/grub`, set:
```
GRUB_CMDLINE_LINUX="cgroup_enable=memory cgroup_memory=1 swapaccount=1"
```

Then run `sudo update-grub && sudo reboot`.

### docker-compose

This might be useful for running `docker-compose` without having it installed:
```
echo alias docker-compose="'"'sudo docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:$PWD" \
    -w="$PWD" \
    docker/compose:1.24.0'"'" >> ~/.bashrc

source ~/.bashrc
```
