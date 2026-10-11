
# PASO 1. IMPORTAR LIBRERIAS
import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# PASO 2. CREAR LA APLICACION
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "chat-tiendas-local"
)

# PASO 3. CREAR SOCKETIO
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

# PASO 4. RUTA PRINCIPAL
@app.route("/")
@app.route("/chat")
def inicio():
    return render_template("chat.html")

# PASO 5. DETECTAR USUARIO CONECTADO
@socketio.on("connect")
def conectar():
    print("USUARIO CONECTADO")

# PASO 6. DETECTAR USUARIO DESCONECTADO
@socketio.on("disconnect")
def desconectar():
    print("USUARIO DESCONECTADO")

# PASO 7. RECIBIR MENSAJES
@socketio.on("mensaje")
def recibir_mensaje(mensaje):
    print("MENSAJE RECIBIDO:", mensaje)

    # Enviar a todos los usuarios conectados
    emit("mensaje", mensaje, broadcast=True)

# PASO 8. INICIAR SERVIDOR LOCAL
if __name__ == "__main__":
    print("SERVIDOR INICIADO")
    socketio.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
