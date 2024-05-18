import time
from datetime import timedelta
from pyrogram.errors import FloodWait

class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

def hrb(value, digits=2, delim="", postfix=""):
    """Return a human-readable file size."""
    if value is None:
        return None
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024:
            break
        value /= 1024
    return f"{value:.{digits}f}{delim}{unit}{postfix}"

def hrt(seconds, precision=0):
    """Return a human-readable time delta as a string."""
    periods = [
        ('d', 86400),  # 60 * 60 * 24
        ('h', 3600),   # 60 * 60
        ('m', 60),
        ('s', 1),
    ]

    time_str = []
    for period, period_seconds in periods:
        if seconds >= period_seconds or (period == 's' and not time_str):
            period_value, seconds = divmod(seconds, period_seconds)
            time_str.append(f"{period_value}{period}")

    if precision > 0:
        time_str = time_str[:precision]

    return ''.join(time_str)

def create_custom_bar(current, total):
    progress_chars = list("KUNAL")
    progress_length = len(progress_chars)
    progress = int((current / total) * progress_length)
    
    bar = ""
    for i in range(progress_length):
        if i < progress:
            bar += progress_chars[i]
        else:
            bar += " "
    return bar

timer = Timer()

async def progress_bar(current, total, reply, start):
    if timer.can_send():
        now = time.time()
        diff = now - start
        if diff < 1:
            return

        elapsed_time = round(diff)
        speed = current / elapsed_time
        remaining_bytes = total - current
        eta = hrt(remaining_bytes / speed, precision=1) if speed > 0 else "-"
        sp = f"{hrb(speed)}/s"
        tot = hrb(total)
        cur = hrb(current)
        progress_bar = create_custom_bar(current, total)

        try:
            await reply.edit(
                f'`\n'
                f'╭──⌯════•|•𝐁𝐨𝐭 𝐒𝐭𝐚𝐭𝐢𝐜𝐬•|•════⌯──╮\n'
                f'├⚡ **Progress:** {progress_bar}\n'
                f'├🚀 **Speed:** {sp}\n'
                f'├📟 **Processed:** {cur}\n'
                f'├🧲 **Size - ETA:** {tot} - {eta}\n'
                f'╰─═══•✨🦋𝐊𝐔𝐍𝐀𝐋🦋✨•═══─╯\n'
                f'`'
            )
        except FloodWait as e:
            time.sleep(e.x)

# Example simulation function
async def simulate_progress(reply):
    total = 100
    start = time.time()
    for current in range(0, total + 1, 10):  # Simulate progress in steps of 10
        await progress_bar(current, total, reply, start)
        time.sleep(1)  # Simulate time delay

# Example of a mock `reply` object for testing purposes
class MockReply:
    async def edit(self, text):
        print(text)

# Simulate the progress bar
mock_reply = MockReply()
import asyncio
asyncio.run(simulate_progress(mock_reply))
