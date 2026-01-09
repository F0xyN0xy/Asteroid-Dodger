// ===== GLOBAL =====
let playerX = 2
let astX: number[] = []
let astY: number[] = []
let score = 0
let speed = 500
let running = false
let bossActive = false
let bossX = 0
let bossY = 0

// ===== DRAW =====
function draw() {
    basic.clearScreen()
    led.plot(playerX, 4)
    for (let i = 0; i < astX.length; i++) {
        led.plot(astX[i], astY[i])
    }
    if (bossActive) {
        // Boss als Quadrat
        led.plot(bossX, bossY)
        led.plot(bossX, Math.min(bossY + 1, 4))
        led.plot(Math.min(bossX + 1, 4), bossY)
        led.plot(Math.min(bossX + 1, 4), Math.min(bossY + 1, 4))
    }
}

// ===== STARTSCREEN =====
function showTitleScreen() {
    running = false
    basic.clearScreen()
    // Titelmusik
    music.playMelody("C5 B A G F E D C ", 120)
    basic.showString("A+B START")
}

input.onButtonPressed(Button.AB, function () {
    if (!running) startGame()
})

input.onButtonPressed(Button.A, function () {
    if (running && playerX > 0) playerX--
})

input.onButtonPressed(Button.B, function () {
    if (running && playerX < 4) playerX++
})

// ===== START GAME =====
function startGame() {
    playerX = 2
    score = 0
    speed = 600
    astX = [randint(0, 4), randint(0, 4)]
    astY = [0, -2]
    bossActive = false
    running = true
}

// ===== GAME OVER =====
function gameOver() {
    running = false
    basic.clearScreen()
    basic.showIcon(IconNames.Skull)
    music.playTone(175, music.beat(BeatFraction.Half))
    basic.pause(800)
    basic.showNumber(score)
    basic.pause(1500)
    showTitleScreen()
}

// ===== GAME LOOP =====
basic.forever(function () {
    if (!running) return

    // Asteroiden bewegen
    for (let i = 0; i < astX.length; i++) {
        astY[i]++

        // Collision
        if (astY[i] == 4 && astX[i] == playerX) {
            music.playTone(330, music.beat(BeatFraction.Quarter))
            gameOver()
            return
        }

        // Asteroid passiert
        if (astY[i] > 4) {
            astY[i] = 0
            astX[i] = randint(0, 4)
            score++
            music.playTone(440, music.beat(BeatFraction.Quarter))
            // Schwierigkeit erhöhen
            if (speed > 150) speed -= 10
            if (astX.length < 4 && score % 5 == 0) {
                astX.push(randint(0, 4))
                astY.push(0)
            }
            // Boss
            if (score % 10 == 0 && !bossActive) {
                bossActive = true
                bossX = randint(0, 3)
                bossY = 0
            }
        }
    }

    // Boss bewegen
    if (bossActive) {
        bossY++
        if (bossY >= 3) {
            if ((playerX == bossX || playerX == bossX + 1)) {
                music.playTone(220, music.beat(BeatFraction.Quarter))
                gameOver()
                return
            } else {
                bossActive = false
                score += 2
                music.playTone(880, music.beat(BeatFraction.Quarter))
            }
        }
    }

    draw()
    basic.pause(speed)
})

// ===== START =====
showTitleScreen()