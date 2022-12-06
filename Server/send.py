class Send:
    async def sendMessageToPlayer(player, message):
        try:
            await player.send(message)
        except:
            print("sendMessageToPlayer() Error send message")
        print("sendMessageToPlayer() ", message)

    async def sendMessageToAll(allPlayer, message):
        for player in allPlayer:
            try:
                await player.client.send(message)
            except:
                print("sendMessageToAll() Error send message")
            print("sendMessageToAll() ", message)