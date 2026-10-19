import time

def process(message_id, seen, effects, before_effect=lambda: None):
    if message_id in seen:
        return "duplicate"
    before_effect()
    effects.append(message_id)
    seen.add(message_id)
    return "processed"
