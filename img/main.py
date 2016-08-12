# Pygame Template.
import pygame as pg
import math
import random
import settings
from os import path
import sys









# Handling of directories
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
pharos_dir = path.join(path.dirname(__file__), 'pharos8')
pharos_dir2 = path.join(path.dirname(__file__), 'pharoswin')
dir = path.dirname(__file__)






# Settings variables
width = 480
height = 600
fps = 60
powerup_time = 5000
earth_scale = 1
approaching_val = 50000000







# Colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
yellow = (255,255,0)
blue = (9,5,38) # Pharos blue







# FUNCTION DEFINITIONS
font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)





def newmob():
    m = Mob()
    allsprites.add(m)
    mobs.add(m)





def draw_shield_bar(surface, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct/100) * bar_length
    outline_rect = pg.Rect(x, y, bar_length, bar_height)
    fill_rect = pg.Rect(x, y, fill, bar_height)
    pg.draw.rect(surface, green, fill_rect)
    pg.draw.rect(surface, white, outline_rect,2)







def draw_lives(surface, x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y =y
        surface.blit(img, img_rect)


# Player sprite
class Player(pg.sprite.Sprite):
    def __init__(self):
        self._layer = 1
        self.groups = allsprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image_orig = space_ship
        self.image = self.image_orig.copy()
        self.rect = space_ship.get_rect()
        self.radius = 27
        #pg.draw.circle(space_ship, red, self.rect.center, self.radius)
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()


        self.rect.x = width/2
        self.rect.y = height/2
        self.speedx = 0
        self.speedy = 0
        self.last = 0
        self.shield = 100
        self.mylives = 3 # Amount of lives that the player has
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        # For powerupgun
        self.power = 1
        self.power_time = pg.time.get_ticks()




    def update(self):
        # Timeout for powerups
        if self.power >= 2 and pg.time.get_ticks() - self.power_time > powerup_time:
            self.power -= 1
            self.power_time = pg.time.get_ticks()
        if self.power == 1:
            self.shoot_delay = 300
        else:
            self.shoot_delay = 400
        # Unhide if hidden for respawns
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 300:
            self.hidden = False
            self.rect.centerx = width/2
            self.rect.centery = height/2

        pos = pg.mouse.get_pos()
        # Function calls
        self.rotater(self.rect.centerx, self.rect.centery, space_ship, pos)

        self.Reticle(pos)
        self.speedx = 0 # To stop the player if no keys are pressed
        self.speedy = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]: # Left
            self.speedx = -4
        if keystate[pg.K_d]: # Right
            self.speedx = 4
        if keystate[pg.K_w]: # Up
            self.speedy = -4
        if keystate[pg.K_s]: # Down
            self.speedy = 4
        if keystate[pg.K_f]:
            self.shoot()
        # For actual movement
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Boundries / Constraints
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height


    # For player rotation and drawing to the screen
    def rotater(self, x, y, image, mousePos):
        now = pg.time.get_ticks()
        angle = 360 - math.atan2(mousePos[1] - y, mousePos[0] - x) * 180 / math.pi  # Get params
        angle = angle - 90
        rotimage = pg.transform.rotate(self.image_orig, angle)
        old_center = self.rect.center



        cursorRect = cursor.get_rect()
        self.image = rotimage
        self.rect = self.image.get_rect()
        self.rect.center = old_center



    # Handling of mouse image
    def Reticle(self, mousePos):
        now = pg.time.get_ticks()
        if settings.hits2bool == True:
            pos1 = mousePos[0] - 25
            pos2 = mousePos[1] - 25
            cursor1 = cursorhit
            screen.blit(cursor1, (pos1, pos2))
            hit_sound.play()
            hit_sound.set_volume(0.15)
        else:
            pos1 = mousePos[0] - 75
            pos2 = mousePos[1] - 75
            cursor1 = cursor
            screen.blit(cursor1, (pos1, pos2))








    def powerup(self):
        self.power += 1
        self.power_time = pg.time.get_ticks()












    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                pos = pg.mouse.get_pos()
                bullet = Bullet(pos, [self.rect.x, self.rect.y], [self.rect.centery, self.rect.centerx])
                allsprites.add(bullet)
                bullets.add(bullet)
                angle = 360 - math.atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx) * 180 / math.pi
                angle = angle - 90
                rotimage = pg.transform.rotate(blt, angle)
                bullet.image = rotimage
                random.choice(blaster_sounds).play()
                random.choice(blaster_sounds).set_volume(0.05)
            if self.power >= 2:
                pos = pg.mouse.get_pos()
                bullet1 = Bullet(pos, [self.rect.x, self.rect.y], [self.rect.centery, self.rect.centerx])
                allsprites.add(bullet1)
                bullets.add(bullet1)
                angle = 360 - math.atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx) * 180 / math.pi
                angle = angle - 90
                rotimage = pg.transform.rotate(blt2, angle)
                bullet1.image = rotimage
                redblast_sound.play()
                redblast_sound.set_volume(0.05)
        else:
            pass
    def hide(self):
        # Hide the player temporariliy
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (width/2,height+200)


