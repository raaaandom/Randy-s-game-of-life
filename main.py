# Importo pygame e lo inizializzo
import pygame
pygame.init()

# Importo math per calcoli matematici complessi
from math import floor

# Importo ctypes e creo user32 per comodita'
import ctypes
user32 = ctypes.windll.user32

# Importo os che mi serve per maneggiare file
import os

# Indice delle immagini
DEATH_IMAGE = 0
LIFE_IMAGE = 1

# Creo un array con le immagini
TOT_IMAGES = 10
images = [None] * TOT_IMAGES

images[DEATH_IMAGE] = pygame.image.load("assets/death.png")
images[LIFE_IMAGE] = pygame.image.load("assets/life.png")

# Creo la finestra
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 720

window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Randy's game of life")

# gestione telecamera
cameraPos_x = 0
cameraPos_y = 0
cameraSpeed = 20

# Creo la mappa di gioco
BOARD_WIDTH = 64
BOARD_HEIGHT = 45

board = [[0 for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]

# Creo la bufferboard
bufferBoard = [[0 for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]

# Definisco gli FPS e creo un clock
FPS = 30
clock = pygame.time.Clock()

# Funzione di rendering
BACKGROUND_COLOR = (0,0,0) #(rgb)
BORDER_COLOR = (255, 0, 0)
def renderBoard():
    window.fill(BACKGROUND_COLOR)
    for j in range(BOARD_HEIGHT):
        for i in range(BOARD_WIDTH):
            value = board[j][i]
            x = (WINDOW_WIDTH / BOARD_WIDTH) * i
            y = (WINDOW_HEIGHT / BOARD_HEIGHT) * j
            window.blit(images[value],(x + cameraPos_x, y + cameraPos_y))
    pygame.draw.rect(window, BORDER_COLOR, (0 + cameraPos_x, 0 + cameraPos_y, WINDOW_WIDTH, WINDOW_HEIGHT), 5)
    pygame.display.update()

# Creo una variabile che mi serve per esportare
nExport = 0

# Flag relativa agli eventi
isSimulationRunning_FLAG = False
isSimulationRunning = False
mouseLClick_Flag = False
mouseMClick_FLAG = False
mouseRClick_FLAG = False
singleStep_FLAG = False
export_FLAG = False

# Funzione di gestione eventi
def catchEvents():

    # Rendo visibili le variabili che mi servono ma che non sono state dichiarate dentro la funzione
    global isSimulationRunning_FLAG
    global isSimulationRunning
    global isGameRunning
    global singleStep_FLAG

    # Leggi tutti i tasti premuti
    keys = pygame.key.get_pressed()

    # Controllo tutti gli eventi
    for event in pygame.event.get():

        # Se la finestra deve essere chiusa esci dal main loop
        if event.type == pygame.QUIT:
            isGameRunning = False
        
        # Se un file sta venendo droppato sulla finestra importalo
        if not isSimulationRunning:
            if event.type == pygame.DROPFILE:
                
                path = event.file
                file = open(path)

                file_content = file.readlines()
                file_content_lines = len(file_content)

                for i in range(file_content_lines):
                    file_content[i] = file_content[i].replace("\n","")

                for y in range(BOARD_HEIGHT):
                    for x in range(BOARD_WIDTH):

                        board[y][x] = int(file_content[y][x])

    # Se spacebar e' premuto avvia / metti in pausa la simulazione
    if keys[pygame.K_SPACE] and not isSimulationRunning_FLAG:
        isSimulationRunning = not isSimulationRunning
        isSimulationRunning_FLAG = True

        # Prompto nella console varie cose:
        if isSimulationRunning:
            print("[STATUS] Simulation started.")
        else:
            print("[STATUS] Simulation stopped.")

    elif not keys[pygame.K_SPACE] and isSimulationRunning_FLAG:
        isSimulationRunning_FLAG = False

    # Se freccia destra e' premuta esegui solo una generazione
    if keys[pygame.K_RIGHT] and not singleStep_FLAG:
    
        if not isSimulationRunning:
            processBoard(1)
            print("[STATUS] Processed a single generation.")
        
        singleStep_FLAG = True
        
    elif not keys[pygame.K_RIGHT] and singleStep_FLAG:
        singleStep_FLAG = False

# Funzione che processa la tavola di gioco
def processBoard(arg=0):
    
    # Rendo visibili le variabili che mi servono ma che non sono state dichiarate dentro la funzione
    global isSimulationRunning

    # Se la simulazione non e' in corso ferma il processamento
    if not isSimulationRunning and arg == 0:
        return

    # Clono la board nella bufferboard
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            bufferBoard[y][x] = board[y][x]

    # Ciclo tutta la board
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            
            # Creo variabili che contano vita e morte attorno alla coordinata esaminata
            morte = 0
            vive = 0

            # Caso: Sinistra
            if x - 1 >= 0:
                if board[y][x - 1] == 0: morte += 1
                if board[y][x - 1] == 1: vive += 1

            # Caso: Destra
            if x + 1 <= BOARD_WIDTH - 1:
                if board[y][x + 1] == 0: morte += 1
                if board[y][x + 1] == 1: vive += 1
            
            # Caso: Sopra
            if y - 1 >= 0:
                if board[y - 1][x] == 0: morte += 1
                if board[y - 1][x] == 1: vive += 1

            # Caso: Sotto
            if y + 1 <= BOARD_HEIGHT - 1:
                if board[y + 1][x] == 0: morte += 1
                if board[y + 1][x] == 1: vive += 1

            # Caso: Sopra-Sinistra
            if x - 1 >= 0 and y - 1 >= 0:
                if board[y - 1][x - 1] == 0: morte += 1
                if board[y - 1][x - 1] == 1: vive += 1

            # Caso: Sopra-Destra
            if x + 1 <= BOARD_WIDTH - 1 and y - 1 >= 0:
                if board[y - 1][x + 1] == 0: morte += 1
                if board[y - 1][x + 1] == 1: vive += 1

            # Caso: Sotto-Sinistra
            if x - 1 >= 0 and y + 1 <= BOARD_HEIGHT - 1:
                if board[y + 1][x - 1] == 0: morte += 1
                if board[y + 1][x - 1] == 1: vive += 1

            # Caso: Sotto-Destra
            if x + 1 <= BOARD_WIDTH - 1 and y + 1 <= BOARD_HEIGHT - 1:
                if board[y + 1][x + 1] == 0: morte += 1
                if board[y + 1][x + 1] == 1: vive += 1

            # Se la cella e' viva...
            if board[y][x] == 1:

                # ... e ha meno di 2 vicini vivi muore
                if vive < 2:
                    bufferBoard[y][x] = 0
                    continue
                
                # ... e ha 2/3 vicini vivi soppravvive
                if vive == 2 or vive == 3:
                    continue

                # ... e ha piu' di 3 vicini vivi muore
                if vive > 3:
                    bufferBoard[y][x] = 0
                    continue
            
            # Se la cella e' morta...
            if board[y][x] == 0:

                # ... e ha esattamente 3 vicini rinasce
                if vive == 3:
                    bufferBoard[y][x] = 1
                    continue
    
    # Salvo la bufferboard nella board
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            board[y][x] = bufferBoard[y][x]

# Funzione editor della board
def editBoard():
    
    # Rendo visibili le variabili che mi servono ma che non sono state dichiarate dentro la funzione
    global isSimulationRunning
    global mouseLClick_Flag
    global mouseMClick_FLAG
    global mouseRClick_FLAG
    global export_FLAG
    global nExport
    global cameraPos_x
    global cameraPos_y

    # Se la simulazione e' in corso ferma il processamento
    if isSimulationRunning:
        return

    # Identifica i tasti del mouse premuti
    mouseKeys = pygame.mouse.get_pressed()
    keyboardKeys = pygame.key.get_pressed()

    # Se il bottone sinistro del mouse e' premuto crea una casella viva
    if mouseKeys[0] and not mouseLClick_Flag:
        mouseLClick_Flag = True

        x,y = pygame.mouse.get_pos()

        if (x-cameraPos_x > WINDOW_WIDTH) or (y-cameraPos_y > WINDOW_HEIGHT) or (x-cameraPos_x < 0) or (y-cameraPos_y < 0):
            pass
        else:
            i = (x-cameraPos_x)*(BOARD_WIDTH/WINDOW_WIDTH)
            j = (y-cameraPos_y)*(BOARD_HEIGHT/WINDOW_HEIGHT)

            i = floor(i)
            j = floor(j)

            board[j][i] = 1

            print("[EDITOR] Placed a life cell.")
    
    elif not mouseKeys[0] and mouseLClick_Flag:
        mouseLClick_Flag = False

    # Se il bottone centrale del mouse e' premuto elimina tutto
    if mouseKeys[1] and not mouseMClick_FLAG:
        mouseMClick_FLAG = True

        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                board[i][j] = 0

        print("[EDITOR] Cleared the board.")
    
    elif not mouseKeys[1] and mouseMClick_FLAG:
        mouseMClick_FLAG = False

    # Se il bottone destro del mouse e' premuto elimina la cella selezionata
    if mouseKeys[2] and not mouseRClick_FLAG:
        mouseRClick_FLAG = True

        x,y = pygame.mouse.get_pos()

        if (x-cameraPos_x > WINDOW_WIDTH) or (y-cameraPos_y > WINDOW_HEIGHT) or (x-cameraPos_x < 0) or (y-cameraPos_y < 0):
            pass
        else:
            i = (x-cameraPos_x)*(BOARD_WIDTH/WINDOW_WIDTH)
            j = (y-cameraPos_y)*(BOARD_HEIGHT/WINDOW_HEIGHT)

            i = floor(i)
            j = floor(j)

            board[j][i] = 0

            print("[EDITOR] Placed a death cell.")
    
    elif not mouseKeys[2] and mouseRClick_FLAG:
        mouseRClick_FLAG = False

    # Se il tasto E e' premuto esporta la tavola nella cartella exportedBoards
    if keyboardKeys[pygame.K_e] and not export_FLAG:
        export_FLAG = True

        nExport = len(os.listdir("exportedBoards/"))
        export = open(f"exportedBoards/{nExport}.rgol_export","w+")

        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):

                export.write(str(board[y][x]))
            export.write("\n")

        export.close()

        print(f"[EDITOR] Exported the board at \"exportedBoards/{nExport}.rgol_export\".")

    elif not keyboardKeys[pygame.K_e] and export_FLAG:
        export_FLAG = False

def cameraMovement():
    global cameraPos_x
    global cameraPos_y
    global cameraSpeed

    keyboardKeys = pygame.key.get_pressed()

    #Muovo la cam con wasd
    if keyboardKeys[pygame.K_a]:
        cameraPos_x += cameraSpeed
    if keyboardKeys[pygame.K_d]:
        cameraPos_x -= cameraSpeed
    if keyboardKeys[pygame.K_w]:
        cameraPos_y += cameraSpeed
    if keyboardKeys[pygame.K_s]:
        cameraPos_y -= cameraSpeed
    
    #reset della cam
    if keyboardKeys[pygame.K_r]:
        cameraPos_x = 0
        cameraPos_y = 0

# Funzione eseguita allo start
def onStartup():
    pass

# Chiamo la funzione eseguita allo start appena prima del mainloop
onStartup()

# Creo il mainloop
isGameRunning = True
while isGameRunning:

    # Limito il framerate
    clock.tick(FPS)

    # Esecuzione delle varie funzioni necessarie
    catchEvents()
    editBoard()
    processBoard()
    renderBoard()
    cameraMovement()

# Svuoto la memoria occupata dal programma
pygame.quit()