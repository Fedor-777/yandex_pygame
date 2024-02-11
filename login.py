import sqlite3

import pygame
import pygame_gui

from settings import *


def login():
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, SIZE_TEXT)
    run = True
    name = ''
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Pygame GUI сетап
    manager = pygame_gui.UIManager(WINDOW_SIZE)
    input_width = 200
    input_height = 30
    input_x = (WINDOW_SIZE[0] - input_width) / 2
    input_y = (WINDOW_SIZE[1] - input_height) / 2
    text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((input_x, input_y),
                                                                              (input_width, input_height)),
                                                     manager=manager)

    while run:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == text_entry:
                        name = text_entry.get_text()
                        run = False
                        # добавление в дб
                        create_database_books()
                        query = "SELECT * FROM stats WHERE nick_player = ?"
                        cursor.execute(query, (name,))
                        rows = cursor.fetchall()
                        id = get_max_id() + 1
                        if len(rows) > 0:
                            print(f"Ник '{name}' уже существует в таблице.")
                        else:
                            print(f"Ник '{name}' добавлен в таблицу.")
                            cursor.execute("INSERT INTO stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                           (id, name, 0, 0, 0, 0, 0, 0, 0))
                            conn.commit()

            manager.process_events(event)

        manager.update(time_delta)
        window.fill((0, 0, 0))
        text_surf = font.render("Введите свой ник и нажмите enter:", True, (255, 255, 255))
        window.blit(text_surf, (40, 300))
        manager.draw_ui(window)
        pygame.display.update()

    conn.close()
    return name


def create_database_books():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stats
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  nick_player TEXT, 
                  score INTEGER, 
                  coins INTEGER,
                  lvl1 INTEGER, money1 INTEGER, 
                  lvl2 INTEGER, money2 INTEGER, 
                  lvl3 INTEGER, money3 INTEGER, 
                  lvl4 INTEGER, money4 INTEGER, 
                  lvl5 INTEGER, money5 INTEGER, 
                  lvl6 INTEGER, money6 INTEGER)''')
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
