import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "clave-local-desarrollo"
)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)


def limpiar_mensaje(datos):
    if not isinstance(datos, dict):
        return None

    usuario = str(
        datos.get("usuario", "Cliente")
    )[:30]

    texto = str(
        datos.get("texto", "")
    ).strip()[:2000]

    if not texto:
        return None

    return {
        "usuario": usuario,
        "texto": texto
    }


@app.route("/")
@app.route("/chat")
def inicio():
    return render_template("chat.html")


@socketio.on("connect")
def conectar():
    print("USUARIO CONECTADO")


@socketio.on("disconnect")
def desconectar():
    print("USUARIO DESCONECTADO")


@socketio.on("mensaje")
def recibir_mensaje(datos):
    mensaje = limpiar_mensaje(datos)

    if mensaje is None:
        return

    print(
        "MENSAJE RECIBIDO:",
        mensaje
    )

    emit(
        "mensaje",
        mensaje,
        broadcast=True
    )


def iniciar_servidor():
    puerto = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    print(
        "SERVIDOR CHAT ONLINE INICIADO"
    )

    socketio.run(
        app,
        host="0.0.0.0",
        port=puerto,
        debug=False
    )


if __name__ == "__main__":
    iniciar_servidor()
