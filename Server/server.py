import websockets
import json
import re
from lobby import Lobby
from player import Player
from send import Send

class Server:
    allPlayerOnline = []

    def findPlayerInList(clientSocket):
        for player in Server.allPlayerOnline:
            if player.client == clientSocket:
                return player

    async def validatePassword(password, clientSocket):
        goodPassword = True

        if len(password) < 3:
            await Send.sendMessageToPlayer(clientSocket, json.dumps(["client_faill_nick_too_short"]))
            goodPassword = False

        if len(password) > 15:
            await Send.sendMessageToPlayer(clientSocket, json.dumps(["client_faill_nick_too_long"]))
            goodPassword = False

        if not re.match(r'^[a-zA-Z0-9]+$', password):
            await Send.sendMessageToPlayer(clientSocket, json.dumps(["client_faill_nick_illegal_characters"]))
            goodPassword = False

        return goodPassword

    async def newPlayerConnected(clientSocket):
        try:
            while True:
                newMessage = json.loads(await clientSocket.recv())
                print("newPlayerConnected() ", newMessage)

                if newMessage[0] == "server_login":
                    if await Server.validatePassword(newMessage[1], clientSocket):
                        Server.allPlayerOnline.append(Player(clientSocket, newMessage[1]))
                        await Send.sendMessageToPlayer(clientSocket, json.dumps(["client_success_login", newMessage[1]]))
                        await Send.sendMessageToAll(Server.allPlayerOnline, json.dumps(["client_sum_online_player", len(Server.allPlayerOnline)]))

                elif newMessage[0] == "server_join_to_lobby":
                    await Lobby.addPlayerToLobby(Server.findPlayerInList(clientSocket))

                elif newMessage[0] == "server_leave_lobby":
                    await Lobby.removePlayerWithLobby(Server.findPlayerInList(clientSocket))

                elif newMessage[0] == "server_logout_with_game":
                    Server.allPlayerOnline.remove(Server.findPlayerInList(clientSocket))
                    await Send.sendMessageToPlayer(clientSocket, json.dumps(["client_success_logout_with_game"]))
                    await Send.sendMessageToAll(Server.allPlayerOnline, json.dumps(["client_sum_online_player", len(Server.allPlayerOnline)]))
                    break

        except websockets.exceptions.ConnectionClosed:
            try:
                await Lobby.removePlayerWithLobby(Server.findPlayerInList(clientSocket))
                Server.allPlayerOnline.remove(Server.findPlayerInList(clientSocket))
                await Send.sendMessageToAll(Server.allPlayerOnline, json.dumps(["client_sum_online_player", len(Server.allPlayerOnline)]))
            except:
                print("newPlayerConnected() Error disconected player")
