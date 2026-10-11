import flet as ft
import socketio


ROJO = "#E31B23"
NEGRO = "#0E0F11"
FONDO = "#F1F3F6"

NOMBRE_TIENDA = "TIENDA PEPE"


def main(page: ft.Page):

    page.title = f"Chat - {NOMBRE_TIENDA}"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = FONDO

    page.window.width = 400
    page.window.height = 780

    sio = socketio.Client()

    mensajes = ft.ListView(
        expand=True,
        spacing=12,
        padding=15,
        auto_scroll=True
    )

    mensaje_inicio = ft.Container(
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
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8
        ),
        alignment=ft.Alignment(0, 0),
        padding=25
    )

    mensajes.controls.append(mensaje_inicio)

    def burbuja_cliente(texto):

        return ft.Row(
            [
                ft.Container(
                    content=ft.Column(
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
                    ),
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
            ],
            alignment=ft.MainAxisAlignment.START
        )

    def burbuja_tienda(texto):

        return ft.Row(
            [
                ft.Container(
                    content=ft.Column(
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
                    ),
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
            ],
            alignment=ft.MainAxisAlignment.END
        )

    @sio.event
    def connect():
        print("TIENDA CONECTADA AL SERVIDOR")

    @sio.event
    def disconnect():
        print("TIENDA DESCONECTADA DEL SERVIDOR")

    @sio.on("mensaje")
    def recibir_mensaje(mensaje):

        print("MENSAJE RECIBIDO:", mensaje)

        if not isinstance(mensaje, dict):
            return

        if mensaje.get("tienda") != NOMBRE_TIENDA:
            return

        if mensaje.get("usuario") == "Tienda":
            return

        texto = mensaje.get("texto", "")

        if not texto:
            return

        if mensaje_inicio in mensajes.controls:
            mensajes.controls.remove(mensaje_inicio)

        mensajes.controls.append(
            burbuja_cliente(texto)
        )

        try:
            mensajes.update()
        except Exception as error:
            print("ERROR ACTUALIZANDO CHAT:", error)

    try:

        sio.connect(
            "http://127.0.0.1:5000"
        )

    except Exception as error:

        print(
            "NO SE PUDO CONECTAR AL SERVIDOR:",
            error
        )

    campo_mensaje = ft.TextField(
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

    def enviar_mensaje(e):

        texto = (
            campo_mensaje.value
            or ""
        ).strip()

        if not texto:
            return

        if mensaje_inicio in mensajes.controls:
            mensajes.controls.remove(mensaje_inicio)

        mensajes.controls.append(
            burbuja_tienda(texto)
        )

        campo_mensaje.value = ""

        page.update()

        mensaje = {
            "tienda": NOMBRE_TIENDA,
            "usuario": "Tienda",
            "texto": texto
        }

        try:

            if sio.connected:

                sio.emit(
                    "mensaje",
                    mensaje
                )

            else:

                print(
                    "SOCKET.IO NO ESTÁ CONECTADO"
                )

        except Exception as error:

            print(
                "ERROR ENVIANDO MENSAJE:",
                error
            )

    campo_mensaje.on_submit = enviar_mensaje

    cabecera = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    NOMBRE_TIENDA,
                    size=18,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Row(
                    [
                        ft.Container(
                            width=8,
                            height=8,
                            bgcolor="#46C76B",
                            border_radius=4
                        ),
                        ft.Text(
                            "Conectada",
                            size=11,
                            color="#D0D0D0"
                        )
                    ],
                    spacing=6
                )
            ],
            spacing=3
        ),
        bgcolor=NEGRO,
        padding=15
    )

    boton_enviar = ft.Container(
        content=ft.Icon(
            ft.Icons.SEND,
            color=ft.Colors.WHITE,
            size=24
        ),
        width=54,
        height=54,
        bgcolor=ROJO,
        border_radius=27,
        alignment=ft.Alignment(0, 0),
        on_click=enviar_mensaje
    )

    barra_mensaje = ft.Container(
        content=ft.Row(
            [
                campo_mensaje,
                boton_enviar
            ],
            spacing=10
        ),
        bgcolor=ft.Colors.WHITE,
        padding=12
    )

    page.add(
        ft.Column(
            [
                cabecera,

                ft.Container(
                    content=mensajes,
                    expand=True,
                    bgcolor=FONDO
                ),

                barra_mensaje
            ],
            expand=True,
            spacing=0
        )
    )


if __name__ == "__main__":

    ft.run(main)