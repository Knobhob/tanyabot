"""Dice roll

Will roll a __x__ sided dice __n__ times.
Examples:
• `/roll 3d20`
• `/roll d6 2d7 3d8` (between 1 and 20 dice)

pattern: `/roll@bot_username? ((?:\d*d\d+\s*)+)$`
"""

import re
from random import randint
from .global_functions import log
from telethon import client, events, errors


@events.register(events.NewMessage(pattern=r"/roll(@\w+)?\s+((?:\d*d\d+\s*)+)$"))
async def on_roll(event):
    m = event.pattern_match

    usr_group = m.group(1)
    username = (await event.client.get_me()).username
    if usr_group and username not in usr_group:
        return


    dice_pattern = r"(\d*)d(\d+)"
    dice_match = re.finditer(dice_pattern, m.group(2))

    outputs = list()
    total = int()
    output_strings = list()

    roll_limit = 0
    for d in dice_match:
        if roll_limit == 20:
            break

        if not d.group(1):
            rolls = 1
        else:
            rolls = int(d.group(1))

        sides = int(d.group(2))

        if rolls > 500 or sides > 100000:
            await event.respond("The maximum rolls is 500, and the maximum amount of sides is 100,000.")
            await log(event, info="Bad roll")
            return

        output_strings.append(f"**{rolls}d{sides}:**")

        val = list()
        for _ in range(0, rolls):
            r = randint(1, sides)
            val.append(str(r))
            total += r

        outputs.append(" ".join(val))
        output_strings.append(f"`{' '.join(val)}`")
        roll_limit += 1

    if len(outputs) > 1:
        output_strings.append(f"**=** `{total}`")

    output = "\n".join(output_strings)

    await log(event)    # Logs the event
    try:
        await event.respond(f"{output}")
    except errors.MessageTooLongError:
        await event.respond(f"**Total =** `{total}`\n"
                            + "Tip:  Message was too long, try rolling less dice next time")
