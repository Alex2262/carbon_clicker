import pygame
import random
from constants import *


'''
This is a file containing different objects, classes, and subclasses.
A lot of Object Oriented Programming exists in this file.
'''


# ----------------- The main Object class -----------------
class Object:
    def __init__(self, rect):
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]


# ----------------- A circular Object -----------------
# (extends Object)
class CircleObject(Object):
    # 3 panels
    def __init__(self, color, center, thickness, radius):
        super().__init__((center[0], center[1], radius, radius))
        self.center = center
        self.color = color

        self.thickness = thickness
        self.radius = radius

    # Draw the item
    def draw(self, surface, selected):
        if len(self.color) < 4 or self.color[3] != 0:
            pygame.draw.circle(surface, self.color,
                              (self.x, self.y), self.radius, self.thickness)


# ----------------- A rectangular Object -----------------
# (extends Object)
class RectObject(Object):
    # 3 panels
    def __init__(self, color, rect, border, radius):
        super().__init__(rect)
        self.color = color

        self.border = border
        self.radius = radius

    # Draw the item
    def draw(self, surface, selected):
        if len(self.color) < 4 or self.color[3] != 0:
            pygame.draw.rect(surface, self.color,
                             (self.x, self.y, self.width, self.height), self.border, self.radius)


# ----------------- A rectangular Object with an image -----------------
# (extends RectObject)
class ImageRectObject(RectObject):
    def __init__(self, color, rect, border, radius, image_file):
        super().__init__(color, rect, border, radius)
        self.image_file = image_file
        self.image = pygame.image.load(self.image_file).convert_alpha()

    def draw(self, surface, selected):
        surface.blit(self.image, (self.x, self.y))


# ----------------- The Rectangular Text Object -----------------
# (extends RectObject)
class RectTextObject(RectObject):
    # Displays the text
    def __init__(self, color, rect, border, radius, text='', text_color=(0, 0, 0), text_size=10):
        super().__init__(color, rect, border, radius)

        self.text_size = text_size
        self.text = text
        self.text_color = text_color

        self.font = pygame.font.Font('fonts/HackbotFreeTrial-8MgA2.otf',
                                     text_size)
        self.text_surf = self.font.render(self.text, True, self.text_color)

    def draw(self, surface, selected):
        super().draw(surface, selected)
        if self.text != '':
            self.text_surf = self.font.render(self.text, True, self.text_color)
            surface.blit(self.text_surf, (self.x + (self.width / 2 - self.text_surf.get_width() / 2),
                                          self.y + (self.height / 2 - self.text_surf.get_height() / 2)))


# ----------------- The Image Rectangular Text Object -----------------
# (extends RectTextObject)
class ImageRectTextObject(RectTextObject):
    def __init__(self, color, rect, border, radius, image_file, text='', text_color=(0, 0, 0), text_size=10):
        super().__init__(color, rect, border, radius, text, text_color, text_size)
        self.image_file = image_file
        self.image = pygame.image.load(self.image_file).convert_alpha()

    def draw(self, surface, selected):
        surface.blit(self.image, (self.x, self.y))
        self.text_surf = self.font.render(self.text, True, self.text_color)
        surface.blit(self.text_surf, (self.x + (self.width / 2 - self.text_surf.get_width() / 2),
                                      self.y + (self.height / 2 - self.text_surf.get_height() / 2)))