class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image = self.image_orig.copy()
        #self.image.fill(red)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/ 2)
        #pg.draw.circle(self.image, red, self.rect.center, self.radius)
        # Spawn position
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last = pg.time.get_ticks()
    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last > 50:
            self.last = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height + 10:
            self.rect.x = random.randrange(0, width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 20)
        if self.rect.left < -25: #bottom
            self.rect.x = random.randrange(width/4,width)
            self.rect.y = (height + 10)
            self.speedy = random.randrange(-20, 0)
        if self.rect.right > width + 20: # right
            self.rect.x = random.randrange(width, width+20)
            self.rect.y = (height/2)
            self.speedy = random.randrange(-10, 10)
            self.speedx = -10



class Bullet(pg.sprite.Sprite):
    def __init__(self, mouse, player, playerpos):
        pg.sprite.Sprite.__init__(self)
        self.image = placeholder
        self.mouse_x, self.mouse_y = mouse[0], mouse[1]
        self.player = player
        self.rect = self.image.get_rect()
        # For better collison
        self.rect.width = 30
        self.rect.height = 80
        self.rect.x = playerpos[1] - 37
        self.rect.y = playerpos[0] - 60
        self.rect1 = space_ship.get_rect()



    def update(self):




        speed = -24.
        range = 200
        distance = [self.mouse_x - self.player[0], self.mouse_y - self.player[1]]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1] / norm]
        bullet_vector = [direction[0] * speed, direction[1] * speed]
        self.rect.x -= bullet_vector[0]
        self.rect.y -= bullet_vector[1]
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top> height:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > width:
            self.kill()
class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 75
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5



    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height:
            self.kill()

class Earth(pg.sprite.Sprite):
    def __init__(self):
        self._layer = 0
        self.groups = allsprites, earthg
        pg.sprite.Sprite.__init__(self, self.groups)
        self.scale = 1
        self.image = pg.transform.scale(earth, (self.scale,self.scale))

        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.centery= height/2
        self.last = 0




    def update(self):

        # earth1 = Earth(1)
        # allsprites.add(earth1)
        self.time = pg.time.get_ticks()
        self.time = 1497346065880 - int(self.time / 10)
        self.time = self.time - (score * 50000000)  # Take away a zero from here.
        now = pg.time.get_ticks()


        if len(str(self.time)) == 13:
            if now - self.last > 500 and self.scale <= 50:
                self.last = now
                self.scale += 1
                self.image = pg.transform.scale(earth, (self.scale, self.scale))
                self.rect = self.image.get_rect()
                self.rect.centerx = width / 2
                self.rect.centery = height / 2
        if len(str(self.time)) == 12:

            if now - self.last > 500 and self.scale <= 100:
                self.last = now
                self.scale += 1
                self.image = pg.transform.scale(earth, (self.scale, self.scale))
                self.rect = self.image.get_rect()
                self.rect.centerx = width / 2
                self.rect.centery = height / 2
        if len(str(self.time)) == 11:

            if now - self.last > 500 and self.scale <= 150:
                self.last = now
                self.scale += 1
                self.image = pg.transform.scale(earth, (self.scale, self.scale))
                self.rect = self.image.get_rect()
                self.rect.centerx = width / 2
                self.rect.centery = height / 2
        if len(str(self.time)) == 10:

            if now - self.last > 500 and self.scale <= 200:
                self.last = now
                self.scale += 1
                self.image = pg.transform.scale(earth, (self.scale, self.scale))
                self.rect = self.image.get_rect()
                self.rect.centerx = width / 2
                self.rect.centery = height / 2




