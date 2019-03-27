package:
	rm -f reminderbot.tgz
	tar czf reminderbot.tgz main.py reminderbot webhook.txt \
		requirements.txt crontab.txt

USER = root
IP = 206.189.68.109
DEST = /opt/reminderbot

# deploys main.py and reminderbot/ to the server
# TODO: update crontab and install python deps
deploy:
	rsync -av main.py ${USER}@${IP}:${DEST}
	ssh ${USER}@${IP} chown reminderbot ${DEST}/main.py
	rsync -av reminderbot ${USER}@${IP}:${DEST}
	ssh ${USER}@${IP} chown -R reminderbot ${DEST}/reminderbot
