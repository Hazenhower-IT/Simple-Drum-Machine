import pygame
from pygame import mixer
pygame.init()

width=1400
height=800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
light_gray = (170, 170, 170)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("HazeNDrum")
label_font = pygame.font.Font("freesansbold.ttf", 32)
medium_font = pygame.font.Font("freesansbold.ttf", 22)

index = 100
fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range (instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 1
beat_changed = True
save_menu = False
load_menu = False
saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    saved_beats.append(line)

beat_name = ""
typing = False
 
#load in sound
hi_hat = mixer.Sound("sounds\hihat.wav")
snare = mixer.Sound("sounds\snare.wav")
kick = mixer.Sound("sounds\kick.wav")
crash = mixer.Sound("sounds\crash.wav")
clap = mixer.Sound("sounds\clap.wav")
tom = mixer.Sound("sounds\\tom.wav")
pygame.mixer.set_num_channels(instruments * 6)


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:

            if i == 0:
                hi_hat.play()
            if i==1:
                snare.play()
            if i==2:
                kick.play()
            if i==3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()



def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, height-195], 5)
    bottom_box = pygame.draw.rect(screen, gray,[0, height-200, width, 200 ], 5)
    boxes=[]
    colors= [gray, white, gray]

    hi_hat_text = label_font.render("Hi Hat", True, colors[actives[0]] )
    screen.blit(hi_hat_text, (30, 30))

    snare_text = label_font.render("Snare", True, colors[actives[1]])
    screen.blit(snare_text, (30, 130))

    kick_text = label_font.render("Kick", True, colors[actives[2]])
    screen.blit(kick_text, (30, 230))

    crash_text = label_font.render("Crash", True, colors[actives[3]])
    screen.blit(crash_text, (30, 330))

    clap_text = label_font.render("Clap", True, colors[actives[4]])
    screen.blit(clap_text, (30, 430))

    tom_text = label_font.render("Tom", True, colors[actives[5]])
    screen.blit(tom_text, (30, 530))

    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (200, (i * 100) + 100), 3)

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray

            rect = pygame.draw.rect(screen, color, [i * ((width - 200) // beats) + 205, (j*100) +5,
                                                    ((width - 200) // beats) - 10, ((height-200)//instruments)- 10 ], 0, 3)
            
            pygame.draw.rect(screen, gold, [i * ((width - 200) // beats) + 200, (j*100),
                                                    ((width - 200) // beats), ((height-200)//instruments) ], 5, 5)
            
            pygame.draw.rect(screen, black, [i * ((width - 200) // beats) + 200, (j*100),
                                                    ((width - 200) // beats), ((height-200)//instruments) ], 2, 5)
            
            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, blue, [beat * ((width - 200) // beats) + 200 , 0, ((width - 200) // beats), instruments * 100 ], 5, 3)

    return boxes


# SAVE MENU
def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, black, [0, 0, width, height])
    menu_text = label_font.render("SAVE MENU: Enter A Name For The Current Beat", True, white)
    saving_btn = pygame.draw.rect(screen, gray, [width//2 - 200, height * 0.75, 400, 100], 0, 5)
    saving_txt = label_font.render("Save Beat", True, white)
    screen.blit(saving_txt, (width // 2 - 70, height * 0.75 + 30))
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(screen, gray, [width-200, height-100, 180, 90], 0, 5)
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (width-160, height-70))
    if typing:
        entry_rect = pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, gray, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430, 250))
    return exit_btn, saving_btn, entry_rect


# LOAD MENU
def draw_load_menu(index):
    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    pygame.draw.rect(screen, black, [0, 0, width, height])

    menu_text = label_font.render("LOAD MENU: Select A Beat To Load", True, white)

    loading_btn = pygame.draw.rect(screen, gray, [width//2 - 200, height * 0.87, 400, 100], 0, 5)
    loading_txt = label_font.render("Load Beat", True, white)
    screen.blit(loading_txt, (width // 2 - 70, height * 0.87 + 30))

    delete_btn = pygame.draw.rect(screen, gray, [(width // 2) - 500, height * 0.87, 200, 100 ], 0, 5)
    delete_text = label_font.render("Delete Beat", True, white)
    screen.blit(delete_text, ((width // 2) - 495, height * 0.87 +30 ))
    
    screen.blit(menu_text, (400, 40))

    exit_btn = pygame.draw.rect(screen, gray, [width-200, height-100, 180, 90], 0, 5)
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (width-160, height-70))

    loaded_rectangle = pygame.draw.rect(screen, gray, [ 190, 90, 1000, 600], 5, 5)

    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, light_gray, [190, 90 + index * 50, 1000, 50])

    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            
            #RETTANGOLO CHE MOSTRA I BEAT SALVATI
            row_text = medium_font.render(f"{beat +1}", True, white)
            screen.blit(row_text, (200, 100 + beat * 50))
            
            #LOGICA PER RIPRENDERE IL NOME DEI BEAT E MOSTRARLI A SCHERMO
            name_index_start = saved_beats[beat].index("name: ") + 6
            name_index_end = saved_beats[beat].index(", beats:")
            name_text = medium_font.render(saved_beats[beat][name_index_start : name_index_end], True, white)
            screen.blit(name_text, (240, 100 + beat * 50))

        #LOGICA PER RIPRENDERE IL NUMERO DEI PATTERN(BEAT) E MOSTRARLI A SCHERMO
        if 0 <= index < len(saved_beats) and beat == index:
            beat_index_end = saved_beats[beat].index(", bpm:")
            loaded_beats = int(saved_beats[beat][name_index_end+8 : beat_index_end])

            #LOGICA PER RIPRENDERE IL NUMERO DI BPM E MOSTRARLI A SCHERMO
            bpm_index_end = saved_beats[beat].index(", selected:")
            loaded_bpm = int(saved_beats[beat][beat_index_end + 6 : bpm_index_end])

            #LOGICA PER RIPRENDERE I PATTERN ATTIVI NELLA TRACCIA CARICATA
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14 : -3]
            loaded_clicks_rows = list(loaded_clicks_string.split("], ["))

            #CARICARE I PATTERN ATTIVI QUANDO SI FA IL LOAD DEL PROPRIO BEAT
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(", "))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == "1" or loaded_clicks_row[item] == "-1":
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])

                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked


    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    return exit_btn, loading_btn, delete_btn, loaded_rectangle, loaded_info


run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat, active_list)

    #Lower Menu Buttons
    play_pause = pygame.draw.rect(screen, gray, [50, height-150, 200, 100], 0 , 5 )
    play_text = label_font.render("Play/Pause", True, white)
    screen.blit(play_text, (70, height-130))

    if playing:
        play_text2= medium_font.render("Playing", True, dark_gray)
    else:
        play_text2 = medium_font.render("Paused", True, dark_gray)
    screen.blit(play_text2, (70, height - 100))

    #BPM Stuff
    bpm_rect = pygame.draw.rect(screen, gray, [300, height- 150, 200, 100], 5, 5)

    bpm_text = medium_font.render("Beats Per Minute", True, white)
    screen.blit(bpm_text, (308, height-130))

    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (370, height-100))

    bpm_add_rect = pygame.draw.rect(screen, gray, [510, height - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [510, height - 100, 48, 48], 0, 5)
    add_text = medium_font.render("+5", True, white)
    sub_text = medium_font.render("-5", True, white)
    screen.blit(add_text, (520, height - 140)) 
    screen.blit(sub_text, (520, height - 90 ))


    #Beats Stuff
    beats_rect = pygame.draw.rect(screen, gray, [600, height- 150, 200, 100], 5, 5)

    beats_text = medium_font.render("Beats in Loop", True, white)
    screen.blit(beats_text, (628, height-130))

    beats_text2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (690, height-100))

    beats_add_rect = pygame.draw.rect(screen, gray, [810, height - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [810, height - 100, 48, 48], 0, 5)
    add_text2 = medium_font.render("+1", True, white)
    sub_text2 = medium_font.render("-1", True, white)
    screen.blit(add_text2, (820, height - 140)) 
    screen.blit(sub_text2, (820, height - 90 ))

    #INSTRUMENT RECTS (PER ACCENDERE E SPEGNERE STRUMENTI SINGOLARMENTE)
    instrument_rects = []
    for  i in range(instruments):
        rect = pygame.rect.Rect((0, i*100), (200,100))
        instrument_rects.append(rect)

    # SAVE AND LOAD STUFF
    save_button = pygame.draw.rect(screen, gray, [900, height-150, 200, 48], 0, 5)
    save_text = label_font.render("Save Beat", True, white)
    screen.blit(save_text, (920, height-140))
    load_button = pygame.draw.rect(screen, gray, [900, height-100, 200, 48], 0, 5)
    load_text = label_font.render("Load Beat", True, white)
    screen.blit(load_text, (920, height-90))

    #CLEAR BOARD
    clear_button = pygame.draw.rect(screen, gray, [1150, height-150, 200, 100], 0, 5)
    clear_text = label_font.render("Clear All", True, white)
    screen.blit(clear_text, (1180, height - 120))

    #SAVE AND LOAD MENU
    if save_menu:
        exit_button, saving_button, entry_rectangle = draw_save_menu(beat_name, typing)
    if load_menu:
        exit_button, loading_button, delete_button, loaded_rectangle, loaded_info = draw_load_menu(index)

    #OGNI VOLTA CHE IL BEAT VA AVANTI DI 1 POSIZIONE, SUONA I PATTERN CORRISPONDENTI
    if beat_changed:
        play_notes()
        beat_changed = False

    # CONTROLLA OGNI EVENTO IN PYGAME
    for event in pygame.event.get():
        
        #SE IL TIPO DI EVENTO è QUIT, CHIUDE L'APPLICAZIONE
        if event.type == pygame.QUIT:
            run = False

        #SE VIENE CLICCKATO IL MOUSE 
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:

            #LOGICA PER ATTIVARE I PULSANTI CONTENENTI I SUONI
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1

        # SE RILASCIO IL BOTTONE DEL MUOSE( UTILE PER EVENTI CHE VANNO CLICCKATI UNA SINGOLA VOLTA COME APPUNTO PAUSA)
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:

            # PLAY/PAUSE LOGIC
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True

            # LOGICA AGGIUNTA O RIMOZIONE BPM
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5

                
            #LOGICA AGGIUNTA O RIMOZIONE BEATS (PANNELLI DA SELEZIONARE PER SUONARE)
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)

            #LOGICA PER IL BOTTONE CHE RESETTA TUTTI I PATTERN
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range (instruments)]

            #LOGICA PER L'APERTURA E CHIUSURA DEL SAVE MENU E LOAD MENU
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True

            #LOGICA PER ACCENDERE O SPEGNERE STRUMENTI SINGOLARMENTE
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1

        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name = ""
                typing = False

            if load_menu:    
                if loaded_rectangle.collidepoint(event.pos):
                    index = (event.pos[1] - 100) // 50

                #LOGICA DEL BOTTONE PER ELIMINARE UN BEAT
                if delete_button.collidepoint(event.pos):
                    if 0 <= index <  len(saved_beats):
                        saved_beats.pop(index)

                #LOGICA DEL BOTTONE PER CARICARE IL BEAT
                if loading_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        beats = loaded_info[0]
                        bpm = loaded_info[1]
                        clicked = loaded_info[2]
                        index = 100
                        load_menu = False

            if save_menu:                
                if entry_rectangle.collidepoint(event.pos):
                    if typing :
                        typing = False
                    elif not typing:
                        typing = True
                if saving_button.collidepoint(event.pos):
                    file = open("saved_beats.txt", "w")
                    saved_beats.append(f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}')
                    for i in range(len(saved_beats)):
                        file.write(str(saved_beats[i]))
                    file.close()
                    save_menu = False
                    typing = False
                    beat_name = ""
        
        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name)>0 and typing:
                beat_name = beat_name[:-1]


    #LUNGHEZZA DEL BEAT E CIOE 3600 (CIOE I 60 FRAME AL SECONDO, MOLTIPLICATI PER I SECONDI IN UN MINUTO (CIOE 60 X 60 = 3600), DIVISO IL NUMERO DI BPM ATTUALI
    beat_length = 3600 // bpm

    #LOGICA PER FAR "SCORRERE" IL PLAYER E QUINDI SUONARE LA DRUM MACHINE, E TORNARE ALL'INIZIO QUANDO ARRIVA A FINE BEAT
    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True


    pygame.display.flip()
pygame.quit()