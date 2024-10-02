# Webex bot
A bot publishing messages on a dedicated [Webex](https://developer.webex.com/) room.<br/>
Webex bots help users automate tasks and bring external content into the discussion. More info on [Bots](https://developer.webex.com/docs/bots) and how to create one.<br/>
This is just a PoC but already usable. The script, written in Python, contained in this repository is supposed to run on your own personal server (a Raspberry pi, a cloud VM, a physical server...). It checks, at configurable intervals, the messages in `auth.log` for contents such as `Invalid user <attacker> from <ip_address> port <port_number>`.<br/>
If any such messages exist, a notification will be published on the Webex room by the bot.<br/>

### Secure your system
You thought you'd get away without the necessary lecture?!?</br>
Security is an active exercise, you need to:
1. assess your threat landscape
2. generate your custom policy
3. apply it
4. make sure it is constantly applied/monitor

Regarding `#2` above, you may want to read a guide:
1. [How To Harden OpenSSH on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-harden-openssh-on-ubuntu-20-04): just an example, the article focuses on Ubuntu but it is applicable to other distros with minor, if any, modifications
2. install [Fail2Ban](https://www.fail2ban.org/)

OK, now you're good to go and read the rest :)

### Setup and first run
1. Clone the repository and create a virtual environment
```
$ git clone https://github.com/carmelo0x99/Webex-bot.git

$ cd Webex-bot/

$ python3 -m venv .

$ source bin/activate

(Webex-bot) $ python3 -m pip install --upgrade pip setuptools wheel

(Webex-bot) $ python3 -m pip install requests
```

2. Configure your own setup with the appropriate credentials: the bearer token and room identifier you've received when first creating the bot.<br/>
The configuration file, `wxbot.json`, should look like this
```
{"BEARER": "<long string>", "ROOM_ID": "<long string>"}
```

3. Check
A quick run of the main script would do:
```
$ ./wxbot.py
```
If everything has been setup correctly, a local log file (`wxbot.log`) will be created. A message should appear in the room only if `auth.log` contains the expected messages.</br>

### Build Docker container
This part is optional but no README would be complete without the containerization section:
```
$ docker build -t <repository>/<image>:<tag> .

$ docker push <repository>/<image>:<tag>

$ docker run \
    --detach \
    --rm \
    --volume /var/log:/var/log:ro \
    --volume $PWD:/usr/local/bin \
    <repository>/<image>:<tag>
```

### Run through crontab
At minute `59` every hour:
```
59 * * * *  (cd /path/to/wxbot; /usr/bin/docker run -d --rm -v /var/log:/var/log:ro -v $PWD:/usr/local/bin <repository>/<image>:<tag>)
```

### What to do when alerts are being received
First and foremost, [DON'T PANIC](https://en.wikipedia.org/wiki/Phrases_from_The_Hitchhiker%27s_Guide_to_the_Galaxy)!!!</br>
If you've secured your system (you have, right?), chances are that any attacks have been unsuccessful.</br>
It won't hurt though to log into your system and:
1. check the logs
2. run a scan with [Lynis](https://cisofy.com/lynis/) or [chkrootkit](http://www.chkrootkit.org) for instance
3. verify that your security policies are still applied
4. just for fun, check where the attackers came from

