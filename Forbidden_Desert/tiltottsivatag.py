import random
import sys
#import csv
import re
import pygame


players = []
total_sand_tiles = 0
MAX_SAND_LIMIT = 48
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
storm_power = 3
storm_level = 2
global Meteorologist_ability_level
Meteorologist_ability_level = 0
pygame.display.set_caption("Tiltott Sivatag")
selected_tile_offset = None
equipment_items = [
        "Jet Pack",
        "Jet Pack",
        "Dune Blaster",
        "Dune Blaster",
        "Solar Shield",
        "Solar Shield",
        "Terrascope",
        "Terrascope",
        "Secret Water Reserve",
        "Time Throttle"
    ]
storm_position = (2, 2) # initial storm hole position
storm_position_changing = storm_position
visible_items = {
        "compass_x": False,
        "compass_y": False,
        "engine_x": False,
        "engine_y": False,
        "propeller_x": False,
        "propeller_y": False,
        "battery_x": False,
        "battery_y": False
    }
revealed_items = set()
random.shuffle(equipment_items)
items_have = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ROWS = 5
COLS = 5
TILE_SIZE = SCREEN_WIDTH // COLS
real_water_place = {"place_1": False,
                    "place_2": False
            }
explorer_diagonal_index = 0
storm_deck = []



sand_img = pygame.image.load('assets/sand.png')
oasis_img = pygame.image.load('assets/oasis.png')
storm_img = pygame.image.load('assets/storm.png')
spawn_img = pygame.image.load('assets/spawn.png')
player_img = pygame.image.load('assets/player.png')
extraction_zone_img = pygame.image.load('assets/extraction_zone.png')
storm_sand1_img = pygame.image.load('assets/storm_sand1.png')
storm_sand2_img = pygame.image.load('assets/storm_sand2.png')
well_nowater_img = pygame.image.load('assets/well_nowater.png')
well_water_img = pygame.image.load('assets/well_water.png')
ancient_city1_img = pygame.image.load('assets/acinet_city1.png')

