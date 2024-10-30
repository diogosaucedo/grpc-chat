from concurrent import futures
import grpc
import time
import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

class ChatServer(rpc.ChatServerServicer):
    def __init__(self):
        """Inicializa o servidor de chat com uma lista de mensagens."""
        self.messages = []  # Armazena mensagens recebidas

    def ChatStream(self, request_iterator, context):
        """Método para transmitir mensagens de chat para os clientes."""
        last_index = 0  # Índice para rastrear a última mensagem enviada
        while True:
            # Envia novas mensagens para os clientes
            while len(self.messages) > last_index:
                message = self.messages[last_index]
                last_index += 1
                yield message
            time.sleep(0.1)  # Evita busy waiting

    def SendNote(self, request: chat.Note, context):
        """Recebe uma nova mensagem e a armazena no servidor."""
        print(f"[{request.name}] {request.message}")  # Exibe a mensagem no console
        self.messages.append(request)  # Adiciona a mensagem à lista
        return chat.Empty()  # Retorna uma resposta vazia

if __name__ == '__main__':
    port = 11912
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_ChatServerServicer_to_server(ChatServer(), server)
    
    # Inicia o servidor e escuta na porta especificada
    print('Starting server. Listening...')
    server.add_insecure_port(f'[::]:{port}')
    server.start()

    try:
        while True:
            time.sleep(64 * 64 * 100)  # Mantém o servidor em execução
    except KeyboardInterrupt:
        print("Server stopping...")
        server.stop(0)  # Para o servidor de forma limpa
