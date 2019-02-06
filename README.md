# ReminderBot
ReminderBot scrapes sudoroom.org for sudo mesh action items,
then sends the list to peoplesopen.net/chat.

Intended for Ubuntu 18.04. Assumes Python 3.6 available (feel free to make this part less brittle.)

## Setup
`webhook.txt` is git-ignored.
You'll need to create the file, and it should contain exactly one line - the URL of the Rocketchat webhook.

```bash
make package
scp reminderbot.tgz root@wherever:/root/
ssh root@wherever 'bash -s' < bootstrap.sh
```
