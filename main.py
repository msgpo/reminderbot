#!/usr/bin/env python3

from reminderbot.bot import main, abort

if __name__ == '__main__':
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description='Figure out what needs doing.')
    parser.add_argument('--webhook-path',
            type=lambda p: Path(p).absolute(),
            default=Path(__file__).absolute().parent / "webhook.txt",
            help='path to file containing webhook URL')

    p = parser.parse_args()
    try:
        with open(p.webhook_path, 'r') as f:
            webhook_url = f.read()
    except FileNotFoundError as e:
        abort("Couldn't find webhook URL: {}".format(e))
    except Exception as e:
        abort("Couldn't read webhook URL: {}".format(e))
    print(webhook_url)
    main(webhook_url)
