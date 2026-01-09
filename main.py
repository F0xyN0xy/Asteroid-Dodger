# ===== GLOBAL =====
playerX = 2
astX: List[number] = []
astY: List[number] = []
score = 0
speed = 500
running = False
bossActive = False
bossX = 0
bossY = 0
# ===== DRAW =====
def draw():
    basic.clear_screen()
    led.plot(playerX, 4)
    for i in range(len(astX)):
        led.plot(astX[i], astY[i])
    if bossActive:
        # Boss als Quadrat
        led.plot(bossX, bossY)
        led.plot(bossX, min(bossY + 1, 4))
        led.plot(min(bossX + 1, 4), bossY)
        led.plot(min(bossX + 1, 4), min(bossY + 1, 4))
# ===== STARTSCREEN =====
def showTitleScreen():
    global running
    running = False
    basic.clear_screen()
    # Titelmusik
    music.play_melody("C5 B A G F E D C ", 120)
    basic.show_string("A+B START")

def on_button_pressed_ab():
    global running
    if not running:
        startGame()
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_a():
    global playerX
    if running and playerX > 0:
        playerX -= 1
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    global playerX
    if running and playerX < 4:
        playerX += 1
input.on_button_pressed(Button.B, on_button_pressed_b)

# ===== START GAME =====
def startGame():
    global playerX, score, speed, astX, astY, bossActive, running
    playerX = 2
    score = 0
    speed = 600
    astX = [randint(0, 4), randint(0, 4)]
    astY = [0, -2]
    bossActive = False
    running = True
# ===== GAME OVER =====
def gameOver():
    global running
    running = False
    basic.clear_screen()
    basic.show_icon(IconNames.SKULL)
    music.play_tone(175, music.beat(BeatFraction.HALF))
    basic.pause(800)
    basic.show_number(score)
    basic.pause(1500)
    showTitleScreen()
# ===== GAME LOOP =====

def on_forever():
    global running, score, speed, bossActive, bossX, bossY
    if not running:
        return
    # Asteroiden bewegen
    for j in range(len(astX)):
        astY[j] += 1
        # Collision
        if astY[j] == 4 and astX[j] == playerX:
            music.play_tone(330, music.beat(BeatFraction.QUARTER))
            gameOver()
            return
        # Asteroid passiert
        if astY[j] > 4:
            astY[j] = 0
            astX[j] = randint(0, 4)
            score += 1
            music.play_tone(440, music.beat(BeatFraction.QUARTER))
            # Schwierigkeit erhöhen
            if speed > 150:
                speed -= 10
            if len(astX) < 4 and score % 5 == 0:
                astX.append(randint(0, 4))
                astY.append(0)
            # Boss
            if score % 10 == 0 and not bossActive:
                bossActive = True
                bossX = randint(0, 3)
                bossY = 0
    # Boss bewegen
    if bossActive:
        bossY += 1
        if bossY >= 3:
            if (playerX == bossX or playerX == bossX + 1):
                music.play_tone(220, music.beat(BeatFraction.QUARTER))
                gameOver()
                return
            else:
                bossActive = False
                score += 2
                music.play_tone(880, music.beat(BeatFraction.QUARTER))
    draw()
    basic.pause(speed)
basic.forever(on_forever)

# ===== START =====
showTitleScreen()