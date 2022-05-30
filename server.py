from concurrent import futures

import grpc
import time

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc


class ChatServer(rpc.ChatServerServicer):  # herdando os arquivos proto do rpc que são gerados

    def __init__(self):
        # Lista com todo o histórico do chat
        self.chats = []

    # O fluxo que será usado para enviar novas mensagens aos clientes
    def ChatStream(self, request_iterator, context):

        lastindex = 0
        # Para cada cliente, um loop infinito é iniciado
        while True:
            # Verifica se existem novas mensagens
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request: chat.Note, context):
        # Mostra as mensagens no console do server
        print("[{}]: {}".format(request.name, request.message))
        # Adiciona a mensagen ao histórico do chat
        self.chats.append(request)
        return chat.Empty()  # A linguagem proto necessita de retorno: retorna chat vazio


if __name__ == '__main__':
    port = 11912  # Define porta aleatória para rodar o servidor
 
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # Cria o servidor gRPC (máximo de clientes)
    rpc.add_ChatServerServicer_to_server(ChatServer(), server)  # Faz registro no servidor gRPC
    
    # gRPC faz tudo praticamente sozinho 
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()

    # O servidor não continua funcionando sem parar, então criamos o loop a seguir
    try:
        while True:
            time.sleep(64 * 64 * 100)
    except:
        print("\nEnd Of Chat")
