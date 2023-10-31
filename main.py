
# Import modules and code/classes/objects from other files
import math

import pygame.font

from objects import *
from messages import *


# The Main function in which all the GUI code is ran
def main():

    # ----------------- Initializing Pygame Variables -----------------
    pygame.init()
    clock = pygame.time.Clock()  # Clock for adjusting the frames per second

    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # The initial Pygame Screen

    screen.fill(SCREEN_COLOR)
    pygame.display.set_caption("Carbon Clicker")

    application_icon = pygame.image.load("images/carbon_clicker_logo.png")
    pygame.display.set_icon(application_icon)

    logo = ImageRectObject((0, 0, 0, 0), (WIDTH // 2 - 200, HEIGHT // 2 - 200, 400, 400), 0, 0,
                            image_file="images/carbon_clicker_logo.png")
    logo.image = pygame.transform.scale(logo.image, (400, 400))

    basic_objects = [
        RectTextObject(SCREEN_COLOR, (WIDTH // 2 - 300, 40, 600, 100), 0, 50,
                       text="", text_color=GOLD_COLOR, text_size=60),
        RectTextObject(SCREEN_COLOR, (WIDTH // 2 - 100, 600, 200, 60), 0, 50,
                       text="", text_color=GOLD_COLOR, text_size=40),
        RectTextObject(GOLD_COLOR, (WIDTH // 2 - 300, 40, 600, 100), 4, 50,
                       text="Carbon Clicker!", text_color=GOLD_COLOR, text_size=60),
        logo,
    ]

    start_button = RectTextButton(GOLD_COLOR, (WIDTH // 2 - 100, 600, 200, 60), 4, 50, action="start_game",
                                  text="Start", text_color=GOLD_COLOR, text_size=40)

    stars = []

    for star_i in range(400):
        stars.append(Star((0, 0, WIDTH, HEIGHT)))

    starting = False
    transparency = 0

    # main_game(screen)

    # ----------------- The Main GUI Loop -----------------
    running = True
    while running:

        # ----------------- Looping through Pygame Events -----------------
        for event in pygame.event.get():

            # Quit Pygame
            if event.type == pygame.QUIT:
                running = False
                break

            # ----------------- Mouse Released -----------------
            if event.type == pygame.MOUSEBUTTONUP and not starting:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.is_selecting(mouse_pos):
                    starting = True

        # Re-Draw
        screen.fill(SCREEN_COLOR)

        # Draw stars
        mouse_pos = pygame.mouse.get_pos()
        displacement = ((mouse_pos[0] - WIDTH // 2) / 2400.0, (mouse_pos[1] - HEIGHT // 2) / 2400.0)

        for star in stars:
            star.update_position(displacement)
            star.draw(screen, False)

        is_selected = start_button.is_selecting(mouse_pos)

        # Draw objects
        draw_basic_objects(screen, basic_objects)
        start_button.draw(screen, is_selected)

        if starting:
            transparency = transparency + 2 + transparency * 0.1
            new_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            new_surface.set_alpha(transparency)
            new_surface.fill((0, 0, 0))
            screen.blit(new_surface, (0, 0))

            if transparency >= 255:
                running = False

        # Set the FPS and update
        clock.tick(60)
        pygame.display.update()

    main_game(screen)


def main_game(screen):

    # ----------------- Initializing Objects -----------------
    starting = True
    transparency = 255

    time = 0  # Used for keeping track of seconds (60 ticks per second)
    clock = pygame.time.Clock()  # Clock for adjusting the frames per second

    # The Main Panels
    title_panel = RectTextObject((0, 0, 0, 0), LAYER_TITLE_RECT, 0, 0,
                                       text="Carbon Clicker!", text_color=GOLD_COLOR, text_size=35)
    pollution_cleared_panel = RectTextObject((0, 0, 0, 0), LAYER_POLLUTION_CLEARED_RECT, 0, 0,
                                       text="Pollution Cleared: 000000 lbs", text_color=GOLD_COLOR, text_size=24)
    pps_panel = RectTextObject((0, 0, 0, 0), LAYER_PPS_RECT, 0, 0,
                                       text="PPS: 000000", text_color=GOLD_COLOR, text_size=24)
    money_panel = RectTextObject((0, 0, 0, 0), LAYER_MONEY_RECT, 0, 0,
                               text="$: 000000", text_color=GOLD_COLOR, text_size=24)
    item_panel = ImageRectTextObject((0, 0, 0), LAYER_ITEMS_RECT, 0, 0, image_file="images/item_panel.png",
                                text="Items!", text_color=GOLD_COLOR, text_size=40)

    achievement_title_panel = RectTextObject((0, 0, 0, 0), LAYER_ACHIEVEMENT_TITLE_RECT, 0, 0, text="Achievements:",
                                             text_color=GOLD_COLOR, text_size=30)
    upgrade_title_panel = RectTextObject((0, 0, 0, 0), LAYER_UPGRADE_TITLE_RECT, 0, 0, text="Upgrades:",
                                             text_color=GOLD_COLOR, text_size=30)

    # ----------------- Sounds -----------------
    click_sound = pygame.mixer.Sound("sounds/mouse_click.mp3")
    click_sound.set_volume(0.4)
    purchase_sound = pygame.mixer.Sound("sounds/purchase.mp3")
    purchase_sound.set_volume(0.6)
    achievement_sound = pygame.mixer.Sound("sounds/achievement_sound.mp3")

    # ----------------- Achievements -----------------
    previous_achievement_stage = 0
    achievement = AchievementText((0, 0, 0, 0), (15,
                                                 LAYER_ACHIEVEMENT_TITLE_RECT[1] + LAYER_ACHIEVEMENT_TITLE_RECT[3]+15,
                                                 LAYER_ACHIEVEMENT_TITLE_RECT[2]-15, 135), 0, 0, text="",
                                 text_color=GOLD_COLOR, text_size=18)

    # ----------------- Objects in their lists -----------------

    # Create the first layer of basic objects
    basic_objects_layer_1 = [
        ImageRectObject((100, 100, 100), LAYER_LEFT_RECT, 0, 0, image_file="images/left_background.png"),
        ImageRectObject((200, 200, 200), LAYER_MIDDLE_RECT, 0, 0, image_file="images/middle_background_border.png"),
        RectObject((0, 0, 0), LAYER_RIGHT_RECT, 0, 0),
        title_panel,
        pollution_cleared_panel,
        pps_panel,
        money_panel,
        RectObject((0, 0, 0), LAYER_SCROLL_BAR_RECT, 0, 0),
        achievement_title_panel,
        upgrade_title_panel,
        achievement
    ]

    # This second layer of objects goes above the items
    basic_objects_layer_2 = [
        item_panel
    ]

    stars = []

    for star_i in range(NUM_STARS):
        stars.append(Star(LAYER_BOTTOM_RECT))

    # ----------------- Scroll Bar -----------------
    holding_scroll_bar = False
    starting_mouse_y = 0
    scroll_bar = ScrollBar((0, 0, 0, 0), (LAYER_RIGHT_RECT[0] + 390, LAYER_RIGHT_RECT[1] + LAYER_ITEMS_RECT[3], 10, 50),
                           0, 0, image_file="images/scroll_bar.png")

    sell_button = ImageButton((0, 0, 0, 0), SELL_BUTTON_RECT, 0, 0, "SELL", "images/sell_button.png",
                              text="SELL!", text_color=GOLD_COLOR, text_size=30)

    # ----------------- Buttons -----------------
    buttons = [
        scroll_bar,
        sell_button
    ]

    # ----------------- Items -----------------
    item_popup = None
    items = []
    item_base_y_pos = LAYER_ITEMS_RECT[3]
    item_max_y_pos = LAYER_ITEMS_RECT[3]
    item_min_y_pos = LAYER_ITEMS_RECT[3] - NUM_ITEMS * 100 + 6 * 100

    for item_type in range(NUM_ITEMS):
        items.append(Item((0, 0, 0, 0), (LAYER_RIGHT_RECT[0], item_base_y_pos + item_type * 100, 390, 100), 0, 0,
                          "ITEM", item_type, "", GOLD_COLOR, 25))

    animation_text_list = []  # append later

    # ----------------- Upgrades -----------------
    upgrade_count = 0
    upgrades_shown = [0]
    upgrades = []
    upgrade_popup = None

    # Create the Upgrade objects
    for _upgrade in range(len(UPGRADE_ORDER)):
        upgrades.append(Upgrade((0, 0, 0, 0),
                                (0, LAYER_UPGRADE_TITLE_RECT[1] + LAYER_UPGRADE_TITLE_RECT[3], 73, 73),
                                 0, 0, "UPGRADE", (UPGRADE_ORDER[_upgrade][0], UPGRADE_ORDER[_upgrade][1]),
                                "", (0, 0, 0), 0))

    # ----------------- Variables and internal Data -----------------
    money = 10000000000000000

    pollution_cleared = 0
    total_pollution_cleared = 0
    previous_pollution_cleared = 0
    pps = 0

    click_strength = 0.2
    max_click_interval = 3
    click_interval = 0
    can_click = True

    hovering_earth = False

    # ----------------- Sprites -----------------
    earth_clicker = Earth(EARTH_CLICKER_RECT)
    sprite_group = pygame.sprite.Group()
    sprites = [earth_clicker,]
    sprite_group.add(sprites)

    # Used to determine which objects are selected
    selected_object = None

    # ----------------- The Main GUI Loop -----------------
    running = True
    while running:

        # ----------------- Looping through Pygame Events -----------------
        for event in pygame.event.get():

            # Quit Pygame
            if event.type == pygame.QUIT:
                running = False
                break

            # ----------------- Mouse Clicked -----------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                colliding_earth = earth_clicker.colliding(location)

                # The earth was clicked
                if can_click and colliding_earth:
                    earth_clicker.resize_down()

                # The scroll bar was clicked
                if selected_object == scroll_bar:
                    starting_mouse_y = location[1]
                    holding_scroll_bar = True

            # ----------------- Mouse Released -----------------
            if event.type == pygame.MOUSEBUTTONUP:
                location = pygame.mouse.get_pos()
                colliding_earth = earth_clicker.colliding(location)

                # Calculate changes when the earth has been clicked
                if can_click and colliding_earth:
                    click_sound.play()
                    earth_clicker.hover()
                    pollution_cleared += click_strength
                    total_pollution_cleared += click_strength

                    # Animations
                    animation_rect = (location[0]+random.randint(-2, 2), location[1]+random.randint(-2, 2),
                                      20, 10)
                    animation_text_list.append(AnimatedText((0, 0, 0, 0), animation_rect, 0, 0,
                                                text="+{} pollution cleared".format(click_strength),
                                                text_color=(GOLD_COLOR[0], GOLD_COLOR[1], GOLD_COLOR[2], 255)))
                    can_click = False

                # An Item is being bought
                if type(selected_object) == Item and money >= selected_object.price:
                    selected_object.count += 1
                    money = round(money - selected_object.price)
                    purchase_sound.play()

                    selected_object.price = round(selected_object.price * 1.1)

                # An Upgrade is being bought
                if type(selected_object) == Upgrade and money >= selected_object.price:
                    money = round(money - selected_object.price)
                    selected_object.purchased = True

                    for i in range(len(selected_object.affected_items)):
                        item = selected_object.affected_items[i]
                        items[item].multiplier += selected_object.affected_rates

                    purchase_sound.play()

                    upgrades_shown.remove(selected_object.upgrade_order)

                # Selling the cleared pollution to gain money
                if selected_object == sell_button:
                    money = round(money + pollution_cleared, 1)
                    previous_pollution_cleared = 0
                    pollution_cleared = 0

                # Once the mouse has been released, stop holding the scroll bar
                holding_scroll_bar = False

        # ----------------- Calculations -----------------

        # Calculate the current rate
        rate = 0
        for item in items:
            rate += item.count * item.rate * item.multiplier

        pollution_cleared += rate / 60
        total_pollution_cleared += rate / 60

        # ----------------- Achievements -----------------
        achievement_stage = int(math.log(int(max(1, total_pollution_cleared)), 1000))
        if achievement_stage != previous_achievement_stage:
            achievement_sound.play()

        earth_clicker.stage = min(4, achievement_stage)
        earth_clicker.redraw()

        achievement.text = achievement_messages[min(6, achievement_stage)]

        previous_achievement_stage = achievement_stage

        # ----------------- Upgrade Calculations -----------------
        if money >= UPGRADE_COSTS[UPGRADE_ORDER[min(len(UPGRADE_ORDER)-1, upgrade_count)][0]] \
                [UPGRADE_ORDER[min(len(UPGRADE_ORDER)-1, upgrade_count)][1]] and upgrade_count < len(UPGRADE_ORDER)-1:
            upgrade_count += 1
            upgrades_shown.append(upgrade_count)

        # Move the upgrades in the correct order
        for upgrade in upgrades:
            if upgrade.upgrade_order in upgrades_shown:
                upgrade.move(len(upgrades_shown) - 1 - upgrades_shown.index(upgrade.upgrade_order))

        # ----------------- Formatting information for viewing -----------------

        # Display numbers with abbreviations and correct formatting
        pollution_cleared_digits = len(str(int(pollution_cleared)))

        # Pollution Cleared calculations
        num_power = int(math.log(int(max(1, pollution_cleared)), 1000))
        pollution_cleared_formatted = str(round(pollution_cleared / (1000 ** num_power), 1)) + \
                                             NUMBER_SUFFIX[num_power]

        pollution_cleared_panel.text = "Pollution Cleared: " + \
                                       " " * (6 - pollution_cleared_digits) + \
                                       pollution_cleared_formatted + " lbs"

        # PPS (Pollution cleared Per Second) calculations
        current_pps_digits = len(str(int(pps)))

        num_power = int(math.log(max(1, int(pps)), 1000))
        pps_formatted = str(round(pps / (1000 ** num_power), 1)) + \
                                             NUMBER_SUFFIX[num_power]
        pps_panel.text = "PPS: " + \
                         " " * (6 - current_pps_digits) + pps_formatted

        # Money calculations
        money_digits = len(str(int(money)))

        num_power = int(math.log(int(max(1, money)), 1000))
        money_formatted = str(round(money / (1000 ** num_power), 1)) + \
                                             NUMBER_SUFFIX[num_power]

        money_panel.text = "$: " + \
                           " " * (6 - money_digits) + \
                           money_formatted

        # ----------------- Mouse and Selection -----------------
        mouse_pos = pygame.mouse.get_pos()
        selected_object = get_selected_object(mouse_pos, buttons, items, upgrades)
        colliding_earth = earth_clicker.colliding(mouse_pos)
        if not colliding_earth and hovering_earth:
            hovering_earth = False
            earth_clicker.resize_normal()
        if not hovering_earth and colliding_earth:
            hovering_earth = True
            earth_clicker.hover()

        # ----------------- Scroll Bar Movement -----------------
        if holding_scroll_bar:

            offset = mouse_pos[1]-starting_mouse_y  # The offset in which we need to move the scroll bar
            if (item_base_y_pos > item_min_y_pos or offset < 0) and (item_base_y_pos < item_max_y_pos or offset > 0):

                # Make sure that the scroll bar does not move too far
                if offset > 0:
                    offset = min(offset, item_base_y_pos - item_min_y_pos)
                if offset < 0:
                    offset = max(offset, item_base_y_pos - item_max_y_pos)

                scroll_bar.move(offset)
                item_base_y_pos -= offset

                starting_mouse_y += offset

        # Scroll the items based on the scroll bar's movement
        scroll_items(items, item_base_y_pos)

        # ----------------- Popup Information -----------------

        # Item popups with descriptions about the items
        if type(selected_object) == Item and not selected_object.hidden:
            item_popup = ItemPopup((0, 0, 0, 0),
                                   (selected_object.x - 390, selected_object.y, 390, 100), 0, 0,
                                   "images/building_frame.png",
                                   popup_message=ITEM_INFO[selected_object.item_type])
        elif type(selected_object) == Upgrade and not selected_object.hidden:
            upgrade_popup = UpgradePopup((0, 0, 0, 0),
                                         (selected_object.x + selected_object.width, selected_object.y, 390, 100), 0, 0,
                                         "images/building_frame.png",
                                         UPGRADE_COSTS[selected_object.item_type][selected_object.tier],
                                         popup_message=UPGRADE_INFO[selected_object.item_type][selected_object.tier])
        else:
            item_popup = None
            upgrade_popup = None

        # ----------------- Redrawing and Updating -----------------

        screen.fill(SCREEN_COLOR)

        # Draw stars
        earth_center = earth_clicker.get_center()
        displacement = ((mouse_pos[0] - earth_center[0]) / 2400.0, (mouse_pos[1] - earth_center[1]) / 2400.0)

        for star in stars:
            star.update_position(displacement)
            star.draw(screen, False)

        draw_main_objects_1(screen, selected_object, basic_objects_layer_1, buttons)
        draw_items(screen, selected_object, items, money)
        draw_upgrades(screen, selected_object, upgrades, money, upgrade_count)
        draw_main_objects_2(screen, basic_objects_layer_2)

        earth_clicker.animate()
        sprite_group.draw(screen)
        draw_animated_text(screen, animation_text_list)
        draw_item_popup(screen, item_popup)
        draw_upgrade_popup(screen, upgrade_popup)

        if starting:
            transparency = max(transparency - 1 - (255 - transparency) * 0.1, 0)
            new_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            new_surface.set_alpha(transparency)
            new_surface.fill((0, 0, 0))
            screen.blit(new_surface, (0, 0))

            if transparency == 0:
                starting = False

        # Set the FPS and update
        clock.tick(60)
        pygame.display.update()

        # ----------------- PPS (Pollution cleared Per Second) Calculations -----------------
        time += 1
        if not can_click:
            click_interval += 1
        if click_interval >= max_click_interval:
            can_click = True
            click_interval = 0
        if time == 60:
            pps = pollution_cleared - previous_pollution_cleared
            previous_pollution_cleared = pollution_cleared
            time = 0

        # ----------------- End of Loop -----------------

    # Once the loop has ended, quit the application
    pygame.quit()


# If the mouse is touching an object that can be selected, return it.
# Else, return None for no selected object
def get_selected_object(mouse_pos, buttons, items, upgrades):
    for button in buttons:
        if button.is_selecting(mouse_pos):
            return button

    for item in items:
        if item.is_selecting(mouse_pos):
            return item

    for upgrade in upgrades:
        if not upgrade.hidden and upgrade.is_selecting(mouse_pos):
            return upgrade

    return None


# Scroll the items/machines based on the base y position
def scroll_items(items, item_base_y_pos):
    for item in items:
        item.y = item_base_y_pos + item.item_type * 100


# Draw basic objects such as a rectangle
def draw_basic_objects(surface, objects):
    for basic_object in objects:
        basic_object.draw(surface, False)


# Draw the buttons
def draw_buttons(surface, selected_object, buttons):
    for button in buttons:
        if button == selected_object:
            button.draw(surface, True)
        else:
            button.draw(surface, False)


# buttons and other main components. This draws the first layer
def draw_main_objects_1(screen, selected_object, basic_objects_layer_1, buttons):

    surface1 = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    draw_basic_objects(surface1, basic_objects_layer_1)

    surface3 = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    draw_buttons(surface3, selected_object, buttons)

    surface1.blit(surface3, (0, 0))
    screen.blit(surface1, (0, 0))


# buttons and other main components. This draws the second layer
def draw_main_objects_2(screen, basic_objects_layer_2):
    surface1 = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    draw_basic_objects(surface1, basic_objects_layer_2)
    screen.blit(surface1, (0, 0))


# Draws animated text and moves it every frame
def draw_animated_text(screen, animated_texts):
    surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

    indexes = []  # stuff to be removed
    for i in range(len(animated_texts)):
        animated_text = animated_texts[i]
        animated_text.draw(surface, False)
        remove = animated_text.move()
        if remove:
            indexes.append(i)

    for removal in indexes:
        animated_texts.pop(removal)

    screen.blit(surface, (0, 0))


# Draw all the items and calculate their visibility
def draw_items(screen, selected_object, items, money):
    surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

    for item in items:
        item.hidden = item.item_type != 0 and item.hidden and money < ITEM_PRICES[item.item_type-1]

        item.enough = money >= item.price
        item.draw(surface, selected_object == item)

    screen.blit(surface, (0, 0))


# Draw all the upgrades and calculate their visibility
def draw_upgrades(screen, selected_object, upgrades, money, upgrade_count):
    surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

    for upgrade in upgrades:
        upgrade.hidden = upgrade.purchased or upgrade_count < upgrade.upgrade_order
        upgrade.enough = money >= upgrade.price
        upgrade.draw(surface, selected_object == upgrade)

    screen.blit(surface, (0, 0))


# Draw the item popup if it exists
def draw_item_popup(screen, item_popup):
    if item_popup is None:
        return

    surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    item_popup.draw(surface, False)

    screen.blit(surface, (0, 0))


# Draw the Upgrade popup if it exists
def draw_upgrade_popup(screen, upgrade_popup):
    if upgrade_popup is None:
        return

    surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    upgrade_popup.draw(surface, False)

    screen.blit(surface, (0, 0))


# Run the main function
if __name__ == '__main__':
    main()
