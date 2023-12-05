import pygame as p
import sys
import ChessMain
class Menu:
    def __init__(self):
        p.init()
        self.width, self.height = 720, 480
        self.screen = p.display.set_mode((self.width, self.height))
        p.display.set_caption("Menú de Inicio")
        self.mainClock = p.time.Clock()

        # Colores
        self.white = (255, 255, 255)

        # Cargar la imagen de fondo
        self.background_image = p.image.load("imagesBG/menuBK.jpg")  # Cambia "background.jpg" por la ruta de tu imagen
        self.background_rect = self.background_image.get_rect()

        # Definir los botones
        self.start_button = p.Rect(self.width // 2 - 100, self.height // 2 - 50, 200, 50)
        self.credits_button = p.Rect(self.width // 2 - 100, self.height // 2 + 20, 200, 50)
        self.quit_button = p.Rect(self.width // 2 - 100, self.height // 2 + 90, 200, 50)

    def show_text(self, text, size, position):
        font = p.font.Font(None, size)
        text_surface = font.render(text, True, self.white)
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, rect, color, text, text_color):
        p.draw.rect(self.screen, color, rect)
        font = p.font.Font(None, 24)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def show_credits(self):
        p.display.set_caption("Creditos")
        self.screen.blit(self.background_image, self.background_rect)

        # Texto de créditos
        title = "Chess With AI"
        dev = " • Inspirado por: Eddie Sharick"
        dev2 = "• Editado y Actualizado por: xMeiker"
        credits_text = "• Nuevas Funciones y Menu Custom por: xMeiker"
        credits_text1 = "• Desarrollado por: xMeiker"
        credits_text2 = "Versión 1.0"
        credits_text3 = "Controles:"
        credits_text4 = "• Presionar z para deshacer un movimiento."
        credits_text5 = "• Presionar r para reiniciar el juego."
        self.show_text(title, 46, (self.width // 2, 50))
        self.show_text(dev, 24, (self.width // 2, 100))
        self.show_text(dev2, 24, (self.width // 2, 130))
        self.show_text(credits_text, 24, (self.width // 2, 160))
        self.show_text(credits_text1, 24, (self.width // 2, 190))
        self.show_text(credits_text2, 24, (self.width // 2, 450))
        self.show_text(credits_text3, 46, (self.width // 2, 270))
        self.show_text(credits_text4, 24, (self.width // 2, 320))
        self.show_text(credits_text5, 24, (self.width // 2, 350))

        p.display.flip()

        # Esperar hasta que se haga clic en cualquier parte de la ventana
        waiting_for_click = True
        while waiting_for_click:
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()
                elif event.type == p.MOUSEBUTTONDOWN:
                    waiting_for_click = False
        p.display.update()
        p.display.set_caption("Menú de Inicio")
        self.mainClock.tick(60)
    def run(self):
        while True:
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()
                elif event.type == p.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        print("Empezar juego")
                        ChessMain.Inicio()
                    elif self.credits_button.collidepoint(event.pos):
                        print("Ver creditos")
                        self.show_credits()
                    elif self.quit_button.collidepoint(event.pos):
                        print("Saliendo...")
                        p.quit()
                        sys.exit()

            # Dibujar la imagen de fondo
            self.screen.blit(self.background_image, self.background_rect)

            # Mostrar texto en el centro de la pantalla
            self.show_text("Chess AI", 72, (self.width // 2, self.height // 4))

            # Dibujar los botones
            self.draw_button(self.start_button, (107,107,107), "Empezar", self.white)
            self.draw_button(self.credits_button, (107,107,107), "Créditos", self.white)
            self.draw_button(self.quit_button, (107,107,107), "Salir", self.white)

            # Actualizar la pantalla
            p.display.flip()

if __name__ == "__main__":
    menu = Menu()
    menu.run()
