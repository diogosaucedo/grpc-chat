# Projeto de Chat em Tempo Real

Este é um aplicativo de chat simples desenvolvido em Python que utiliza gRPC para comunicação em tempo real. O projeto inclui um cliente com uma interface gráfica usando Tkinter e um servidor que gerencia a comunicação entre os clientes.

## Funcionalidades

- Envio e recebimento de mensagens em tempo real.
- Interface gráfica simples para interação do usuário.
- Suporte para múltiplos clientes se conectando ao mesmo servidor.

## Instalando Dependências

Para instalar as dependências necessárias, siga os passos abaixo:

```bash
python -m venv venv  # Criação de um ambiente virtual
./venv/Scripts/activate  # Ativação do ambiente virtual (Windows: .\venv\Scripts\activate)
pip install -r requirements.txt  # Instalação das dependências
```

## Gerando gRPC a partir do arquivo .proto

Você pode executar os arquivos com extensão .bat ou .sh para gerar os arquivos gRPC. Lembre-se que, como esses arquivos serão gerados dentro da pasta "proto", você precisará atualizar a importação no arquivo chat_pb2_grpc.py na linha 6 para:

```python
import proto.chat_pb2 as chat_pb2
```

## Iniciando servidor:

Para iniciar o servidor, execute o seguinte comando:

```bash
python server.py

```

Iniciando cliente:
Para iniciar o cliente, execute:

```bash
python cliente.py

```

## Nota

Lembre-se que, se você for utilizar em computadores distintos, o computador que executar o cliente para enviar mensagens para onde está o servidor precisará alterar o valor da variável address de 'localhost' para o seu endereço IP:

```python
address = 'SEU_IP'


```

# Contribuições

Sinta-se à vontade para enviar um pull request ou abrir uma issue se encontrar algum problema ou tiver sugestões de melhorias.
