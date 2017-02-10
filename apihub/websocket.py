#!/usr/bin/env python

import asyncio
import aiopg

import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print("< {}".format(name))

    greeting = "Hello {}!".format(name)
    await websocket.send(greeting)
    print("> {}".format(greeting))


connected = {}

async def handler(websocket, path):
    print(path)
    global connected
    # Register.

    connected[path[1:]] = websocket
    print(connected)
    # try:
    #     # Implement logic here.
    #     #await asyncio.wait([ws.send("Hello!") for ws in connected])
    #
    #     await asyncio.wait([connected['key123'].send("this is message to this particular stuff")])
    #     await asyncio.sleep(100)
    #
    #     while True:
    #         for i in
    # finally:
    #     pass
    #     # Unregister.
    #     #connected.remove(websocket)


    while True:
        message = await websocket.recv()
        await consumer(message)


async def consumer(message):
    print("MSG FROM CLIENT - > " , message)
#============================P
dsn = 'dbname=postgres user=postgres password=postgres host=127.0.0.1'


async def notify(conn):
    async with conn.cursor() as cur:
        for i in range(5):
            msg = "message {}".format(i)
            print('Send ->', msg)
            await cur.execute("NOTIFY channel, '{}'".format(msg))

        #await cur.execute("NOTIFY channel, 'finish'")

async def listen(conn):
    global connected
    async with conn.cursor() as cur:
        await cur.execute("LISTEN channel")
        while True:
            msg = await conn.notifies.get()
            if msg.payload == 'finish':
                return
            else:
                print('Receive <-', msg.payload)
                print(connected)
                try:
                    if connected is not None and connected['key123'] is not None:
                        await asyncio.wait([connected['key123'].send(msg.payload)])
                except KeyError as ke:
                    print("ERROR " , ke)

async def main():
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn1:
            listener = listen(conn1)
            async with pool.acquire() as conn2:
                notifier = notify(conn2)
                await asyncio.gather(listener, notifier)
    print("ALL DONE")



start_server = websockets.serve(handler, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()
