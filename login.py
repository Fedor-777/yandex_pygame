import os
import sqlite3

import pygame

from settings import *


def login():
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, SIZE_TEXT)
    text = ""
    input_active = True
    run = True
    name = ''
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    background_image = pygame.image.load(os.path.join(os.path.dirname(__file__), "изображение.png"))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_TAB:
                    name = text
                    run = False
                    # _________создание/добавление ника в бд
                    create_database_books()
                    query = "SELECT * FROM stats WHERE nick_player = ?"
                    cursor.execute(query, (name,))
                    rows = cursor.fetchall()
                    id = get_max_id() + 1
                    if len(rows) > 0:
                        print(f"Ник '{name}' уже существует в таблице.")
                    else:
                        print(f"Ник '{name}' добавлен в таблицу.")
                        cursor.execute("INSERT INTO stats VALUES (?, ?, ?, ?)", (id, name, 0, 1))
                        conn.commit()
                else:
                    text += event.unicode

        # ______Отрисовка и создание текстов
        # window.fill((0, 0, 0))
        window.blit(background_image, (0, 0))
        text_surf = font.render("Введите свой ник и нажмите таб:", True, (255, 255, 255))
        window.blit(text_surf, (40, 300))
        text_surf_input = font.render(text, True, (255, 0, 0))
        window.blit(text_surf_input, text_surf_input.get_rect(center=window.get_rect().center))
        pygame.display.flip()
        clock.tick(60)

    conn.close()
    return name


def create_database_books():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stats
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nick_player TEXT, score INTEGER, lvl INTEGER)''')
    conn.commit()
    conn.close()


def get_max_id():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT MAX(id) FROM stats")
    max_id = c.fetchone()[0]
    conn.close()
    if max_id is not None:
        return max_id
    else:
        return 0
