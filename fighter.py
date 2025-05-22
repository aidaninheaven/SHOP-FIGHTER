import pygame

#from projectiles import Projectile

class Fighter():
    
    def __init__(self, player, x, y, flip, data, spriteSheet, animationSteps):

        self.player = player
        self.size = data[0]
        self.imageScale = data[1]
        self.offset = data[2]

        self.flip = flip

        self.animationList = self.loadImages(spriteSheet, animationSteps, player)
        self.action = 0 #0: idle   #1: run     #2: jump    #3: attack1    #4: attack2    #5: hit    #6: death    #7: attack3  <--- this is wrong now
        self.frameIndex = 0
        self.image = self.animationList[self.action][self.frameIndex]
        self.updateTime = pygame.time.get_ticks()

        self.rect = pygame.Rect((x, y, 80, 180))

        #Y velocity
        self.velY = 0
        self.running = False
        self.jump = False
        self.attacking = False

        self.collidingRight = False
        self.collidingLeft = False
       

        #which attack is being used
        self.attackType = 0
        self.attackCooldown = 0
        self.hit = False
        self.health = 100
        self.specBar = 0
        self.alive = True
        self.attackDelay = 0  #ms delay before attack hitbox triggers
        self.attackHitboxTriggered = False



    def loadImages(self, spriteSheet, animationSteps, player):

        #extract images from spritesheet
        animationList = []

        if player == 1:

            for y, animation in enumerate(animationSteps):

                tempImgList = []

                for x in range(animation):
                    tempImg = spriteSheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                    
                    tempImgList.append(pygame.transform.scale(tempImg, (self.size * self.imageScale, self.size * self.imageScale)))

                animationList.append(tempImgList)

            return animationList
        
        if player == 2:

            for y, animation in enumerate(animationSteps):

                tempImgList = []

                for x in range(animation):
                    tempImg = spriteSheet.subsurface(x * 231, y * 190, 231, 190)
                    
                    tempImgList.append(pygame.transform.scale(tempImg, (231 * self.imageScale, 190 * self.imageScale)))

                animationList.append(tempImgList)

            return animationList





    '''def move(self, screenWidth, screenHeight, surface, target, roundOver):

        speed = 7
        gravity = 1.7
        dx = 0
        dy = 0
        self.running = False

        #get keypresses
        key = pygame.key.get_pressed()

        #can only perform other actions if not currently attacking
        if self.attacking == False and self.alive == True and roundOver == False:
            #check player 1 controls
            if self.player == 1:

                #movement
                if key[pygame.K_a]:
                    dx = -speed
                    self.facingLeft = True
                    self.running = True

                if key[pygame.K_d]:
                    dx = speed
                    self.facingLeft = False
                    self.running = True
                #jump
                if key[pygame.K_w] and self.jump == False:
                    self.velY = -30
                    self.jump = True

                #attack
                # Handle attacks only if a valid key is pressed
                if key[pygame.K_f]:
                    self.attackType = 1
                    self.attack(surface, target, self.player, self.attackType)
                elif key[pygame.K_g]:
                    self.attackType = 2
                    self.attack(surface, target, self.player, self.attackType)
                elif key[pygame.K_r]:
                    self.attackType = 3
                    self.attack(surface, target, self.player, self.attackType)
                elif key[pygame.K_t]:
                    self.attackType = 4
                    self.attack(surface, target, self.player, self.attackType)


            #check player 2 controls
            if self.player == 2:

                #movement
                if key[pygame.K_LEFT]:
                    dx = -speed
                    self.facingLeft = True
                    self.running = True

                if key[pygame.K_RIGHT]:
                    dx = speed
                    self.facingLeft = False
                    self.running = True
                #jump
                if key[pygame.K_UP] and self.jump == False:
                    self.velY = -30
                    self.jump = True

                #attack
                if key[pygame.K_KP1] or key[pygame.K_KP2] or key[pygame.K_KP4] or key[pygame.K_KP5]:
                    
                    #determine which attack was used
                    if key[pygame.K_KP1]:
                        self.attackType = 1
                        self.attack(surface, target, self.player, self.attackType)
                    if key[pygame.K_KP2]:
                        self.attackType = 2
                        self.attack(surface, target, self.player, self.attackType)
                    if key[pygame.K_KP4]:
                        self.attackType = 3
                        self.attack(surface, target, self.player, self.attackType)
                    if key[pygame.K_KP5]:
                        self.attackType = 4
                        self.attack(surface, target, self.player, self.attackType)
                    
                    


        #apply gravity

        self.velY += gravity
        dy += self.velY

        #ensure player stays on screen
        if self.rect.left + dx < 0:

            dx = 0 - self.rect.left

        if self.rect.right + dx > screenWidth:

            dx = screenWidth - self.rect.right

        if self.rect.bottom + dy > screenHeight - 110:

            self.velY = 0
            self.jump = False
            dy = screenHeight - 110 - self.rect.bottom

        #ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #make players collide
        if self.rect.colliderect(target.rect):

            #self.rect.x -= dx
            #self.rect.y -= dy

            self.handleCollision(target)

            if self.rect.left + dx < 0:

                dx = 1 - self.rect.left
            

            if self.rect.right + dx > screenWidth:

                dx = screenWidth - self.rect.right



        #apply attack cooldown
        if self.attackCooldown > 0:
            self.attackCooldown -=1

        #update player position
        self.rect.x += dx
        self.rect.y += dy

    #handle animation updates
    def update(self, player, target):
        animationCooldown = 80  #ms per frame

        #player 1 logic
        if player == 1:
            if self.health <= 0:
                if self.alive:
                    self.health = 0
                    self.alive = False
                    self.updateAction(1)  # Death
                    

            elif self.hit:
                self.updateAction(3)  # Hit
            elif self.attacking:
                if self.attackType == 1:
                    self.updateAction(6)  # Attack1
                elif self.attackType == 2:
                    self.updateAction(7)  # Attack2
                    animationCooldown = 120
                elif self.attackType == 3:
                    self.updateAction(0)  # strong
                    animationCooldown = 120
                elif self.attackType == 4:
                    self.updateAction(9) #special
            elif self.jump:
                self.updateAction(5)  # Jump
            elif self.running:
                self.updateAction(8)  # Run
            else:
                self.updateAction(4)  # Idle

        #player 2 logic
        elif player == 2:
            if self.health <= 0:
                if self.alive:
                    self.health = 0
                    self.alive = False
                    self.updateAction(0)  # Death

            elif self.hit:
                self.updateAction(2)  # Hit
            elif self.attacking:
                if self.attackType == 1:
                    animationCooldown = 40
                    self.updateAction(5)  # Attack1
                elif self.attackType == 2:
                    animationCooldown = 90
                    self.updateAction(6)  # Attack2
                elif self.attackType == 3:
                    self.updateAction(8) #strong
                elif self.attackType == 4:
                    animationCooldown = 110
                    self.updateAction(9) #special
            elif self.jump:
                self.updateAction(4)  # Jump
            elif self.running:
                self.updateAction(7)  # Run
            else:
                self.updateAction(3)  # Idle

        #Attack hitbox logic
        if self.attacking and not self.attackHitboxTriggered:
            if pygame.time.get_ticks() - self.attackStartTime >= self.attackDelay:
                self.applyAttackHitbox(pygame.display.get_surface(), target)
                self.attackHitboxTriggered = True

        #handle animation frame update
        self.image = self.animationList[self.action][self.frameIndex]

        #advance frame if cooldown passed
        if pygame.time.get_ticks() - self.updateTime > animationCooldown:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()

            #check if animation has finished
            if self.frameIndex >= len(self.animationList[self.action]):
                if self.action == 1 and not self.alive:  # Death animation
                    self.frameIndex = len(self.animationList[self.action]) - 1  # Freeze on last frame
                else:
                    self.frameIndex = 0
                    if self.attacking:
                        self.attacking = False
                        self.attackHitboxTriggered = False
                    if self.hit:
                        self.hit = False'''
    
    def move(self, screenWidth, screenHeight, surface, target, roundOver):
        speed = 7
        gravity = 1.7
        dx = 0
        dy = 0
        self.running = False

        key = pygame.key.get_pressed()
        currentTime = pygame.time.get_ticks()

        # Check if the key press is new (for attacks and jump)
        if not hasattr(self, 'lastKeys'):
            self.lastKeys = key
            self.keyDelay = 150  # ms delay between accepted inputs
            self.lastKeyTime = currentTime

        keyChanged = currentTime - self.lastKeyTime >= self.keyDelay

        if self.attacking == False and self.alive == True and roundOver == False:
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -speed
                    self.facingLeft = True
                    self.running = True

                if key[pygame.K_d]:
                    dx = speed
                    self.facingLeft = False
                    self.running = True

                if key[pygame.K_w] and not self.jump and keyChanged and not self.lastKeys[pygame.K_w]:
                    self.velY = -30
                    self.jump = True
                    self.lastKeyTime = currentTime

                if keyChanged:
                    if key[pygame.K_f] and not self.lastKeys[pygame.K_f]:
                        self.attackType = 1
                        self.attack(surface, target, self.player, self.attackType)
                        self.lastKeyTime = currentTime
                    elif key[pygame.K_g] and not self.lastKeys[pygame.K_g]:
                        self.attackType = 2
                        self.attack(surface, target, self.player, self.attackType)
                        self.lastKeyTime = currentTime
                    elif key[pygame.K_r] and not self.lastKeys[pygame.K_r]:
                        self.attackType = 3
                        self.attack(surface, target, self.player, self.attackType)
                        self.lastKeyTime = currentTime
                    elif key[pygame.K_t] and not self.lastKeys[pygame.K_t]:
                        self.attackType = 4
                        self.attack(surface, target, self.player, self.attackType)
                        self.lastKeyTime = currentTime

            elif self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = -speed
                    self.facingLeft = True
                    self.running = True

                if key[pygame.K_RIGHT]:
                    dx = speed
                    self.facingLeft = False
                    self.running = True

                if key[pygame.K_UP] and not self.jump and keyChanged and not self.lastKeys[pygame.K_UP]:
                    self.velY = -30
                    self.jump = True
                    self.lastKeyTime = currentTime

                if keyChanged:
                    if key[pygame.K_KP1] and not self.lastKeys[pygame.K_KP1]:
                        self.attackType = 1
                        self.attack(surface, target, self.player, self.attackType)
                        self.lastKeyTime = currentTime
                    elif key[pygame.K_KP2] and not self.lastKeys[pygame.K_KP2]:
                        self.attackType = 2
                        self.attack(surface, target, self.player, self.attackType)
                        self.lastKeyTime = currentTime
                    elif key[pygame.K_KP4] and not self.lastKeys[pygame.K_KP4]:
                        self.attackType = 3
                        self.attack(surface, target, self.player, self.attackType)
                        self.lastKeyTime = currentTime
                    elif key[pygame.K_KP5] and not self.lastKeys[pygame.K_KP5]:
                        self.attackType = 4
                        self.attack(surface, target, self.player, self.attackType)
                        self.lastKeyTime = currentTime

        # Apply gravity
        self.velY += gravity
        dy += self.velY

        # Ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left

        if self.rect.right + dx > screenWidth:
            dx = screenWidth - self.rect.right

        if self.rect.bottom + dy > screenHeight - 110:
            self.velY = 0
            self.jump = False
            dy = screenHeight - 110 - self.rect.bottom

        # Ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # Make players collide
        if self.rect.colliderect(target.rect):
            self.handleCollision(target)

            if self.rect.left + dx < 0:
                dx = 1 - self.rect.left
            if self.rect.right + dx > screenWidth:
                dx = screenWidth - self.rect.right

        # Apply attack cooldown
        if self.attackCooldown > 0:
            self.attackCooldown -= 1

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

        # Save key state
        self.lastKeys = key




    def attack(self, surface, target, player, attackType):
        if self.attackCooldown == 0 and not self.attacking:
            self.attacking = True
            self.attackType = attackType
            self.attackStartTime = pygame.time.get_ticks() 
            self.attackHitboxTriggered = False  # Reset trigger flag

            # Set attackDelay based on type
            if player == 1:

                if self.attackType == 1:
                    self.attackDelay = 320
                elif self.attackType == 2:
                    self.attackDelay = 320
                elif self.attackType == 3:
                    if self.specBar < 50:
                        print("Not enough special bar for attack 3")
                        self.attacking = False
                        return
                    self.attackDelay = 560

                elif self.attackType == 4:
                    self.attackDelay = 400
                else:
                    self.attackDelay = 200  # default fallback

            elif player == 2:

                if self.attackType == 1:
                    self.attackDelay = 200
                elif self.attackType == 2:
                    self.attackDelay = 500
                elif self.attackType == 3:
                    if self.specBar < 50:
                        print("Not enough special bar for Player 2 attack 3")
                        self.attacking = False
                        return
                    self.attackDelay = 460

                elif self.attackType == 4:
                    self.attackDelay = 600
                else:
                    self.attackDelay = 200  # default fallback



    def applyAttackHitbox(self, surface, target):
        attackingRect = None

        #mr e attacks
        if self.player == 1 and self.attackType == 1:

            hitbox_width = 2.5 * self.rect.width
            hitbox_height = self.rect.height
            hitbox_y = self.rect.y

            if self.flip:
                hitbox_x = self.rect.centerx - hitbox_width
            else:
                hitbox_x = self.rect.centerx

            attackingRect = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

            if attackingRect.colliderect(target.rect):
                target.health -= 10
                self.specBar += 10
                target.hit = True
                print("this one", target.health)

        elif self.player == 1 and self.attackType == 2:

            hitbox_width = 2.5 * self.rect.width
            hitbox_height = self.rect.height
            hitbox_y = self.rect.y

            if self.flip:
                hitbox_x = self.rect.centerx - hitbox_width
            else:
                hitbox_x = self.rect.centerx

            attackingRect = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

        elif self.player == 1 and self.attackType == 3:

            hitbox_width = 3.2 * self.rect.width
            hitbox_height = self.rect.height + 10
            hitbox_y = self.rect.y

            if self.flip:
                hitbox_x = self.rect.centerx - hitbox_width
            else:
                hitbox_x = self.rect.centerx

            attackingRect = pygame.Rect(hitbox_x, hitbox_y - 10, hitbox_width, hitbox_height)

        elif self.player == 1 and self.attackType == 4:

            hitbox_width = 4 * self.rect.width
            hitbox_height = self.rect.height * 2
            hitbox_y = self.rect.y

            if self.flip:
                hitbox_x = self.rect.centerx - hitbox_width
            else:
                hitbox_x = self.rect.centerx

            attackingRect = pygame.Rect(hitbox_x - 40, hitbox_y - self.rect.height, hitbox_width, hitbox_height)


        #staff attacks
        elif self.player == 2 and self.attackType == 1:

            hitbox_width = 3 * self.rect.width
            hitbox_height = self.rect.height / 2
            hitbox_y = self.rect.y

            if self.flip:
                hitbox_x = self.rect.centerx - hitbox_width
            else:
                hitbox_x = self.rect.centerx

            attackingRect = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)


        elif self.player == 2 and self.attackType == 2:
            hitbox_width = 200
            hitbox_height = 100
            hitbox_y = self.rect.centery - hitbox_height  # vertically centered

            if self.flip:
                # Position hitbox far to the left
                hitbox_x = self.rect.left - 250
            else:
                # Position hitbox far to the right
                hitbox_x = self.rect.right + 50

            attackingRect = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

        elif self.player == 2 and self.attackType == 3:
            
            hitbox_width = 3.8 * self.rect.width
            hitbox_height = self.rect.height
            hitbox_y = self.rect.y

            if self.flip:
                hitbox_x = self.rect.centerx - hitbox_width
            else:
                hitbox_x = self.rect.centerx

            attackingRect = pygame.Rect(hitbox_x, hitbox_y - 30, hitbox_width, hitbox_height)
              

        elif self.player == 2 and self.attackType == 4:

            hitbox_width = 200
            hitbox_height = 200
            hitbox_y = self.rect.centery - hitbox_height  # vertically centered

            if self.flip:
                # Position hitbox far to the left
                hitbox_x = self.rect.left - 250
            else:
                # Position hitbox far to the right
                hitbox_x = self.rect.right + 50

            attackingRect = pygame.Rect(hitbox_x - 50, hitbox_y + 40, hitbox_width, hitbox_height)




        else:
            # Default hitbox
            hitbox_width = 2 * self.rect.width
            if self.flip:
                hitbox_x = self.rect.centerx - hitbox_width
            else:
                hitbox_x = self.rect.centerx

            attackingRect = pygame.Rect(hitbox_x, self.rect.y, hitbox_width, self.rect.height)

        # Debug: draw hitbox
        pygame.draw.rect(surface, (0, 255, 0), attackingRect)

        if attackingRect.colliderect(target.rect):
            target.health -= 10
            self.specBar += 10
            target.hit = True
            print("Hit! Target Health:", target.health)


    def updateAction(self, newAction):
        #check if the new action is different to the previous one
        if newAction != self.action:
            self.action = newAction

            #update the animation settings
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()

    def handleCollision(self, target):

        if self.rect.x > target.rect.x:

            self.rect.x += 5
            target.rect.x -= 5

        else:

            self.rect.x -=5
            target.rect.x +=5
        

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        if self.flip:
            draw_x = self.rect.x - (self.offset[0] * self.imageScale)
        else:
            draw_x = self.rect.x - ((self.image.get_width() - self.rect.width) - (self.offset[0] * self.imageScale))

        pygame.draw.rect(surface, (255, 0, 0), self.rect)  # Debug: show hitbox
        surface.blit(img, (draw_x, self.rect.y - (self.offset[1] * self.imageScale)))
