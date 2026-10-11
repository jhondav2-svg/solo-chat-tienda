
import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# CREAR APLICACION
app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "clave-local-desarrollo"
)

# CONFIGURAR SOCKET.IO
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

# PAGINA PRINCIPAL
@app.route("/")
@app.route("/chat")
def inicio():
    return render_template("chat.html")


# USUARIO CONECTADO
@socketio.on("connect")
def conectar():
    print("USUARIO CONECTADO")


# USUARIO DESCONECTADO
@socketio.on("disconnect")
def desconectar():
    print("USUARIO DESCONECTADO")


# RECIBIR Y ENVIAR MENSAJES
@socketio.on("mensaje")
def recibir_mensaje(datos):

    if not isinstance(datos, dict):
        return

    usuario = str(datos.get("usuario", "Cliente"))[:30]
    texto = str(datos.get("texto", "")).strip()[:2000]

    if not texto:
        return

    mensaje = {
        "usuario": usuario,
        "texto": texto
    }

    print("MENSAJE RECIBIDO:", mensaje)

    emit("mensaje", mensaje, broadcast=True)


# INICIAR SERVIDOR
if __name__ == "__main__":

    puerto = int(os.environ.get("PORT", 5000))

    print("SERVIDOR CHAT ONLINE INICIADO")

    socketio.run(
        app,
        host="0.0.0.0",
        port=puerto,
        debug=False
    )
