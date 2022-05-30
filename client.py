import threading

import grpc

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

address = 'localhost'
port = 11912

class Client:

    def __init__(self, u: str):
        self.username = u

        # cria o canal gRPC
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServerStub(channel)

        # cria uma nova listening thread para quando novas mesagens chegarem
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()

        self.send_message() #chama a criação da mensagem

    def __listen_for_messages(self):
      # Aqui a thread fica esperando por novas mesagens para mostrá-las
      for note in self.conn.ChatStream(chat.Empty()):  
        print("R[{}]: {}".format(note.name, note.message))

    def send_message(self): 
        message = input("Send: ")# Recebe a mensagem do usuário
        try:
            while message != '':
                n = chat.Note()  # cria um objeto para as mensagens
                n.name = self.username  # define username
                n.message = message  # define a mesagem no objeto
                self.conn.SendNote(n)  # manda o objeto para o servidor
                message = input("")
        except:
            print("\nEnd Of Chat")

if __name__ == '__main__':
    username = None
    while username is None:
        # recupera o username para podemos diferenciar os diferentes clientes
        username = input("Name? ")
    c = Client(username)  # inicia o Client e faz a thread manter a conexão com o servidor
