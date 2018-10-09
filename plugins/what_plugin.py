r"""When a user says "wot" the bot will reply with the previous message in BOLD CAPS.

pattern:  `(?i)^wh?[aou]t\??$`
"""

from telethon import events, sync

# Can't you hear?!
@events.register(events.NewMessage(pattern=r"(?i)^wh?[aou]t\??$"))
async def wut(event):
    if event.is_reply:
        sender = await event.get_sender()
        print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
        repliedmsg = await event.get_reply_message()
        await event.reply(f"**{repliedmsg.raw_text.upper()}**")
    else:
        prev_id = (event.id)-1
        prev_msg = await event.client.get_messages(event.chat_id, ids=prev_id)
        await event.reply(f"**{prev_msg.raw_text.upper()}**")