# Generic definitions
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((width,height))
pg.display.set_caption("pharos game")
clock = pg.time.Clock()
#Load sound
hit_sound = pg.mixer.Sound(path.join(snd_dir,'hitmarker.ogg'))
blast_sound = pg.mixer.Sound(path.join(snd_dir,'blast.ogg'))
blast_sound2 = pg.mixer.Sound(path.join(snd_dir,'blast2.ogg'))
redblast_sound = pg.mixer.Sound(path.join(snd_dir,'blaster2powerup.ogg'))
explosion_sound = pg.mixer.Sound(path.join(snd_dir,'expl.ogg'))
player_death = pg.mixer.Sound(path.join(snd_dir,'rumble1.ogg'))
powerup_sound = pg.mixer.Sound(path.join(snd_dir,'powerup.ogg'))
powerup_sound2 = pg.mixer.Sound(path.join(snd_dir,'powerup2.ogg'))

#pg.mixer.music.set_volume(2)
blaster_sounds = []
for snd in ['blast.ogg','blast2.ogg']:
    blaster_sounds.append(pg.mixer.Sound(path.join(snd_dir,snd)))


# Load images
space_ship = pg.image.load(path.join(img_dir,'ship.png')).convert_alpha()
space_ship = pg.transform.scale(space_ship, (70, 80))
pharosend = pg.image.load(path.join(img_dir,'pharosend.png')).convert_alpha()

blt = pg.image.load(path.join(img_dir,'bullet.png')).convert_alpha()
blt = pg.transform.scale(blt, (70, 80))
blt2 = pg.image.load(path.join(img_dir,'bullet2.png')).convert_alpha()
blt2 = pg.transform.scale(blt2, (70, 80))
placeholder = pg.image.load(path.join(img_dir,'placeholder.png')).convert_alpha()
cursor = pg.image.load(path.join(img_dir,'cursorimg.png')).convert_alpha()
cursorhit = pg.image.load(path.join(img_dir,'cursorimghit.png')).convert_alpha()
cursorhit = pg.transform.scale(cursorhit, (50, 50))
bg = pg.image.load(path.join(img_dir,'1.jpg')).convert_alpha()
bg = pg.transform.scale(bg, (width, height))
bg_rect = bg.get_rect()
dmg = pg.image.load(path.join(img_dir,'damage.png')).convert_alpha()
dmg = pg.transform.scale(dmg, (width, height))
signal = pg.image.load(path.join(img_dir,'signal.png')).convert_alpha()
signal = pg.transform.scale(signal, (56, 56))
#hud = pg.image.load(path.join(img_dir,'hud.png')).convert_alpha()
#hud = pg.transform.scale(hud, (width, height))
lives = pg.image.load(path.join(img_dir,'lives.png')).convert_alpha()
lives = pg.transform.scale(lives, (80, 80))
# The earth
earth = pg.image.load(path.join(img_dir,'earth.png')).convert_alpha()
# For power ups
powerup_images = {}
powerup_images['shield'] = pg.image.load(path.join(img_dir,'powerup2.png')).convert_alpha()
powerup_images['gun'] = pg.image.load(path.join(img_dir,'powerup.png')).convert_alpha()
loadingimg = pg.image.load(path.join(img_dir,'pharoslogo.png')).convert_alpha()
loadingimg  = pg.transform.scale(loadingimg , (450, 350))
coderimg = pg.image.load(path.join(img_dir,'coder.png')).convert_alpha()
coderimg = pg.transform.scale(coderimg , (200, 40))
pharostitle = pg.image.load(path.join(img_dir,'pharostitle.png')).convert_alpha()



