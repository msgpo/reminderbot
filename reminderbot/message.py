#!/usr/bin/env python

from random import sample

PAYLOAD_TEMPLATE = '''
{greeting}
I've retrieved the latest action items from {source}.

{items}

Something wrong? Not the most recent action items?
Learn how to troubleshoot me on [the wiki](https://sudoroom.org/wiki/Mesh/Reminderbot)!
'''

def make_message(source, items):
    """Produces the final message to be sent to the user."""
    quoted = _quote_items(items)
    return PAYLOAD_TEMPLATE.format(greeting=_random_greeting(),
            source=source,
            items=quoted)

def _quote_items(items):
    return '\n'.join(('> ' + line for line in items.split('\n') if line.strip()))

def _random_greeting():
    """Produces a silly random greeting."""
    template = "{salutation}, {adjective} {first}-{second}!"
    return template.format(salutation=_random_salutation(),
            adjective=_random_adjective(),
            first=_random_first(),
            second=_random_second())

def _random_salutation():
    return sample(["Greetings", "Good morning", "Salutations",
        "Howdy", "Heyo", "Happy Friday"], 1)[0]

def _random_adjective():
    return sample(["dearest", "most excellent", "beloved", "meshy"], 1)[0]

def _random_first():
    return sample(["mesh", "space", "Internet", "web", "community"], 1)[0]

def _random_second():
    return sample(["cadets", "meshers", "stewards", "hackers"], 1)[0]

if __name__ == '__main__':
    for _ in range(10):
        print(_random_greeting())
