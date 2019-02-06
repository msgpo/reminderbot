package:
	rm -f reminderbot.tgz
	tar czf reminderbot.tgz main.py reminderbot webhook.txt \
		reminderbot.timer reminderbot.service \
		Pipfile Pipfile.lock crontab.txt