# For meteors
meteor_images = []
meteor_list =['asteroid.png','meteorBrown_big1.png','meteorBrown_big2.png',
              'meteorBrown_big3.png','meteorBrown_big4.png','meteorBrown_med1.png','meteorBrown_small1.png',
              'meteorBrown_small2.png','meteorBrown_tiny1.png','meteorBrown_tiny2.png']
for img in meteor_list:
    meteor_images.append(pg.image.load(path.join(img_dir, img)).convert_alpha())
pos = pg.mouse.get_pos()
# Load end sequence stuff
end_images = []
end_list = []
y = 0
while y <= 30:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    pg.event.clear()
    pg.event.set_blocked(pg.MOUSEMOTION)
    pg.event.set_blocked(pg.MOUSEBUTTONDOWN)
    pg.event.set_blocked(pg.MOUSEBUTTONUP)

    pg.mouse.set_visible(False)

    y += 1
    val = str(y)
    if len(val) == 1:
        val = '0' + val
    if len(val) == 2:
        val = val
    file = 'vid ' + str(val) + '.jpg'
    end_list.append(file)
    draw_text(screen, "Initiating..", 13, width - 75, height - 85)
    pg.display.flip()
for img in end_list:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    pg.event.clear()
    pg.event.set_blocked(pg.MOUSEMOTION)
    pg.event.set_blocked(pg.MOUSEBUTTONDOWN)
    pg.event.set_blocked(pg.MOUSEBUTTONUP)

    pg.mouse.set_visible(False)

    myimage = pg.image.load(path.join(pharos_dir2, img)).convert_alpha()
    myimage = pg.transform.scale(myimage, (width, height))
    end_images.append(myimage)
    screen.fill(black)
    draw_text(screen, "Initiating...", 13, width - 75, height - 85)
    pg.display.flip()




explosion_anim ={}
explosion_anim['lg'] = []
explosion_anim['sm'] =[]
explosion_anim['player1'] = []






