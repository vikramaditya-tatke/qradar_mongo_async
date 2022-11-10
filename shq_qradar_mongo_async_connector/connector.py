import asyncio
import pylogging
import startserver

#TODO: Add proper exception handling by removing the generic "Exception"
async def main():
    pylogging.init_logging()
    await startserver.start_server()


asyncio.run(main())