extraction_zone_img = pygame.transform.scale(extraction_zone_img, (TILE_SIZE, TILE_SIZE))
sand_img = pygame.transform.scale(sand_img, (TILE_SIZE, TILE_SIZE))
oasis_img = pygame.transform.scale(oasis_img, (TILE_SIZE, TILE_SIZE))
storm_img = pygame.transform.scale(storm_img, (TILE_SIZE, TILE_SIZE))
spawn_img = pygame.transform.scale(spawn_img, (TILE_SIZE, TILE_SIZE))
well_water_img = pygame.transform.scale(well_water_img, (TILE_SIZE, TILE_SIZE))
well_nowater_img = pygame.transform.scale(well_nowater_img, (TILE_SIZE, TILE_SIZE))
ancient_city1_img = pygame.transform.scale(ancient_city1_img, (TILE_SIZE, TILE_SIZE))
player_img = pygame.transform.scale(player_img, (TILE_SIZE // 2.5, TILE_SIZE // 2.5))
storm_sand1_img = pygame.transform.scale(storm_sand1_img, (TILE_SIZE, TILE_SIZE))
storm_sand2_img = pygame.transform.scale(storm_sand2_img, (TILE_SIZE, TILE_SIZE))
font = pygame.font.SysFont(None, 24)


engine_img = pygame.image.load('assets/engine.png')
engine_arrow_img = pygame.image.load('assets/engine_arrow.png')
engine_arrow_y_img = pygame.image.load('assets/engine_arrow_y.png')

propeller_img = pygame.image.load('assets/propeller.png')
propeller_arrow_img = pygame.image.load('assets/propeller_arrow.png')
propeller_arrow_y_img = pygame.image.load('assets/propeller_arrow_y.png')

compass_arrow_img = pygame.image.load('assets/compass_arrow.png')
compass_arrow_y_img = pygame.image.load('assets/compass_arrow_y.png')
compass_img = pygame.image.load('assets/compass.png')

battery_arrows_img = pygame.image.load('assets/battery_arrows.png')
battery_arrows_y_img = pygame.image.load('assets/battery_arrows_y.png')
battery_img = pygame.image.load('assets/battery.png')

engine_img = pygame.transform.scale(engine_img, (TILE_SIZE // 2.5, TILE_SIZE // 2.5))
engine_arrow_img = pygame.transform.scale(engine_arrow_img, (TILE_SIZE, TILE_SIZE))
engine_arrow_y_img = pygame.transform.scale(engine_arrow_y_img, (TILE_SIZE, TILE_SIZE))

propeller_img = pygame.transform.scale(propeller_img, (TILE_SIZE // 2.5, TILE_SIZE // 2.5))
propeller_arrow_img = pygame.transform.scale(propeller_arrow_img, (TILE_SIZE, TILE_SIZE))
propeller_arrow_y_img = pygame.transform.scale(propeller_arrow_y_img, (TILE_SIZE, TILE_SIZE))

compass_arrow_img = pygame.transform.scale(compass_arrow_img, (TILE_SIZE, TILE_SIZE))
compass_arrow_y_img = pygame.transform.scale(compass_arrow_y_img, (TILE_SIZE, TILE_SIZE))
compass_img = pygame.transform.scale(compass_img, (TILE_SIZE // 2.5, TILE_SIZE // 2.5))

battery_arrows_img = pygame.transform.scale(battery_arrows_img, (TILE_SIZE, TILE_SIZE))
battery_arrows_y_img = pygame.transform.scale(battery_arrows_y_img, (TILE_SIZE, TILE_SIZE))
battery_img = pygame.transform.scale(battery_img, (TILE_SIZE // 2.5, TILE_SIZE // 2.5))

PLAYER_OFFSETS = [
    (0.25, 0.25),  # Top-left
    (0.75, 0.25),  # Top-right
    (0.25, 0.75),  # Bottom-left
    (0.75, 0.75),  # Bottom-right
    (0.5, 0.5),    # Center (for solo or 5th player)
]
class Character:
    def __init__(self, name, max_water, action_points, start_pos, icon, sand_remove):
        self.name = name
        self.max_water = max_water
        self.water = max_water
        self.action_points = action_points
        self.position = start_pos
        self.icon = icon
        self.inventory = []
        self.sand_remove = sand_remove
        self.solar_shield_active = False

    def decrease_water(self):
        if self.water > 0:
            self.water -= 1
            print(f"{self.name} has {self.water} water left.")
        if self.water <= 0:
            print(f"Game Over! {self.name} died of thirst.")
            pygame.quit()
            sys.exit()

    def increase_water(self):
        if self.water < self.max_water:
            self.water += 1
            print(f"{self.name} refilled water: {self.water}/{self.max_water}")
    def reset_action_points(self):
        self.action_points = 4  # Reset to full (or specific per character)testin porpuses set to 12
    def move(self, direction, map_tiles):
        if self.action_points <= 0:
            print(f"{self.name} has no action points left and cannot move!")
            out_of_auction = True
            return out_of_auction
        row, col = self.position
        tile = map_tiles[row * COLS + col]
        sand = tile["sand"]
        tile_type = tile["type"]
        if sand >= 2:
            print("invalid move, too much sand")
            return
        if tile_type == 25:
            print("invalid move, there is storm there")
            return
        if direction == "UP" and row > 0:
            row -= 1
        elif direction == "DOWN" and row < 4:  # Assuming a 5x5 grid
            row += 1
        elif direction == "LEFT" and col > 0:
            col -= 1
        elif direction == "RIGHT" and col < 4:
            col += 1
        #for explorer
        elif self.name == "Explorer":
            if direction == "UP_LEFT" and row > 0 and col > 0:
                row -= 1
                col -= 1
            elif direction == "UP_RIGHT" and row > 0 and col < 4:
                row -= 1
                col += 1
            elif direction == "DOWN_LEFT" and row < 4 and col > 0:
                row += 1
                col -= 1
            elif direction == "DOWN_RIGHT" and row < 4 and col < 4:
                row += 1
                col += 1
            else:
                print("Invalid diagonal move!")
                return
        else:
            print("Invalid move!")
            return
        tile = map_tiles[row * COLS + col]
        sand = tile["sand"]
        tile_type = tile["type"]
        if sand >= 2:
            print("invalid move, too much sand")
            return
        if tile_type == 25:
            print("invalid move, there is storm there")
            return


        self.position = (row, col)  # Update position
        self.action_points -= 1
        print(f"{self.name} moved to {self.position}. Action Points left: {self.action_points}")
        update_sand_counter(map_tiles)
    def clean(self, offset, map_tiles):
            if self.action_points <= 0:
                print(f"{self.name} has no action points left and cannot clean!")
                return

            row, col = self.position
            target_row = row + offset[0]
            target_col = col + offset[1]

            if 0 <= target_row < ROWS and 0 <= target_col < COLS:
                index = target_row * COLS + target_col
                tile = map_tiles[index]
                if tile["sand"] > 0:
                    tile["sand"] -= self.sand_remove
                    if tile["sand"] < 0:
                        tile["sand"] = 0
                    self.action_points -= 1
                    print(f"{self.name} cleared sand. Remaining: {tile['sand']}. Action Points left: {self.action_points}")
                    update_sand_counter(map_tiles)
                else:
                    print("No sand to clean.")
    def flip(self, map_tiles, players):
        if self.action_points <= 0:
            print(f"{self.name} has no action points left and cannot explore a tile!")
            return

        row, col = self.position
        tile = map_tiles[row * COLS + col]
        sand = tile["sand"]
        flipped = tile["flipped"]
        tile_type = tile["type"]
        if sand > 0:
            print("There is still sand on the tile")
            return
        if flipped == "yes":
            print("The tile has already been flipped")
            return

        players_on_tile = [player for player in players if player.position == (row, col)]

        tile["flipped"] = "yes"
        self.action_points -= 1
        print(f"{self.name} flipped the tile at ({row}, {col}). Action Points left: {self.action_points}")
        if tile_type == "2" or tile_type == "3":
            if players_on_tile:
                for player in players_on_tile:
                    original_water = player.water
                    player.water = min(player.water + 2, player.max_water)
                    print(f"{player.name} received +2 water ({original_water} → {player.water}).")

        
        if tile_type in range(5, 26) or tile_type == 1:
            giving_items(equipment_items, self)

    def receive_item(self, equipment_items):
        if not equipment_items:
            print("No items left to give.")
            return

        item = equipment_items.pop(0)
        self.inventory.append(item)
        equipment_items.append(item)
        print(f"{self.name} received item: {item}")
    def pick_up_item(self, map_tiles):
        global items_have

        if self.action_points <= 0:
            print(f"{self.name} has no action points left and cannot pick up an item!")
            return

        row, col = self.position
        tile = map_tiles[row * COLS + col]

        if tile.get("item") in ("engine", "compass", "propeller", "battery"):
            picked_item = tile["item"]
            self.inventory.append(picked_item)
            items_have += 1
            tile["item"] = None
            self.action_points -= 1
            print(
                f"{self.name} picked up {picked_item}. Action points left: {self.action_points}. Items collected: {items_have}")
        else:
            print(f"No item to pick up at position ({row}, {col}).")
class Climber(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passenger = None

    def move(self, direction, map_tiles):
        if self.action_points <= 0:
            print(f"{self.name} has no action points left!")
            return

        row, col = self.position

        # Direction handling
        if direction == "UP" and row > 0:
            target = (row - 1, col)
        elif direction == "DOWN" and row < ROWS - 1:
            target = (row + 1, col)
        elif direction == "LEFT" and col > 0:
            target = (row, col - 1)
        elif direction == "RIGHT" and col < COLS - 1:
            target = (row, col + 1)
        else:
            print("Invalid move (out of bounds)")
            return

        new_row, new_col = target
        tile = map_tiles[new_row * COLS + new_col]

        if tile["type"] == 25:
            print("❌ Cannot move into the storm.")
            return

        prev_pos = self.position
        self.position = target
        self.action_points -= 1
        print(f"{self.name} climbed to {self.position}. AP left: {self.action_points}")

        # If a passenger is set and still on the same tile
        if self.passenger and self.passenger.position == prev_pos:
            self.passenger.position = target
            print(f"🧗 {self.passenger.name} followed {self.name} to {target}!")

        self.passenger = None
        update_sand_counter(map_tiles)


def main():
    global items_have, storm_deck, storm_power, Meteorologist_ability_level

    player_count = startdata() #save_file, start_game,
    clock = pygame.time.Clock()
    running = True
    storm_power = 3
    items_have = 0

    map_tiles, extraction_tile = random_tiles()
    starting_point, _, _ = draw_grid(map_tiles, None)

    players = player_creation(player_count, starting_point)

    current_player_index = 0
    current_player = players[current_player_index]
    player_turn_active = True

    while running:
        screen.fill((0, 0, 0))

        _, visible_items, _ = draw_grid(map_tiles, current_player)
        reviling_items(visible_items, map_tiles)
        draw_players(players)
        draw_sand_counter()
        draw_player_info(players)

        pygame.display.flip()

        if player_turn_active:
            player_turn_active = player_input_auction(current_player, map_tiles, players)
        else:
            storm_events(map_tiles, players)
            current_player.solar_shield_active = False
            current_player.reset_action_points()
            Meteorologist_ability_level = 0
            chicken_dinner(players, extraction_tile, items_have)

            current_player_index = (current_player_index + 1) % len(players)
            current_player = players[current_player_index]

            player_turn_active = True

        clock.tick(60)

#control settings
def player_input_auction(player, map_tiles, players):
    global selected_tile_offset
    global explorer_diagonal_index
    global Meteorologist_ability_level

    diagonal_directions = [(-1, 1), (1, 1), (1, -1), (-1, -1)]  # clockwise

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:

            if player.name == "Explorer" and event.key == pygame.K_q:
                selected_tile_offset = diagonal_directions[explorer_diagonal_index]
                print(f"🧭 Explorer selected diagonal direction {selected_tile_offset}")
                explorer_diagonal_index = (explorer_diagonal_index + 1) % 4
                return True
            elif event.key == pygame.K_w:
                selected_tile_offset = (-1, 0)
            elif event.key == pygame.K_s:
                selected_tile_offset = (1, 0)
            elif event.key == pygame.K_a:
                selected_tile_offset = (0, -1)
            elif event.key == pygame.K_d:
                selected_tile_offset = (0, 1)
            elif event.key == pygame.K_x:
                selected_tile_offset = (0, 0)

            elif event.key == pygame.K_ESCAPE:
                print("Selection cleared.")
                selected_tile_offset = None

            elif event.key == pygame.K_f:
                player.flip(map_tiles, players)
                selected_tile_offset = None
                return True


            elif event.key == pygame.K_p:
                player.pick_up_item(map_tiles)
                selected_tile_offset = None
                return True


            elif event.key == pygame.K_t:
                trade_between_players(players)

            elif event.key == pygame.K_u:
                print("Select player to use item (press 1-5):")
                selecting_player = True
                selected_player = None

                while selecting_player:
                    for event_inner in pygame.event.get():
                        if event_inner.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event_inner.type == pygame.KEYDOWN:
                            if pygame.K_1 <= event_inner.key <= pygame.K_5:
                                index = event_inner.key - pygame.K_1
                                if index < len(players):
                                    selected_player = players[index]
                                    print(f"Selected player: {selected_player.name}")
                                    selecting_player = False
                                else:
                                    print("Invalid player selection.")
                            elif event_inner.key == pygame.K_ESCAPE:
                                print("Cancelled player selection.")
                                return True

                if not selected_player.inventory:
                    print(f"{selected_player.name} has no items!")
                    return True

                print(f"{selected_player.name}'s items:")
                for idx, item in enumerate(selected_player.inventory):
                    print(f"{idx + 1}: {item}")

                print("Select item to use (press corresponding number):")
                selecting_item = True

                while selecting_item:
                    for event_item in pygame.event.get():
                        if event_item.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event_item.type == pygame.KEYDOWN:
                            item_index = event_item.key - pygame.K_1
                            if 0 <= item_index < len(selected_player.inventory):
                                selected_item = selected_player.inventory[item_index]
                                print(f"{selected_player.name} is using {selected_item}.")

                                if selected_item == "Jet Pack":
                                    Jet_Pack(selected_player, map_tiles)
                                elif selected_item == "Dune Blaster":
                                    Dune_Blaster(selected_player, map_tiles)
                                elif selected_item == "Solar Shield":
                                    print("Solar Shield activated! (Implement as needed)")
                                    selected_player.inventory.remove("Solar Shield")
                                elif selected_item == "Terrascope":
                                    Terrascope(selected_player, map_tiles)
                                elif selected_item == "Secret Water Reserve":
                                    SWR(selected_player)
                                elif selected_item == "Time Throttle":
                                    Time_Throttle(selected_player)
                                else:
                                    print("Unknown item selected.")
                                selecting_item = False
                            elif event_item.key == pygame.K_ESCAPE:
                                print("Cancelled item selection.")
                                return True
                return True

            elif event.key == pygame.K_m and selected_tile_offset:
                player_attempt_move(player, map_tiles, selected_tile_offset)
                selected_tile_offset = None
                return True

            elif event.key == pygame.K_c and selected_tile_offset:
                player_attempt_clean(player, map_tiles, selected_tile_offset)
                selected_tile_offset = None
                return True

            elif event.key == pygame.K_RETURN:
                print(f"{player.name} ended their turn.")
                selected_tile_offset = None
                return False

            elif player.name == "Water Carrier" and event.key == pygame.K_q:
                picking_up_water(player)
                selected_tile_offset = None
                return True

            elif player.name == "Navigator" and event.key == pygame.K_q:
                moving_players(players, player, map_tiles)
                selected_tile_offset = None
                return True


            elif player.name == "Meteorologist" and event.key == pygame.K_q and Meteorologist_ability_level < storm_power:
                if player.action_points > 0:
                    Meteorologist_ability_level += 1
                    player.action_points -= 1
                    print(f"🌪️ Meteorologist used their ability to reduce the storm.")
                    print(f"⚡ Action Points left: {player.action_points}")
                    print(f"🧮 Storm cards to be drawn at end of round: {storm_power - Meteorologist_ability_level}")
                else:
                    print("🚫 Not enough action points to use this ability.")
                selected_tile_offset = None
                return True

            elif isinstance(player, Climber) and event.key == pygame.K_q:
                print("🥗 Climber ability: choose a player to bring with you.")
                print("Press number key 1–5 to choose a player.")

            elif isinstance(player, Climber) and pygame.K_1 <= event.key <= pygame.K_5:
                index = event.key - pygame.K_1
                if index < len(players):
                    target = players[index]
                    if target == player:
                        print("❌ You can't bring yourself.")
                    elif target.position == player.position:
                        player.passenger = target
                        print(f"✅ {target.name} will move with {player.name} on next move.")
                    else:
                        print(f"❌ {target.name} is not on your tile.")
                return True

    return True


#Abilities
def picking_up_water(player):
    if player.action_points <= 0:
        print("🚫 Not enough action points to pick up water.")
        return
    player_row, player_col = player.position
    print("picking up water")

    # Convert pixel coordinates to grid tile coordinates
    water1 = None
    water2 = None

    if real_water_place["place_1"]:
        x1, y1 = real_water_place["place_1"]
        water1 = (y1 // TILE_SIZE, x1 // TILE_SIZE)

    if real_water_place["place_2"]:
        x2, y2 = real_water_place["place_2"]
        water2 = (y2 // TILE_SIZE, x2 // TILE_SIZE)

    print(f"DEBUG: Player at {player.position}, water1 at {water1}, water2 at {water2}")

    if player.position == water1:
        print("💧 Player is at water well (place 1)")
        player.increase_water()
        player.action_points -= 1
        print(f"{player.name} has {player.water} water. Action Points left: {player.action_points}")

    elif player.position == water2:
        print("💧 Player is at water well (place 2)")
        player.increase_water()
        player.action_points -= 1

    else:
        print("🚫 You're not on a valid water tile.")
def moving_players(players, navigator, map_tiles):
    if navigator.action_points <= 0:
        print("🚫 Not enough action points.")
        return

    print("🧭 Navigator is using their ability.")

    # Step 1: Choose a player to move (not self)
    # Step 1: Choose a player to move (not self)
    movable_players = [p for p in players if p != navigator]
    print("Choose a player to move (press 1–5):")

    selected = None
    selecting = True

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    index = event.key - pygame.K_1
                    if index < len(movable_players):
                        selected = movable_players[index]
                        print(f"👉 Moving {selected.name}")
                        selecting = False
                    else:
                        print("Invalid selection.")
                elif event.key == pygame.K_ESCAPE:
                    print("Cancelled Navigator ability.")
                    return

    moved_steps = 0
    while moved_steps < 3:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                direction_map = {
                    pygame.K_w: (-1, 0),
                    pygame.K_s: (1, 0),
                    pygame.K_a: (0, -1),
                    pygame.K_d: (0, 1),
                    pygame.K_RETURN: "DONE",
                    pygame.K_ESCAPE: "CANCEL"
                }

                key = event.key
                if key in direction_map:
                    if direction_map[key] in ("DONE", "CANCEL"):
                        if direction_map[key] == "CANCEL":
                            print("Cancelled navigator ability.")
                            return
                        elif direction_map[key] == "DONE":
                            print(f"Moved {moved_steps} steps.")
                            navigator.action_points -= 1
                            return

                    offset = direction_map[key]
                    new_row = selected.position[0] + offset[0]
                    new_col = selected.position[1] + offset[1]
                    if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                        index = new_row * COLS + new_col
                        tile = map_tiles[index]
                        if tile["sand"] < 2 and tile["type"] != 25:
                            selected.position = (new_row, new_col)
                            moved_steps += 1
                            print(f"{selected.name} moved to {selected.position} ({moved_steps}/3)")
                            render_game_state(map_tiles, navigator, players)
                        else:
                            print("❌ Can't move there: too much sand or storm.")
                    else:
                        print("❌ Out of bounds.")
    navigator.action_points -= 1
    print(f"Action Points left: {navigator.action_points}")
def render_game_state(map_tiles, current_player, players):
    screen.fill((0, 0, 0))
    _, visible_items, _ = draw_grid(map_tiles, current_player)
    reviling_items(visible_items, map_tiles)
    draw_players(players)
    draw_sand_counter()
    pygame.display.flip()


#displaying
def draw_grid(map_tiles, current_player):
    starting_player_point = None
    extraction_tile = None
    visible_items = {}

    for row in range(ROWS):
        for col in range(COLS):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            tile = map_tiles[row * COLS + col]
            tile_type = tile["type"]
            sand = tile["sand"]

            if tile_type in range(14, 25):
                if tile["flipped"] == "yes":
                    screen.blit(ancient_city1_img, (x, y))
                else:
                    screen.blit(sand_img, (x, y))

            elif tile_type in range(5, 14):
                if tile["flipped"] == "no":
                    screen.blit(sand_img, (x, y))
                else:
                    # Compass clues
                    if tile_type == 5:  # Horizontal (left-right arrows)
                        screen.blit(compass_arrow_img, (x, y))
                        visible_items["compass_y"] = row
                    elif tile_type == 6:  # Vertical (up-down arrows)
                        screen.blit(compass_arrow_y_img, (x, y))
                        visible_items["compass_x"] = col

                    # Engine clues
                    elif tile_type == 7:  # Horizontal (left-right arrows)
                        screen.blit(engine_arrow_img, (x, y))
                        visible_items["engine_y"] = row
                    elif tile_type == 8:  # Vertical (up-down arrows)
                        screen.blit(engine_arrow_y_img, (x, y))
                        visible_items["engine_x"] = col

                    # Propeller clues
                    elif tile_type == 9:  # Horizontal (left-right arrows)
                        screen.blit(propeller_arrow_img, (x, y))
                        visible_items["propeller_y"] = row
                    elif tile_type == 10:  # Vertical (up-down arrows)
                        screen.blit(propeller_arrow_y_img, (x, y))
                        visible_items["propeller_x"] = col

                    # Battery clues
                    elif tile_type == 11:  # Horizontal (left-right arrows)
                        screen.blit(battery_arrows_img, (x, y))
                        visible_items["battery_y"] = row
                    elif tile_type == 12:  # Vertical (up-down arrows)
                        screen.blit(battery_arrows_y_img, (x, y))
                        visible_items["battery_x"] = col

                    # Extraction Zone
                    elif tile_type == 13:
                        screen.blit(extraction_zone_img, (x, y))
                        extraction_tile = (row, col)

            elif tile_type in range(2, 5):
                if tile["flipped"] == "no":
                    screen.blit(oasis_img, (x, y))
                else:
                    if tile_type in (2, 3):
                        screen.blit(well_water_img, (x, y))
                        real_water_place["place_1"] = (x, y)
                    elif tile_type == 4:
                        screen.blit(well_nowater_img, (x, y))
                        real_water_place["place_2"] = (x, y)

            elif tile_type == 25:
                screen.blit(storm_img, (x, y))

            elif tile_type == 1:
                starting_player_point = (row, col)
                if tile["flipped"] == "yes":
                    screen.blit(ancient_city1_img, (x, y))
                else:
                    screen.blit(spawn_img, (x, y))

            # Sand drawing logic
            if sand == 1:
                screen.blit(storm_sand1_img, (x, y))
            elif sand >= 2:
                screen.blit(storm_sand2_img, (x, y))
            if sand >= 3:
                sand_text = font.render(str(sand), True, (255, 255, 255))
                text_rect = sand_text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(sand_text, text_rect)

            # Highlight item tiles
            if tile.get("item") in ("engine", "compass", "propeller", "battery"):
                pygame.draw.rect(screen, (255, 255, 0), (x + 2, y + 2, TILE_SIZE - 4, TILE_SIZE - 4), 3)

            # Item placement
            if tile.get("item") == "engine":
                screen.blit(engine_img, (
                    x + TILE_SIZE // 2 - engine_img.get_width() // 2,
                    y + TILE_SIZE // 2 - engine_img.get_height() // 2))
            elif tile.get("item") == "compass":
                screen.blit(compass_img, (
                    x + TILE_SIZE // 2 - compass_img.get_width() // 2,
                    y + TILE_SIZE // 2 - compass_img.get_height() // 2))
            elif tile.get("item") == "propeller":
                screen.blit(propeller_img, (
                    x + TILE_SIZE // 2 - propeller_img.get_width() // 2,
                    y + TILE_SIZE // 2 - propeller_img.get_height() // 2))
            elif tile.get("item") == "battery":
                screen.blit(battery_img, (
                    x + TILE_SIZE // 2 - battery_img.get_width() // 2,
                    y + TILE_SIZE // 2 - battery_img.get_height() // 2))

    # Draw selection box around selected tile
    if selected_tile_offset and current_player:
        row, col = current_player.position
        target_row = row + selected_tile_offset[0]
        target_col = col + selected_tile_offset[1]
        if 0 <= target_row < ROWS and 0 <= target_col < COLS:
            x = target_col * TILE_SIZE
            y = target_row * TILE_SIZE
            pygame.draw.rect(screen, (255, 0, 0), (x, y, TILE_SIZE, TILE_SIZE), 3)

    return starting_player_point, visible_items, extraction_tile
def draw_players(players):
    for player in players:
        if not isinstance(player.position, tuple):
            print(f"HIBA: {player.name} pozíciója nem tuple: {player.position} (type={type(player.position)})")
            if isinstance(player.position, dict) and "row" in player.position and "col" in player.position:
                player.position = (player.position["row"], player.position["col"])
            else:
                player.position = (0, 0)  # fallback pozíció

    tile_groups = {}
    for player in players:
        pos = player.position
        if pos not in tile_groups:
            tile_groups[pos] = []
        tile_groups[pos].append(player)

    # Draw grouped players with offsets
    for tile_pos, group in tile_groups.items():
        row, col = tile_pos
        for index, player in enumerate(group):
            if index >= len(PLAYER_OFFSETS):
                continue  # Avoid going out of bounds (max 5 supported)
            offset_x, offset_y = PLAYER_OFFSETS[index]
            x = col * TILE_SIZE + int(offset_x * TILE_SIZE) - player.icon.get_width() // 2
            y = row * TILE_SIZE + int(offset_y * TILE_SIZE) - player.icon.get_height() // 2
            screen.blit(player.icon, (x, y))
def draw_sand_counter():
    sand_text = font.render(f"Sand tiles: {total_sand_tiles}/{MAX_SAND_LIMIT}", True, (255, 255, 0))
    screen.blit(sand_text, (10, SCREEN_HEIGHT - 30))
def random_tiles():
    base_tiles = [1, 2, 3, 4] + list(range(5, 25))  # 24 tile types
    random.shuffle(base_tiles)

    base_tiles.insert(12, 25)  # storm tile in the center

    map_tiles = {}
    extraction_tile_pos = None  # Initialize this clearly

    for index, tile_type in enumerate(base_tiles):
        row, col = divmod(index, COLS)
        map_tiles[index] = {
            "type": tile_type,
            "original_type": tile_type,
            "sand": 0,
            "flipped": "no",
            "item": None
        }
        # Clearly capture the extraction tile position
        if tile_type == 13:
            extraction_tile_pos = (row, col)

    for row in range(5):
        for col in range(5):
            index = row * 5 + col
            is_main_diag = row == col
            is_anti_diag = row + col == 4
            is_center = row == 2 and col == 2
            if (is_main_diag or is_anti_diag) and not is_center:
                map_tiles[index]["sand"] += 1

    update_sand_counter(map_tiles)

    # Return BOTH map_tiles AND extraction_tile position
    return map_tiles, extraction_tile_pos
def tint_surface_player(surface, tint_color):
    tinted = surface.copy()
    tinted.fill(tint_color, special_flags=pygame.BLEND_RGB_MULT)
    return tinted
def reviling_items(visible_items, map_tiles):
    items = ["engine", "compass", "propeller", "battery"]

    for item in items:
        x_key = f"{item}_x"
        y_key = f"{item}_y"

        if item not in revealed_items:
            if visible_items.get(x_key) is not None and visible_items.get(y_key) is not None:
                # Clue with horizontal arrows gives ROW, vertical arrows gives COLUMN
                row = visible_items[y_key]   # Horizontal clue (left-right arrows) gives the row
                col = visible_items[x_key]   # Vertical clue (up-down arrows) gives the column

                index = row * COLS + col
                map_tiles[index]["item"] = item
                revealed_items.add(item)
def draw_player_info(players):
    start_x = 10
    start_y = SCREEN_HEIGHT - 90  # adjust according to available space
    line_height = 20
    font_info = pygame.font.SysFont(None, 20)

    for i, player in enumerate(players):
        player_info = f"Player {i + 1}: {player.name} | Water: {player.water}/{player.max_water} | AP: {player.action_points}"
        text_surface = font_info.render(player_info, True, (255, 255, 255))
        screen.blit(text_surface, (start_x, start_y + i * line_height))


#idk
def player_attempt_move(player, map_tiles, offset):
    direction_map = {
        (-1, 0): "UP",
        (1, 0): "DOWN",
        (0, -1): "LEFT",
        (0, 1): "RIGHT"
    }
    diagonal_map = {
        (-1, -1): "UP_LEFT",
        (-1, 1): "UP_RIGHT",
        (1, -1): "DOWN_LEFT",
        (1, 1): "DOWN_RIGHT"
    }

    if offset in direction_map:
        direction = direction_map[offset]
        player.move(direction, map_tiles)

    elif player.name == "Explorer" and offset in diagonal_map:
        direction = diagonal_map[offset]
        player.move(direction, map_tiles)

    else:
        print("❌ Invalid move offset.")

def player_attempt_clean(player, map_tiles, offset):
    player.clean(offset, map_tiles)
def giving_items(equipment_items, player):
    player.receive_item(equipment_items)
def all_players_on_tile(players, tile_position):
    return all(player.position == tile_position for player in players)

#items
def SWR(player):
    if "Secret Water Reserve" in player.inventory:
        player.inventory.remove("Secret Water Reserve")
        player.water = min(player.water + 2, player.max_water)
        print(f"Secret Water Reserve used by {player.name}. Water: {player.water}/{player.max_water}")
    else:
        print(f"{player.name} doesn't have Secret Water Reserve!")
def Time_Throttle(player):
    if "Time Throttle" in player.inventory:
        player.inventory.remove("Time Throttle")
        player.action_points += 2
        print(f"Time Throttle used by {player.name}. AP: {player.action_points}")
    else:
        print(f"{player.name} doesn't have Time Throttle!")
def Dune_Blaster(player, map_tiles):
    if "Dune Blaster" not in player.inventory:
        print(f"{player.name} doesn't have a Dune Blaster!")
        return

    if player.action_points <= 0:
        print(f"{player.name} has no action points left!")
        return

    print("Select tile to blast sand from with WASD keys, then press 'B' to activate. ESC to cancel.")
    selecting_tile = True
    offset = [0, 0]

    while selecting_tile:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    offset = [-1, 0]
                elif event.key == pygame.K_s:
                    offset = [1, 0]
                elif event.key == pygame.K_a:
                    offset = [0, -1]
                elif event.key == pygame.K_d:
                    offset = [0, 1]
                elif event.key == pygame.K_b:
                    row, col = player.position
                    target_row = row + offset[0]
                    target_col = col + offset[1]

                    if 0 <= target_row < ROWS and 0 <= target_col < COLS:
                        index = target_row * COLS + target_col
                        tile = map_tiles[index]

                        if tile["sand"] > 0:
                            tile["sand"] = 0  # Removes all sand
                            player.action_points -= 1
                            player.inventory.remove("Dune Blaster")
                            print(f"{player.name} used Dune Blaster at ({target_row}, {target_col}). Sand cleared. AP left: {player.action_points}")
                            update_sand_counter(map_tiles)
                        else:
                            print(f"No sand on tile at ({target_row}, {target_col})!")
                    else:
                        print("Invalid tile chosen. Out of bounds.")

                    selecting_tile = False  # Finish selection after usage

                elif event.key == pygame.K_ESCAPE:
                    print("Cancelled Dune Blaster.")
                    selecting_tile = False

        # Render feedback
        render_game_state(map_tiles, player, players)
        target_row = player.position[0] + offset[0]
        target_col = player.position[1] + offset[1]
        if 0 <= target_row < ROWS and 0 <= target_col < COLS:
            pygame.draw.rect(screen, (255, 0, 0),
                             (target_col * TILE_SIZE, target_row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)
        pygame.display.flip()
def Jet_Pack(player, map_tiles):
    if "Jet Pack" not in player.inventory:
        print(f"{player.name} doesn't have a Jet Pack!")
        return


    choosing_tile = True
    target_pos = list(player.position)

    print("Use WASD keys to move your target location, press ENTER to confirm.")

    while choosing_tile:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and target_pos[0] > 0:
                    target_pos[0] -= 1
                elif event.key == pygame.K_s and target_pos[0] < ROWS - 1:
                    target_pos[0] += 1
                elif event.key == pygame.K_a and target_pos[1] > 0:
                    target_pos[1] -= 1
                elif event.key == pygame.K_d and target_pos[1] < COLS - 1:
                    target_pos[1] += 1
                elif event.key == pygame.K_RETURN:
                    index = target_pos[0] * COLS + target_pos[1]
                    tile = map_tiles[index]

                    if tile["type"] != 25:
                        player.position = tuple(target_pos)
                        player.inventory.remove("Jet Pack")
                        print(f"{player.name} used Jet Pack to fly to {player.position}. AP left: {player.action_points}")
                        update_sand_counter(map_tiles)
                    else:
                        print("Cannot fly directly into the storm!")

                    choosing_tile = False

        # Render selection rectangle
        render_game_state(map_tiles, player, players)
        pygame.draw.rect(screen, (0, 255, 0), (target_pos[1] * TILE_SIZE, target_pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)
        pygame.display.flip()
def Terrascope(player, map_tiles):
    if "Terrascope" not in player.inventory:
        print(f"{player.name} doesn't have a Terrascope!")
        return

    choosing_tile = True
    target_pos = list(player.position)

    print("Use WASD keys to select a tile to peek, press ENTER to confirm.")

    while choosing_tile:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and target_pos[0] > 0:
                    target_pos[0] -= 1
                elif event.key == pygame.K_s and target_pos[0] < ROWS - 1:
                    target_pos[0] += 1
                elif event.key == pygame.K_a and target_pos[1] > 0:
                    target_pos[1] -= 1
                elif event.key == pygame.K_d and target_pos[1] < COLS - 1:
                    target_pos[1] += 1
                elif event.key == pygame.K_RETURN:
                    index = target_pos[0] * COLS + target_pos[1]
                    tile = map_tiles[index]

                    if tile["type"] != 25 and tile["flipped"] == "no":
                        tile_type = tile["type"]
                        if tile_type == 1:
                            tile_name = "Starting Tile"
                        elif tile_type in range(2, 5):
                            tile_name = "Possible Water (Oasis)"
                        elif tile_type in range(5, 14):
                            clues = {
                                5: "Compass Clue (horizontal)", 6: "Compass Clue (vertical)",
                                7: "Engine Clue (horizontal)", 8: "Engine Clue (vertical)",
                                9: "Propeller Clue (horizontal)", 10: "Propeller Clue (vertical)",
                                11: "Battery Clue (horizontal)", 12: "Battery Clue (vertical)",
                                13: "Extraction Zone"
                            }
                            tile_name = clues.get(tile_type, "Unknown Clue")
                        elif tile_type in range(14, 25):
                            tile_name = "Ancient City"
                        else:
                            tile_name = "Unknown Tile"

                        print(f"Terrascope peek: The selected tile at {tuple(target_pos)} is '{tile_name}'.")
                        player.inventory.remove("Terrascope")
                    elif tile["flipped"] == "yes":
                        print("Tile already flipped! Choose another tile.")
                    else:
                        print("Cannot peek at the storm!")

                    choosing_tile = False

        # Render selection rectangle
        render_game_state(map_tiles, player, players)
        pygame.draw.rect(screen, (0, 255, 0),
                         (target_pos[1] * TILE_SIZE, target_pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)
        pygame.display.flip()


#game things
def startdata():
    '''
    save_file = "test"
    start_game = True
    player_count = 2
    return save_file, start_game, player_count
    '''
    while True:
        try:
            player_count = int(input("How many players are going to play (2-5)? "))
            if player_count in range(2, 6):
                return player_count
            else:
                print("Invalid number, must be between 2 and 5. Please try again.")
        except ValueError:
            print("Invalid input, please enter a numeric value (2-5).")

    '''
    save_file_pattern = r'.+\.csv'
    while True:
        chess_start = input("Would you like to start a continue a game? (type: START or CONTINUE) ")
        if chess_start.upper().strip() == "START" or chess_start.upper().strip() == "CONTINUE":
            break
        else:
            print("Invalid input. Please type 'START' or 'CONTINUE'.")
    while True:
        if chess_start.upper().strip() == "START":
            save_file = input("What should be the new game name? ")
            if not re.fullmatch(save_file_pattern, save_file):
                save_file += ".csv"
                print(save_file)
            if re.fullmatch(save_file_pattern, save_file):
                print("choosing save file location was successful ")
                start_game = True
                while True:
                    player_count = int(input("How many players are playing? (type a number 2-5)"))
                    if 1 < player_count < 6:
                        return save_file, start_game, player_count

        elif chess_start.upper().strip() == "CONTINUE":
            filename = input("What is your file name? ")
            if not re.fullmatch(save_file_pattern, filename):
                filename += ".csv"
            if re.fullmatch(save_file_pattern, filename):
                try:
                    with open(filename, "r") as _:
                        print(f"Successfully loaded the game from {filename}")
                        start_game = False
                        player_count = 0
                        return filename, start_game, player_count
                except FileNotFoundError:
                    sys.exit(f"Could not read {filename}")

        else:
        print("Invalid input. Please type 'START' or 'CONTINUE'.")'''
def player_creation(player_count, starting_player_point):
    character_library = {
        "Explorer": {
            "max_water": 4,
            "action_points": 4,
            "sand_remove": 1,
            "move": 1,
            "ability": "Can move and clear sand diagonally."
        },
        "Climber": {
            "max_water": 4,
            "action_points": 4,
            "sand_remove": 1,
            "move": 1,
            "ability": "Can move through blocked tiles and take others with them."
        },
        "Archeologist": {
            "max_water": 4,
            "action_points": 4,
            "sand_remove": 2,
            "move": 1,
            "ability": "Can remove 2 sand per action."
        },
        "Meteorologist": {
            "max_water": 4,
            "action_points": 4,
            "sand_remove": 1,
            "move": 1,
            "ability": "Can spend actions to reduce storm card draws."
        },
        "Navigator": {
            "max_water": 4,
            "action_points": 4,
            "sand_remove": 1,
            "move": 1,
            "ability": "Can move other players up to 3 tiles per action."
        },
        "Water Carrier": {
            "max_water": 5,
            "action_points": 4,
            "sand_remove": 1,
            "move": 1,
            "ability": "Can collect extra water and give it to others remotely."
        },
    }
    player_colors = [
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (255, 255, 0),  # Yellow
        (255, 165, 0),  # Orange
        (128, 0, 128),  # Purple
    ]
    x, y = starting_player_point
    character_names = random.sample(list(character_library), player_count)
    players = []

    character_classes = {
        "Climber": Climber,
        # Add other special classes as necessary
    }

    for name in character_names:
        tint = player_colors[len(players)]
        icon = tint_surface_player(player_img, tint)
        data = character_library[name]

        cls = character_classes.get(name, Character)
        player = cls(
            name=name,
            max_water=data["max_water"],
            action_points=data["action_points"],
            start_pos=(x, y),
            icon=icon,
            sand_remove=data["sand_remove"]  # added sand_remove here
        )

        player.move_ability = data["move"]
        player.ability = data["ability"]
        players.append(player)

    return players
def chicken_dinner(player, dinner_tile, items_have):
    if all_players_on_tile(players, dinner_tile) and items_have == 4:
        print("🎉 You won the game!")
        pygame.quit()
        sys.exit()
def update_sand_counter(map_tiles):
    global total_sand_tiles
    total_sand_tiles = 0  # reset at the start
    for tile in map_tiles.values():
        total_sand_tiles += tile["sand"]

    if total_sand_tiles > MAX_SAND_LIMIT:
        print("Game over! Too much sand has accumulated!")
        pygame.quit()
        sys.exit()
def trade_between_players(players):
    print("📦 Trade Menu: Choose two players to trade.")

    # Step 1: Select the player who is giving
    print("Select the player who will GIVE:")
    for i, p in enumerate(players):
        print(f"{i + 1}. {p.name} (Water: {p.water}, Items: {p.inventory})")

    giver = None
    receiver = None

    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                giver_index = event.key - pygame.K_1
                if 0 <= giver_index < len(players):
                    giver = players[giver_index]
                    selecting = False
                elif event.key == pygame.K_ESCAPE:
                    print("❌ Trade cancelled.")
                    return

    # Step 2: Select the player who will receive
    print(f"Now select who receives from {giver.name}:")
    for i, p in enumerate(players):
        if p != giver:
            print(f"{i + 1}. {p.name} (Water: {p.water}, Items: {p.inventory})")

    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                receiver_index = event.key - pygame.K_1
                if 0 <= receiver_index < len(players) and players[receiver_index] != giver:
                    receiver = players[receiver_index]
                    selecting = False
                elif event.key == pygame.K_ESCAPE:
                    print("❌ Trade cancelled.")
                    return

    # Check: Same tile
    if giver.position != receiver.position:
        print("❌ Both players must be on the same tile to trade!")
        return

    # Step 3: Choose trade type
    print(f"🤝 {giver.name} and {receiver.name} are trading.")
    print("Press I to transfer an item, W to transfer 1 water. ESC to cancel.")

    trading = True
    while trading:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i and giver.inventory:
                    print("Choose item to give:")
                    for i, item in enumerate(giver.inventory):
                        print(f"{i + 1}. {item}")

                    selecting_item = True
                    while selecting_item:
                        for e in pygame.event.get():
                            if e.type == pygame.KEYDOWN:
                                item_index = e.key - pygame.K_1
                                if 0 <= item_index < len(giver.inventory):
                                    item = giver.inventory.pop(item_index)
                                    receiver.inventory.append(item)
                                    print(f"✅ {giver.name} gave {item} to {receiver.name}.")
                                    selecting_item = False
                                    trading = False
                                    break
                                elif e.key == pygame.K_ESCAPE:
                                    print("❌ Item trade cancelled.")
                                    selecting_item = False
                                    break

                elif event.key == pygame.K_w:
                    if giver.water > 0 and receiver.water < receiver.max_water:
                        giver.water -= 1
                        receiver.water += 1
                        print(f"💧 {giver.name} gave 1 water to {receiver.name}.")
                    else:
                        print("❌ Cannot trade water. Check water limits.")
                    trading = False

                elif event.key == pygame.K_ESCAPE:
                    print("❌ Trade cancelled.")
                    trading = False


#new storm
def storm_card(storm_deck):
    storm_deck_o = [
        # Storm Moves 1 space
        "Storm Up 1", "Storm Down 1", "Storm Left 1", "Storm Right 1",
        "Storm Up 1", "Storm Down 1",

        # Storm Moves 2 spaces
        "Storm Left 2", "Storm Right 2", "Storm Up 2", "Storm Down 2",
        "Storm Left 2", "Storm Right 2",

        # Storm Moves 3 spaces (max)
        "Storm Up 3", "Storm Down 3", "Storm Right 3",

        # Sun Beats Down
        "Sun Beats Down", "Sun Beats Down", "Sun Beats Down", "Sun Beats Down",

        # Storm Picks Up
        "Picks Up", "Picks Up", "Picks Up",

        # Equipment: None (do nothing)
        "None", "None", "None", "None", "None"]
    if len(storm_deck) == 0:  # nincsen kartya
        random.shuffle(storm_deck_o)
        return storm_deck_o

    elif len(storm_deck) < storm_power:  # nincs eleg kartya
        random.shuffle(storm_deck_o)
        storm_deck_filtered = storm_deck_o.copy()
        for item in storm_deck:
            if item in storm_deck_filtered:
                storm_deck_filtered.remove(item)

        merged = storm_deck + storm_deck_filtered
        random.shuffle(merged)
        return merged
def storm(storm_deck, storm_power):
    if len(storm_deck) < storm_power:
        storm_deck = storm_card(storm_deck)

    drawn_cards = []
    for _ in range(storm_power):
        if storm_deck:
            drawn_cards.append(storm_deck.pop(0))
    return drawn_cards
def storm_events(map_tiles, players):
    global storm_deck, storm_power

    effective_storm_power = max(0, storm_power - Meteorologist_ability_level)
    if Meteorologist_ability_level > 0:
        print(f"⚠️ Storm draw count this round (after Meteorologist reduction): {effective_storm_power}")
    storm_events_cards = storm(storm_deck, effective_storm_power)

    for card in storm_events_cards:
        print(f"🃏 Storm card: {card}")

        if card == "None":
            continue
        elif card == "Sun Beats Down":
            sun_beats_down(players)
        elif card == "Picks Up":
            storm_pick_up(storm_power, Meteorologist_ability_level)
        elif card.startswith("Storm"):
            match = re.match(r"Storm (Up|Down|Left|Right) (\d)", card)
            if match:
                direction = match.group(1)
                amount = int(match.group(2))
                storm_movement(direction, amount, map_tiles, players)
def storm_movement(direction, amount, map_tiles, players):
    global storm_position_changing

    row, col = storm_position_changing

    for _ in range(amount):
        if direction == "Down":
            if row + 1 >= ROWS:
                break
            new_row, new_col = row + 1, col
        elif direction == "Up":
            if row - 1 < 0:
                break
            new_row, new_col = row - 1, col
        elif direction == "Right":
            if col + 1 >= COLS:
                break
            new_row, new_col = row, col + 1
        elif direction == "Left":
            if col - 1 < 0:
                break
            new_row, new_col = row, col - 1
        else:
            print("❌ Invalid direction!")
            return

        index1 = row * COLS + col
        index2 = new_row * COLS + new_col

        # Swap the tiles
        map_tiles[index1], map_tiles[index2] = map_tiles[index2], map_tiles[index1]

        # Swap players on the tiles too
        for player in players:
            if player.position == (row, col):
                player.position = (new_row, new_col)
                #print(f"🌪️ {player.name} moved with the storm from {(row, col)} to {(new_row, new_col)}.")
            elif player.position == (new_row, new_col):
                player.position = (row, col)
                #print(f"🌪️ {player.name} moved with the storm from {(new_row, new_col)} to {(row, col)}.")

        if map_tiles[index1]["type"] != 25:
            map_tiles[index1]["sand"] += 1

        # Update storm position
        storm_position_changing = (new_row, new_col)
        row, col = new_row, new_col
        update_sand_counter(map_tiles)


def storm_pick_up(storm_level, Meteorologist_ability_level):
    global storm_power
    if 1 < storm_level <= 6:
        storm_power = 3
    elif 6 < storm_level <= 10:
        storm_power = 4
    elif 10 < storm_level <= 13:
        storm_power = 5
    elif 13 < storm_level:
        storm_power = 6
    storm_power = storm_power - Meteorologist_ability_level
    return
def sun_beats_down(players):
    print("🔥 Sun Beats Down! Each player must decide to use a Solar Shield if they have one.")

    for player in players:
        if player.solar_shield_active:
            print(f"🛡️ {player.name} is protected by Solar Shield.")
            continue

        if "Solar Shield" in player.inventory:
            print(f"{player.name} has a Solar Shield. Use it? (Y = yes, N = no)")
            deciding = True
            while deciding:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            player.inventory.remove("Solar Shield")
                            player.solar_shield_active = True
                            print(f"{player.name} activated Solar Shield!")
                            deciding = False
                        elif event.key == pygame.K_n:
                            player.decrease_water()
                            deciding = False
                        elif event.key == pygame.K_ESCAPE:
                            print("Cancelling decision. Losing water by default.")
                            player.decrease_water()
                            deciding = False
        else:
            player.decrease_water()

if __name__ == '__main__':
    main()
