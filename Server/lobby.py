import asyncio
import json
from send import Send

class Lobby:
    allPlayerInLobby = []
    ifTimeToStartGame = False
    timerLobby = 0

    async def addPlayerToLobby(player):
        Lobby.allPlayerInLobby.append(player)
        await Send.sendMessageToPlayer(player.client, json.dumps(["client_success_join_to_lobby", 20]))
        await Send.sendMessageToAll(Lobby.allPlayerInLobby, json.dumps(["client_list_player_in_lobby", Lobby.nicksWithList()]))

        if len(Lobby.allPlayerInLobby) > 1 and Lobby.ifTimeToStartGame == False:
            Lobby.ifTimeToStartGame = True
            Lobby.timerLobby = asyncio.create_task(Lobby.timeToStartGame())

    async def removePlayerWithLobby(player):
        if Lobby.findPlayerInList(player):
            Lobby.allPlayerInLobby.remove(player)
            await Send.sendMessageToPlayer(player.client, json.dumps(["client_success_leave_lobby"]))
            await Send.sendMessageToAll(Lobby.allPlayerInLobby, json.dumps(["client_list_player_in_lobby", Lobby.nicksWithList()]))

        if len(Lobby.allPlayerInLobby) < 2 and Lobby.ifTimeToStartGame == True:
            Lobby.ifTimeToStartGame = False
            Lobby.timerLobby.cancel()
            await Send.sendMessageToAll(Lobby.allPlayerInLobby, json.dumps(["client_time_to_start_game", -1]))

    async def timeToStartGame():
        for time_to_start in range(60, 0, -1):
            await Send.sendMessageToAll(Lobby.allPlayerInLobby, json.dumps(["client_time_to_start_game", time_to_start]))
            await asyncio.sleep(1)

    def nicksWithList():
        nicks_list = []

        for player in Lobby.allPlayerInLobby:
            nicks_list.append(player.nick)

        return nicks_list

    def findPlayerInList(findPlayer):
        for player in Lobby.allPlayerInLobby:
            if player == findPlayer:
                return True
        return False