# ----------------- Achievements -----------------
# (extends RectTextObject)
# Achievement text information that is shown when the user has reached a certain checkpoint
class AchievementText(RectTextObject):
    def __init__(self, color, rect, border, radius, text='', text_color=(0, 0, 0, 255), text_size=20):
        super().__init__(color, rect, border, radius, text, text_color, text_size)

    def draw(self, surface, selected):
        max_char_per_line = 2 * (self.width - 30) // self.text_size
        word_list = self.text.split()
        lines = []
        current_line = ""

        for i in range(len(word_list)):

            if len(current_line) + 1 + len(word_list[i]) > max_char_per_line:
                lines.append(current_line)
                current_line = ""  # NOTE: CHECK FOR COPYING

            current_line += word_list[i]
            current_line += " "

            if i == len(word_list) - 1:
                lines.append(current_line)
                break

        for i in range(len(lines)):
            self.text_surf = self.font.render(lines[i], True, self.text_color)
            surface.blit(self.text_surf, (self.x + 15, self.y + 15 + i * (self.height - 30) // len(lines)))


# ----------------- The Animated Text Object -----------------
# (extends RectTextObject)
# The text that appears when you click the earth (+1 pollution cleared
class AnimatedText(RectTextObject):
    # +1 pollution cleared
    def __init__(self, color, rect, border, radius, text='', text_color=(0, 0, 0, 255), text_size=20):
        super().__init__(color, rect, border, radius, text, text_color, text_size)

    def draw(self, surface, selected):
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_surf.set_alpha(self.text_color[3])
        surface.blit(self.text_surf, (self.x + (self.width / 2 - self.text_surf.get_width() / 2),
                                      self.y + (self.height / 2 - self.text_surf.get_height() / 2)))

    # rise and fade out
    def move(self):
        self.y -= 3
        self.text_color = (self.text_color[0], self.text_color[1], self.text_color[2], self.text_color[3]-6)
        if self.y <= 0 or self.text_color[3] <= 0:
            return True
        return False


# ----------------- The Rectangular Text Button -----------------
# (extends RectTextObject)
# A general class for text buttons that are rectangular
class RectTextButton(RectTextObject):
    def __init__(self, color, rect, border, radius, action, text='', text_color=(0, 0, 0), text_size=10):
        super().__init__(color, rect, border, radius, text, text_color, text_size)
        self.action = action

    def draw(self, surface, selected):
        if selected:
            pygame.draw.rect(surface, (self.color[0], self.color[1], self.color[2], 255),
                             (self.x, self.y, self.width, self.height), self.border, self.radius)
        else:
            pygame.draw.rect(surface, (self.color[0], self.color[1], self.color[2], 220),
                             (self.x, self.y, self.width, self.height), self.border, self.radius)

        if self.text != '':
            self.text_surf = self.font.render(self.text, True, self.text_color)
            surface.blit(self.text_surf, (self.x + (self.width / 2 - self.text_surf.get_width() / 2),
                                          self.y + (self.height / 2 - self.text_surf.get_height() / 2)))

    def is_selecting(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width and \
                self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False

    def get_action(self):
        return self.action


# ----------------- The Image Button -----------------
# (extends RectTextButton)
# A general class for Image Button Objects
class ImageButton(RectTextButton):
    # e.g. sell button. Buttons with images
    def __init__(self, color, rect, border, radius, action, image_file, text='', text_color=(0, 0, 0), text_size=10):
        super().__init__(color, rect, border, radius, action, text, text_color, text_size)
        self.image = pygame.image.load(image_file).convert_alpha()

    def draw(self, surface, selected):
        surface.blit(self.image, (self.x, self.y))

        self.text_surf = self.font.render(self.text, True, self.text_color)
        surface.blit(self.text_surf, (self.x + (self.width / 2 - self.text_surf.get_width() / 2),
                                      self.y + (self.height / 2 - self.text_surf.get_height() / 2)))

        if selected:
            new_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            new_surface.set_alpha(40)
            new_surface.fill((0, 0, 0))
            surface.blit(new_surface, (self.x, self.y))

    def is_selecting(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width and \
                self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False

    def get_action(self):
        return self.action


# ----------------- The Item -----------------
# Every object or machine that you purchase
# For example, volunteers, claws, trees, seabins, etc.
# All items are tools you can use to help the environment, or new innovative technologies designed to reduce pollution
class Item(RectTextButton):
    # the things you buy on the right
    def __init__(self, color, rect, border, radius, action, item_type, text='', text_color=GOLD_COLOR, text_size=32):
        super().__init__(color, rect, border, radius, action, text, text_color, text_size)
        self.hidden = True
        self.enough = False
        self.item_type = item_type
        self.image = pygame.image.load("images/building_frame.png").convert_alpha()
        self.item_icon = pygame.image.load("images/item_icons/item_icon{0}.png".format(item_type))

        self.price = ITEM_PRICES[item_type]
        self.text = ITEM_NAMES[item_type]
        self.rate = ITEM_RATES[item_type]
        self.count = 0
        self.multiplier = 1

    # Draws the rectangle on the right side of the screen
    def draw(self, surface, selected):
        surface.blit(self.image, (self.x, self.y))

        # Only show the actual Item if it is not hidden
        if not self.hidden:
            surface.blit(self.item_icon, (self.x+10, self.y + (self.height / 2 - 100 / 2)))
            self.text_surf = self.font.render(self.text, True, self.text_color)
            surface.blit(self.text_surf, (self.x + 35 + (self.width / 2 - self.text_surf.get_width() / 2),
                                          self.y - 20 + (self.height / 2 - self.text_surf.get_height() / 2)))

            money_font = pygame.font.Font('fonts/HackbotFreeTrial-8MgA2.otf',
                                          24)
            money_text_surf = money_font.render("$: " + str(self.price), True, MONEY_COLOR)
            surface.blit(money_text_surf, (self.x + 35 + (self.width / 2 - money_text_surf.get_width() / 2),
                                          self.y + 20 + (self.height / 2 - money_text_surf.get_height() / 2)))

            count_font = pygame.font.Font('fonts/HackbotFreeTrial-8MgA2.otf',
                                          35)
            count_text_surf = count_font.render(str(self.count), True, COUNT_COLOR)
            surface.blit(count_text_surf, (self.x + 150 + (self.width / 2 - count_text_surf.get_width() / 2),
                                          self.y + 10 + (self.height / 2 - count_text_surf.get_height() / 2)))

        # Visibility code for when the upgrade is selected or not able to be bought
        if selected:
            new_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            new_surface.set_alpha(40)
            new_surface.fill((0, 0, 0))
            surface.blit(new_surface, (self.x, self.y))
        if not self.enough:
            new_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            new_surface.set_alpha(200)
            new_surface.fill((0, 0, 0))
            surface.blit(new_surface, (self.x, self.y))

    def is_selecting(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width and \
                self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False

    def get_action(self):
        return self.action


# ----------------- The Scroll Bar -----------------
# (extends ImageButton)
# A scroll bar that scrolls the items up and down
class ScrollBar(ImageButton):
    def __init__(self, color, rect, border, radius, image_file):
        super().__init__(color, rect, border, radius, "", image_file, text="", text_color=(0, 0, 0), text_size=0)

    def draw(self, surface, selected):
        super().draw(surface, selected)

    def move(self, mouse_y_offset):
        self.y += mouse_y_offset


# ----------------- Item Popup Class -----------------
# The text label that pops up when you hover your cursor over an item.
# It provides a brief description about what the item does in the real world
class ItemPopup(ImageRectTextObject):
    # self, color, rect, border, radius, image_file, text='', text_color=(0, 0, 0), text_size=10
    def __init__(self, color, rect, border, radius, machine_image, popup_message="Lorem Ipsum"):
        super().__init__(color, rect, border, radius, machine_image, text=popup_message, text_color=(250, 250, 250),
                         text_size=15)

    def draw(self, surface, selected):
        surface.blit(self.image, (self.x, self.y))

        # ----------------- Code used for wrapping text and formatting -----------------

        popup_width = 390
        popup_height = 100

        # Calculate each line
        max_char_per_line = 2 * (popup_width - 30) // self.text_size
        word_list = self.text.split()
        lines = []
        current_line = ""

        # Place each formatted line into an array that will be processed
        for i in range(len(word_list)):

            if len(current_line) + 1 + len(word_list[i]) > max_char_per_line:
                lines.append(current_line)
                current_line = ""  # NOTE: CHECK FOR COPYING

            current_line += word_list[i]
            current_line += " "

            if i == len(word_list) - 1:
                lines.append(current_line)
                break

        # Place each line of text
        for i in range(len(lines)):
            self.text_surf = self.font.render(lines[i], True, self.text_color)
            surface.blit(self.text_surf, (self.x + 15, self.y + 15 + i * (popup_height - 30) // len(lines)))


# ----------------- Upgrade Class -----------------
# (extends ImageButton)
# Upgrades for increasing machine rates
class Upgrade(ImageButton):
    def __init__(self, color, rect, border, radius, action, item, text, text_color, text_size):
        self.image_file = "images/upgrade_frame.png"  # TODO: Get image file (frame)

        super().__init__(color, rect, border, radius, action, self.image_file, text, text_color, text_size)

        self.item_type = item[0]
        self.tier = item[1]

        self.price = UPGRADE_COSTS[self.item_type][self.tier]
        self.affected_items = UPGRADE_ACTIONS[self.item_type]
        self.affected_rates = UPGRADE_RATES[self.item_type][self.tier]
        self.hidden = False
        self.purchased = False
        self.enough = False

        self.icon = pygame.image.load(
            "images/upgrade_icons/upgrade_icon{0}_{1}.png".format(self.item_type, self.tier)).convert_alpha()

        self.upgrade_order = 0
        for i in range(len(UPGRADE_ORDER)):
            if self.item_type == UPGRADE_ORDER[i][0] and self.tier == UPGRADE_ORDER[i][1]:
                self.upgrade_order = i
                break

    # Draw the Upgrades
    def draw(self, surface, selected):
        if self.hidden:
            return

        surface.blit(self.image, (self.x, self.y))
        surface.blit(self.icon, (self.x + 4, self.y + 4))

        # Visibility code for when the upgrade is selected or not able to be bought
        if selected:
            new_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            new_surface.set_alpha(40)
            new_surface.fill((0, 0, 0))
            surface.blit(new_surface, (self.x, self.y))
        if not self.enough:
            new_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            new_surface.set_alpha(200)
            new_surface.fill((0, 0, 0))
            surface.blit(new_surface, (self.x, self.y))

    # Move the upgrades based on order and price
    def move(self, new_order):
        if self.hidden:
            return

        row = new_order // 4
        col = new_order % 4
        self.x = 4 + col * self.width
        self.y = LAYER_UPGRADE_TITLE_RECT[1] + LAYER_UPGRADE_TITLE_RECT[3] - 4 + row * self.height


# ----------------- Upgrade Popup Class -----------------
# The popup that appears when you hover over an upgrade
class UpgradePopup(ItemPopup):
    def __init__(self, color, rect, border, radius, machine_image, price, popup_message="Lorem Ipsum"):
        super().__init__(color, rect, border, radius, machine_image, popup_message)
        self.text = popup_message + " $:.." + str(price)

    def draw(self, surface, selected):
        super().draw(surface, selected)


# ----------------- The Earth Clicker -----------------
# (extends the pygame Sprite object for ease of use)
# The globe in the middle that you click
class Earth(pygame.sprite.Sprite):
   
    def __init__(self, rect):
        super().__init__()

        self.max_animation_frames = 10
        self.animation_frame = self.max_animation_frames
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.current_rect = rect

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

        self.stage = 0

        self.unedited_sprite = pygame.image.load("images/earth_clickers/earth0.png")
        self.sprite = pygame.transform.smoothscale(
            self.unedited_sprite,
            (self.width, self.height))

        self.image.blit(self.sprite, (0, 0))
    
    # Draws the earth, depending on how clean it is
    def redraw(self):

        self.unedited_sprite = pygame.image.load("images/earth_clickers/earth{}.png".format(min(4, self.stage)))
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

        self.sprite = pygame.transform.smoothscale(
            self.unedited_sprite,
            (self.width, self.height))

        self.image.blit(self.sprite, (0, 0))
    
    # ----------------- Clicking animations -----------------
    # Scale the earth down
    def resize_down(self):
        self.animation_frame = 0
        self.current_rect = EARTH_CLICKER_SMALL_RECT

    # Rescale it back up
    def resize_normal(self):
        self.animation_frame = 0
        self.current_rect = EARTH_CLICKER_RECT

    def hover(self):
        self.animation_frame = 0
        self.current_rect = EARTH_CLICKER_LARGE_RECT

    def animate(self):
        if self.animation_frame == self.max_animation_frames:
            return

        self.animation_frame += 1

        deltas = (self.current_rect[0] - self.x,
                  self.current_rect[1] - self.y,
                  self.current_rect[2] - self.width,
                  self.current_rect[3] - self.height)

        adjusted_deltas = []
        for d in deltas:
            adjusted_deltas.append(d * (self.animation_frame / self.max_animation_frames))

        self.x += adjusted_deltas[0]
        self.y += adjusted_deltas[1]
        self.width += adjusted_deltas[2]
        self.height += adjusted_deltas[3]

        self.redraw()

    def get_center(self):
        radius = self.width // 2
        center = (self.x + radius, self.y + radius)

        return center

    def colliding(self, location):
        radius = self.width // 2
        center = self.get_center()

        x_leg = abs(location[0] - center[0])
        y_leg = abs(location[1] - center[1])

        hyp = (x_leg ** 2 + y_leg ** 2) ** 0.5

        if hyp <= radius:
            return True
        else:
            return False


# (extends CircleObject)
class Star(CircleObject):
    # 3 panels
    def __init__(self, spawn_rect):
        self.inherent_speed = random.randint(-10, 10) / 100.0
        self.spawn_rect = spawn_rect
        self.radius = 1
        self.x = random.randint(spawn_rect[0], spawn_rect[0] + spawn_rect[2] - self.radius)
        self.y = random.randint(spawn_rect[1], spawn_rect[1] + spawn_rect[3] - self.radius)
        self.twinkle_frame_gap = random.randint(120, 500)
        self.twinkle_frame_counter = 0

        super().__init__((random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)),
                         (self.x, self.y), 0, self.radius)
        self.center = (self.x, self.y)

    def update_position(self, displacement):
        displacement = (displacement[0] + self.inherent_speed,
                        displacement[1] + self.inherent_speed)

        self.x += displacement[0]
        self.y += displacement[1]

        # Out of bounds
        if self.x < self.spawn_rect[0]:
            self.inherent_speed = random.randint(-10, 10) / 100.0
            self.x = self.spawn_rect[0] + self.spawn_rect[2]
            self.y = random.randint(self.spawn_rect[1], self.spawn_rect[1] + self.spawn_rect[3] - self.radius)
        elif self.x > self.spawn_rect[0] + self.spawn_rect[2]:
            self.inherent_speed = random.randint(-10, 10) / 100.0
            self.x = self.spawn_rect[0]
            self.y = random.randint(self.spawn_rect[1], self.spawn_rect[1] + self.spawn_rect[3] - self.radius)
        elif self.y < self.spawn_rect[1]:
            self.inherent_speed = random.randint(-10, 10) / 100.0
            self.x = random.randint(self.spawn_rect[0], self.spawn_rect[0] + self.spawn_rect[2] - self.radius)
            self.y = self.spawn_rect[1] + self.spawn_rect[3]
        elif self.y > self.spawn_rect[1] + self.spawn_rect[3]:
            self.inherent_speed = random.randint(-10, 10) / 100.0
            self.x = random.randint(self.spawn_rect[0], self.spawn_rect[0] + self.spawn_rect[2] - self.radius)
            self.y = self.spawn_rect[1]

        self.center = (self.x, self.y)

    def draw(self, surface, selected):
        super().draw(surface, selected)
        self.twinkle_frame_counter += 1

        if self.twinkle_frame_counter == self.twinkle_frame_gap:
            self.radius = 2
        elif self.twinkle_frame_counter == self.twinkle_frame_gap + 20:
            self.radius = 1
            self.twinkle_frame_counter = 0
            self.twinkle_frame_gap = random.randint(120, 500)


