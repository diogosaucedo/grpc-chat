import threading
from tkinter import *
from tkinter import simpledialog
import grpc
import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

address = 'localhost'
port = 11912


class Client:
    def __init__(self, username: str, window):
        """Inicializa o cliente com nome de usuário e configura a interface."""
        self.window = window
        self.username = username

        # Cria um canal gRPC e um stub
        channel = grpc.insecure_channel(f"{address}:{port}")
        self.conn = rpc.ChatServerStub(channel)

        # Inicia uma thread para ouvir mensagens
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        self.__setup_ui()
        self.window.mainloop()

    def __listen_for_messages(self):
        """Escuta mensagens do servidor em uma thread separada."""
        for note in self.conn.ChatStream(chat.Empty()):
            print(f"R[{note.name}] {note.message}")  # Debugging statement
            self.chat_list.insert(END, f"[{note.name}] {note.message}\n")  # Adiciona a mensagem à UI

    def send_message(self, event):
        """Envia a mensagem quando o usuário pressiona Enter."""
        message = self.entry_message.get().strip()  # Recupera e limpa espaços em branco
        if message:
            note = chat.Note()  # Cria a mensagem protobuf
            note.name = self.username  # Define o nome de usuário
            note.message = message  # Define a mensagem
            print(f"S[{note.name}] {note.message}")  # Debugging statement
            self.conn.SendNote(note)  # Envia a mensagem para o servidor

            self.entry_message.delete(0, END)  # Limpa a caixa de entrada

    def __setup_ui(self):
        """Configura a interface do usuário."""
        self.chat_list = Text(self.window, height=15, width=50)  # Aumenta a altura da lista de chat
        self.chat_list.pack(side=TOP)

        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.pack(side=LEFT)

        self.entry_message = Entry(self.window, bd=5, width=50)  # Aumenta a largura da caixa de entrada
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)


if __name__ == '__main__':
    root = Tk()  # Cria a janela principal
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()  # Oculta a janela até que o nome de usuário seja definido
    username = None

    while username is None:
        username = simpledialog.askstring("Username", "What's your username?", parent=root)

    root.deiconify()  # Mostra a janela principal
    Client(username, frame)  # Inicia o cliente
