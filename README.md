# Webex-bot
A bot publishing messages on a dedicated [Webex](https://developer.webex.com/) room<br/>

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
 
### Pre-requisites
Webex bots help users automate tasks and bring external content into the discussion. More info on [Bots](https://developer.webex.com/docs/bots)<br/>

### Setup and first run
1. Clone the repository and create a virtual environment
```
$ git clone https://github.com/carmelo0x99/wxbot.git

$ cd wxbot/

$ python3 -m venv .

$ source bin/activate

(wxbot) $ python3 -m pip install --upgrade pip setuptools wheel

(wxbot) $ python3 -m pip install requests
```

2. Configure your own setup with the appropriate bot name, token and chat ID. The configuration file, `wxbot.json`, looks like this
```
{"BEARER": "<long string>", "ROOM_ID": "<long string>"}
```

3. Check
A quick run of the main script would do:
```
$ ./wxbot.py
```
If everything has been setup correctly, a message should appear in the room.</br>

### Build Docker container
This part is optional but no README would be complete without the containerization section:
```
$ docker build -t <repository>/<image>:<tag> .

$ docker push <repository>/<image>:<tag>

$ docker run \
    --detach \
    --rm \
    --volume /var/log:/var/log:ro \
    --volume -v $PWD:/usr/local/bin \
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

