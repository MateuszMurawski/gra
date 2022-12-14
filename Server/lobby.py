import asyncio
import json
from send import Send

class Lobby:
    allPlayerInLobby = []
    ifTimeToStartGame = False
    timerLobby = 0
    maxPlayersInLobby = 20

    async def addPlayerToLobby(player):
        Lobby.allPlayerInLobby.append(player)
        await Send.sendMessageToPlayer(player.client, json.dumps(["client_success_join_to_lobby", Lobby.maxPlayersInLobby]))
        await Send.sendMessageToAll(Lobby.allPlayerInLobby, json.dumps(["client_list_player_in_lobby", Lobby.nicksWithList()]))

        if len(Lobby.allPlayerInLobby) > 1 and Lobby.ifTimeToStartGame == False:
            Lobby.ifTimeToStartGame = True
            Lobby.timerLobby = asyncio.create_task(Lobby.timeToStartGame())

        if len(Lobby.allPlayerInLobby) >= 20:
            await Send.sendMessageToAll(Lobby.allPlayerInLobby, json.dumps(["client_start_new_game"]))

    async def removePlayerWithLobby(player):
        if Lobby.findPlayerInList(player):
            try:
                Lobby.allPlayerInLobby.remove(player)
            except:
                print("removePlayerWithLobby() Error remove player with lobby")
            await Send.sendMessageToPlayer(player.client, json.dumps(["client_success_leave_lobby"]))
            await Send.sendMessageToAll(Lobby.allPlayerInLobby, json.dumps(["client_list_player_in_lobby", Lobby.nicksWithList()]))

        if len(Lobby.allPlayerInLobby) < 2 and Lobby.ifTimeToStartGame == True:
            try:
                Lobby.timerLobby.cancel()
            except:
                print("removePlayerWithLobby() Error cancel() timerLobby")
            Lobby.ifTimeToStartGame = False
            await Send.sendMessageToAll(Lobby.allPlayerInLobby, json.dumps(["client_time_to_start_game", -1]))

    async def timeToStartGame():
        for timeToStart in range(60, 0, -1):
            await Send.sendMessageToAll(Lobby.allPlayerInLobby, json.dumps(["client_time_to_start_game", timeToStart]))
            await asyncio.sleep(1)

        await Send.sendMessageToAll(Lobby.allPlayerInLobby, json.dumps(["client_start_new_game"]))

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
