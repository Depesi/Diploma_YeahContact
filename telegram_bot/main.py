import asyncio

from app.Core import dp, bot
from app.Commands import *


async def main():
    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
