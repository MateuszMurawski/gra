import websockets
import json
from lobby import Lobby
from player import Player
from send import Send

class Server:

    allPlayerOnline = []
    
    def findPlayerInList(clientSocket):
        for player in Server.allPlayerOnline:
            if player.client == clientSocket:
                return player

    async def newPlayerConnected(clientSocket):
        try:
            newMessage = json.loads(await clientSocket.recv())
            print("newPlayerConnected() ", newMessage)

            if newMessage[0] == "server_login":
                Server.allPlayerOnline.append(Player(clientSocket, newMessage[1]))
                await Send.sendMessageToPlayer(clientSocket, json.dumps(["client_success_login"]))
                await Send.sendMessageToAll(Server.allPlayerOnline, json.dumps(["client_sum_online_player", len(Server.allPlayerOnline)]))

            while True:
                newMessage = json.loads(await clientSocket.recv())
                print("newPlayerConnected() ", newMessage)

                if newMessage[0] == "server_leave_game":
                    await Lobby.removePlayerWithLobby(Server.findPlayerInList(clientSocket))
                    Server.allPlayerOnline.remove(Server.findPlayerInList(clientSocket))
                    await Send.sendMessageToAll(Server.allPlayerOnline, json.dumps(["client_sum_online_player", len(Server.allPlayerOnline)]))
                    break

                elif newMessage[0] == "server_join_to_lobby":
                    await Lobby.addPlayerToLobby(Server.findPlayerInList(clientSocket))

                elif newMessage[0] == "server_leave_lobby":
                    await Lobby.removePlayerWithLobby(Server.findPlayerInList(clientSocket))
        
        except websockets.exceptions.ConnectionClosed:
            await Lobby.removePlayerWithLobby(Server.findPlayerInList(clientSocket))
            Server.allPlayerOnline.remove(Server.findPlayerInList(clientSocket))
            await Send.sendMessageToAll(Server.allPlayerOnline, json.dumps(["client_sum_online_player", len(Server.allPlayerOnline)]))
            
            try:
                await game.handleDisconnect(clientSocket)
            except:
                print("newPlayerConnected() Error disconected player")
        
            
