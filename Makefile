package:
	rm -f reminderbot.tgz
	tar czf reminderbot.tgz main.py reminderbot webhook.txt \
		requirements.txt crontab.txt
