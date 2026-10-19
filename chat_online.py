import os
import flet as ft
import socketio

ROJO = "#E31B23"
NEGRO = "#0E0F11"
FONDO = "#F1F3F6"

NOMBRE_TIENDA = "TIENDA PEPE"

SERVIDOR = os.environ.get(
    "CHAT_SERVER_URL",
    "http://127.0.0.1:5000"
)

class ChatOnline:

    def __init__(self, page: ft.Page):

        self.page = page
        self.sio = socketio.Client()

        self.configurar_pagina()
        self.crear_controles()
        self.configurar_socket()
        self.mostrar_interfaz()
        self.conectar_servidor()

    def configurar_pagina(self):

        self.page.title = f"Chat - {NOMBRE_TIENDA}"

        self.page.padding = 0
        self.page.spacing = 0

        self.page.bgcolor = FONDO

        self.page.window.width = 400
        self.page.window.height = 780

    def crear_controles(self):

        self.mensajes = ft.ListView(
            expand=True,
            spacing=12,
            padding=15,
            auto_scroll=True
        )

        self.mensaje_inicio = (
            self.crear_mensaje_inicio()
        )

        self.mensajes.controls.append(
            self.mensaje_inicio
        )

        self.campo_mensaje = (
            self.crear_campo_mensaje()
        )

        self.campo_mensaje.on_submit = (
            self.enviar_mensaje
        )

        self.boton_enviar = (
            self.crear_boton_enviar()
        )

    def crear_mensaje_inicio(self):

        return ft.Container(

            content=ft.Column(
                [
                    ft.Icon(
                        ft.Icons.CHAT_BUBBLE_OUTLINE,
                        size=35,
                        color="#999999"
                    ),

                    ft.Text(
                        "Esperando mensajes",
                        size=16,
                        color="#333333",
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Text(
                        NOMBRE_TIENDA,
                        size=12,
                        color="#777777"
                    )
                ],

                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),

                spacing=8
            ),

            alignment=ft.Alignment(
                0,
                0
            ),

            padding=25
        )

    def crear_campo_mensaje(self):

        return ft.TextField(

            hint_text="Responder al cliente...",

            expand=True,

            filled=True,

            bgcolor=ft.Colors.WHITE,

            color=ft.Colors.BLACK,

            cursor_color=ROJO,

            border_color="#DDDDDD",

            focused_border_color=ROJO,

            border_width=1,

            focused_border_width=2,

            border_radius=24,

            content_padding=ft.Padding(
                left=18,
                right=18,
                top=14,
                bottom=14
            )
        )

    def crear_cabecera(self):

        indicador = ft.Container(
            width=8,
            height=8,
            bgcolor="#46C76B",
            border_radius=4
        )

        estado = ft.Text(
            "Conectada",
            size=11,
            color="#D0D0D0"
        )

        fila_estado = ft.Row(
            [
                indicador,
                estado
            ],
            spacing=6
        )

        informacion = ft.Column(
            [
                ft.Text(
                    NOMBRE_TIENDA,
                    size=18,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD
                ),

                fila_estado
            ],
            spacing=3
        )

        return ft.Container(
            content=informacion,
            bgcolor=NEGRO,
            padding=15
        )
        
    def crear_boton_enviar(self):

        return ft.Container(

            content=ft.Icon(
                ft.Icons.SEND,
                color=ft.Colors.WHITE,
                size=24
            ),

            width=54,
            height=54,

            bgcolor=ROJO,

            border_radius=27,

            alignment=ft.Alignment(
                0,
                0
            ),

            on_click=self.enviar_mensaje
        )

    def crear_burbuja_cliente(
        self,
        texto
    ):

        contenido = ft.Column(
            [
                ft.Text(
                    "Cliente",
                    size=10,
                    color="#666666",
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    texto,
                    size=14,
                    color="#222222"
                )
            ],
            spacing=3
        )

        burbuja = ft.Container(
            content=contenido,
            bgcolor=ft.Colors.WHITE,
            width=245,
            padding=12,
            border_radius=ft.BorderRadius(
                top_left=18,
                top_right=18,
                bottom_left=5,
                bottom_right=18
            )
        )

        return ft.Row(
            [burbuja],
            alignment=ft.MainAxisAlignment.START
        )

    def crear_burbuja_tienda(
        self,
        texto
    ):

        contenido = ft.Column(
            [
                ft.Text(
                    "Tú",
                    size=10,
                    color="#FFD6D6",
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    texto,
                    size=14,
                    color=ft.Colors.WHITE
                )
            ],
            spacing=3
        )

        burbuja = ft.Container(
            content=contenido,
            bgcolor=ROJO,
            width=245,
            padding=12,
            border_radius=ft.BorderRadius(
                top_left=18,
                top_right=18,
                bottom_left=18,
                bottom_right=5
            )
        )

        return ft.Row(
            [burbuja],
            alignment=ft.MainAxisAlignment.END
        )

    def ocultar_mensaje_inicio(self):

        if self.mensaje_inicio not in self.mensajes.controls:
            return

        self.mensajes.controls.remove(
            self.mensaje_inicio
        )
        
    def actualizar_chat(self):

        try:

            self.mensajes.update()

        except Exception as error:

            print(
                "ERROR ACTUALIZANDO CHAT:",
                error
            )

    def configurar_socket(self):

        self.sio.on(
            "connect",
            self.servidor_conectado
        )

        self.sio.on(
            "disconnect",
            self.servidor_desconectado
        )

        self.sio.on(
            "mensaje",
            self.recibir_mensaje
        )

    def servidor_conectado(self):

        print(
            "TIENDA CONECTADA AL SERVIDOR"
        )

    def servidor_desconectado(self):

        print(
            "TIENDA DESCONECTADA DEL SERVIDOR"
        )

    def obtener_texto_recibido(
        self,
        mensaje
    ):

        if not isinstance(
            mensaje,
            dict
        ):
            return None

        if mensaje.get(
            "usuario"
        ) == "Tienda":
            return None

        texto = str(
            mensaje.get(
                "texto",
                ""
            )
        ).strip()

        return texto or None

    def recibir_mensaje(
        self,
        mensaje
    ):

        texto = (
            self.obtener_texto_recibido(
                mensaje
            )
        )

        if texto is None:
            return

        self.ocultar_mensaje_inicio()

        self.mensajes.controls.append(
            self.crear_burbuja_cliente(
                texto
            )
        )

        self.actualizar_chat()


    def obtener_texto_escrito(self):

        texto = (
            self.campo_mensaje.value
            or ""
        ).strip()

        return texto or None

    def construir_mensaje(
        self,
        texto
    ):

        return {
            "usuario": "Tienda",
            "texto": texto
        }

    def emitir_mensaje(
        self,
        mensaje
    ):

        if not self.sio.connected:

            print(
                "SOCKET.IO NO ESTÁ CONECTADO"
            )

            return

        try:

            self.sio.emit(
                "mensaje",
                mensaje
            )

        except Exception as error:

            print(
                "ERROR ENVIANDO MENSAJE:",
                error
            )

    def enviar_mensaje(
        self,
        evento
    ):

        texto = (
            self.obtener_texto_escrito()
        )

        if texto is None:
            return

        self.ocultar_mensaje_inicio()

        self.mensajes.controls.append(
            self.crear_burbuja_tienda(
                texto
            )
        )

        self.campo_mensaje.value = ""

        self.page.update()

        mensaje = (
            self.construir_mensaje(
                texto
            )
        )

        self.emitir_mensaje(
            mensaje
        )

    def crear_barra_mensaje(self):

        fila = ft.Row(
            [
                self.campo_mensaje,
                self.boton_enviar
            ],
            spacing=10
        )

        return ft.Container(
            content=fila,
            bgcolor=ft.Colors.WHITE,
            padding=12
        )

    def mostrar_interfaz(self):

        zona_mensajes = ft.Container(
            content=self.mensajes,
            expand=True,
            bgcolor=FONDO
        )

        interfaz = ft.Column(
            [
                self.crear_cabecera(),
                zona_mensajes,
                self.crear_barra_mensaje()
            ],
            expand=True,
            spacing=0
        )

        self.page.add(
            interfaz
        )

    def conectar_servidor(self):

        try:

            self.sio.connect(
                SERVIDOR
            )

        except Exception as error:

            print(
                "NO SE PUDO CONECTAR "
                "AL SERVIDOR:",
                error
            )

def main(page: ft.Page):

    ChatOnline(page)

if __name__ == "__main__":

    ft.run(
        main,
        view=ft.AppView.WEB_BROWSER
    )