for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pg.image.load(path.join(img_dir, filename))
    img_lg = pg.transform.scale(img, (75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pg.transform.scale(img, (32,32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pg.image.load(path.join(img_dir, filename))
    explosion_anim['player1'].append(img)

# Background images
bg_images = []
background_list = []
#pharosloop2 001
x = 0


pg.mixer.music.load(path.join(snd_dir, 'loadingtheme.ogg'))
pg.mixer.music.play(loops=-1)
while x < 266:

    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    pg.event.clear()
    pg.event.set_blocked(pg.MOUSEMOTION)
    pg.event.set_blocked(pg.MOUSEBUTTONDOWN)
    pg.event.set_blocked(pg.MOUSEBUTTONUP)

    pg.mouse.set_visible(False)


    x += 1
    val = str(x)
    if len(val) == 1:
        counter = '00' + val
    if len(val) == 2:
        counter = '0' + val
    if len(val) == 3:
        counter = val
    file= 'pharosloop2 ' + str(counter) + '.jpg'
    background_list.append(file)
    percent = (int(val)/266) * 50
    percent = int(percent)
    percent = str(percent)



    screen.fill(black)
    screen.blit(coderimg, (width/2-110, height/2 -50))

    draw_text(screen, "LOADING: " + percent +"%", 13, width- 75, height-85)
    pg.display.flip()


#background_list.append(pg.image.load(path.join(pharos_dir, file)).convert_alpha())

val =0
for img in background_list:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    pg.event.clear()
    pg.event.set_blocked(pg.MOUSEMOTION)
    pg.event.set_blocked(pg.MOUSEBUTTONDOWN)
    pg.event.set_blocked(pg.MOUSEBUTTONUP)

    pg.mouse.set_visible(False)
    val += 1
    img = pg.image.load(path.join(pharos_dir, img)).convert_alpha()
    img = pg.transform.scale(img, (width, height))
    bg_images.append(img)

    percent = 50 + (int(val)/266) * 50
    percent = int(percent)
    percent = str(percent)





    screen.fill(black)
    screen.blit(loadingimg, (width/2-240, 0))
    draw_text(screen, "A spaceman, awoken after being cryogenically frozen due to his spaceship malfunctioning wants to return home.", 11, width/2, height - 155)
    draw_text(screen, "It is now the year 3005. Is there life still on earth?", 13, width/2, height - 145)
    draw_text(screen, "Is he all alone? Help him to return home.", 13, width/2, height - 135)
    draw_text(screen, "LOADING: " + percent +"%", 13, width- 75, height-85)
    pg.display.flip()

# Load ending sequence stuff

# Screens
def show_go_screen():




    pg.mixer.music.load(path.join(snd_dir, 'gameover.ogg'))
    pg.mixer.music.play(loops=-1)
    screen.fill(black)
    with open(path.join(dir, 'highscore.txt'), 'w') as file:
        try:
            highscore = int(f.read())
        except:
            highscore = 0

    draw_text(screen, "GAME OVER", 64, width/2, height/4)
    draw_text(screen, "PRESS P KEY TO TRY AGAIN", 18, width/2, height*0.75)
    if score > highscore:
        highscore = score
        draw_text(screen, "NEW HIGH SCORE! " + str(highscore), 22,width / 2, height / 2 + 90)
        with open(path.join(dir, 'highscore.txt'), 'w') as file:
            file.write(str(score))
    else:
        draw_text(screen, "High score: " + str(highscore), 22,width / 2, height / 2 + 90)
    pg.display.flip()
    waiting = True






    while waiting:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:

                    waiting = False
def show_title_screen():
    pg.mixer.music.load(path.join(snd_dir, 'startscreen.ogg'))
    pg.mixer.music.play(loops=-1)
    screen.blit(pharostitle, (0, 0))
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False

def show_end_sequence():
    clock.tick(fps)
    last2 = 0
    last3 = 0
    current_frame = 0
    pg.mixer.music.load(path.join(snd_dir, 'PharosEngingSequence.ogg'))
    pg.mixer.music.play(loops=0)

    waiting = True
    waiting2 = False
    while waiting:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                waiting = False
        now = pg.time.get_ticks()
        if now - last2 > 50:

            last2 = now
            current_frame = (current_frame + 1) % len(end_images)
            screen.blit(end_images[current_frame], (0, 0))
            pg.display.flip()
        if current_frame == 30:
            waiting = False
            waiting2 = True
    while waiting2:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting2 = False
                pg.quit()


        screen.fill(white)
        if pg.mixer.music.get_busy() == False:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting2 = False
                    pg.quit()

            screen.blit(pharosend, (0, 0))
        pg.display.flip()


#Cursors
pg.mouse.set_visible(False)
show_title_screen()
pg.mixer.music.load(path.join(snd_dir, 'pharosgameaudio.ogg'))
pg.mixer.music.play(loops=-1)
# Game loop

game_over = False
game_won = True
allsprites = pg.sprite.LayeredUpdates()
mobs = pg.sprite.Group()
bullets = pg.sprite.Group()
powerups = pg.sprite.Group()
earthg = pg.sprite.Group()
e = Earth()
allsprites.add(e)
earthg.add(e)

player1 = Player()
allsprites.add(player1)

for i in range(10):
    newmob()
# Scoress
score = 0

running = True
gamewon = False
last = 0
current_frame = 0
while running:
    if game_over:
        show_go_screen()
        game_over = False
        pg.mixer.music.load(path.join(snd_dir, 'pharosgameaudio.ogg'))
        pg.mixer.music.play(loops=-1)
        allsprites = pg.sprite.LayeredUpdates()
        mobs = pg.sprite.Group()
        bullets = pg.sprite.Group()
        powerups = pg.sprite.Group()
        earthg = pg.sprite.Group()
        e = Earth()
        allsprites.add(e)
        earthg.add(e)

        player1 = Player()
        allsprites.add(player1)

        for i in range(10):
            newmob()
        # Scoress
        score = 0





    # Process events
    time = pg.time.get_ticks()

    clock.tick(fps)
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False



    # Update
    now = pg.time.get_ticks()
    if now - last > 15:
        last = now
        current_frame = (current_frame + 1) % len(bg_images)
    screen.blit(bg_images[current_frame], (0,0))


    allsprites.update()
    # Hit checking / Update
    # Sprite to check, w/ a group...
    # Check to see if bullet hit mob (group to group)  mob and bullet gets deleted
    if player1.power == 1:
        hits2 = pg.sprite.groupcollide(mobs, bullets, True, True)
    if player1.power >= 2:
        hits2 = pg.sprite.groupcollide(mobs, bullets, True, False)

    if hits2:
        explosion_sound.play()
        for hits in hits2:
            if hits.radius > 40:
                explosion_sound.set_volume(0.1)
            if hits.radius > 20 and hits.radius < 40:
                explosion_sound.set_volume(0.05)
            if hits.radius < 20:
                explosion_sound.set_volume(0.02)


        settings.hits2bool = True
    else:
        settings.hits2bool = False



    for hit in hits2: # For every sprite dead, spawn new ones
        score += 50 - hit.radius
        if hits.radius > 40:
            expl = Explosion(hit.rect.center, 'lg')
        if hits.radius > 20 and hits.radius < 40:
            expl = Explosion(hit.rect.center, 'lg')
        if hits.radius < 20:
            expl = Explosion(hit.rect.center, 'sm')

        allsprites.add(expl)
        if random.random() > 0.8:
            pow = Pow(hit.rect.center)
            allsprites.add(pow)
            powerups.add(pow)
        newmob()


    # Check to see if player hit mob (sprite to group)
    hits = pg.sprite.spritecollide(player1, mobs, True, pg.sprite.collide_circle) # List w/ hit mobssssssssssssssssssssss


    for hit in hits: # If hits has something in it
        player1.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        allsprites.add(expl)
        newmob()
        screen.blit(dmg, (0, 0))
        if player1.shield < 0:
            player_death.play()
            death_explosion = Explosion(player1.rect.center, 'player1')
            allsprites.add(death_explosion)
            player1.hide()
            player1.mylives -= 1
            player1.shield = 100
    # Check player hit powerup



    hits = pg.sprite.spritecollide(player1, powerups, True)
    for hits in hits:
        if hits.type == 'shield':
            score += 500
            if player1.shield != 100:
                powerup_sound.play()
                powerup_sound.set_volume(0.1)
            player1.shield += random.randrange(10, 30)
            if player1.shield >= 100:
                player1.shield = 100
        if hits.type == 'gun':
            score += 500
            powerup_sound2.play()
            powerup_sound2.set_volume(0.1)
            player1.powerup()
    # If player died and explosion finished
    if player1.mylives == 0 and not death_explosion.alive():
        game_over = True







    # Draw moved to where rotate is

    allsprites.draw(screen)
    #screen.blit(hud, (0, 0))

    draw_text(screen, "SCORE: " + str(score), 18, width/2, 10)

    #Flip
    time = pg.time.get_ticks()

       # earth1 = Earth(1)
        #allsprites.add(earth1)

    time  = 1497346065880 - int(time/10)
    # To lengthen game time
    if len(str(time)) == 12:
        approaching_val /= 4
    if len(str(time)) == 11:
        approaching_val /= 5
    if len(str(time)) == 10:
        approaching_val /= 6
    if len(str(time)) == 9:
        approaching_val /= 7
    if len(str(time)) == 6:
        approaching_val /= 8





    time = time - (score * approaching_val) # Take away a zero from here.
    draw_text(screen, "APPROACHIN", 13, width- 75, height-85)
    draw_text(screen, str(time) + " Φę", 25, width-120, height-65)
    if time <= 0: #<=
        gamewon = True
        running = False


    draw_shield_bar(screen, 30, 20, player1.shield)
    screen.blit(signal, (0, 0))
    draw_text(screen, "SIGNAL STRENGTH", 10, 93, 7)
    draw_text(screen, "LIVES", 15, width-90, 7)
    draw_lives(screen, width - 160, 5, player1.mylives, lives)
    pg.display.flip()
if gamewon == True:
    show_end_sequence() # Show ending game sequence
    #end_images
    pg.quit()
else:
    pg.quit()

# End the game