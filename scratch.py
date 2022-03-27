# Scratch file for testing simple code

import asyncio

async def main():
    # Returns a co-routine object whose execution must be awaited
    print("Matt")
    task = asyncio.create_task(foo("Text"))
    print("Finish")

async def foo(text):
    print(text)
    await asyncio.sleep(1)

# Event loop
asyncio.run(main())
