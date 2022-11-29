class Send:
    async def sendMessageToPlayer(player, message):
        await player.send(message)
        print("sendMessageToPlayer() ", message)

    async def sendMessageToAll(allPlayer, message):
        for player in allPlayer:
            await player.client.send(message)
            print("sendMessageToAll() ", message)