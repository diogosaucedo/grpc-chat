from concurrent import futures
import grpc
import time

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

class ChatServer(rpc.ChatServerServicer):

    def __init__(self):
        self.chats = []

    def ChatStream(self, request_iterator, context):
        lastindex = 0
        while True:
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n
            time.sleep(0.1)  # Evita busy waiting

    def SendNote(self, request: chat.Note, context):
        print(f"[{request.name}] {request.message}")
        self.chats.append(request)
        return chat.Empty()

if __name__ == '__main__':
    port = 11912
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_ChatServerServicer_to_server(ChatServer(), server)
    print('Starting server. Listening...')
    server.add_insecure_port(f'[::]:{port}')
    server.start()

    try:
        while True:
            time.sleep(64 * 64 * 100)
    except KeyboardInterrupt:
        print("Server stopping...")
        server.stop(0)