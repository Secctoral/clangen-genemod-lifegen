from random import choice, randrange
from re import sub
from typing import Optional
from .Screens import Screens

import pygame
import pygame_gui
from pygame_gui.core import ObjectID

import scripts.screens.screens_core.screens_core
from scripts.cat.cats import create_example_cats, create_cat, Cat
from scripts.cat.names import names
from scripts.cat.genotype import Genotype
from scripts.cat.phenotype import Phenotype
from scripts.cat.skills import Skill, SkillPath
from scripts.cat.pelts import Pelt
from scripts.clan import Clan
from scripts.game_structure import image_cache
from scripts.game_structure.game_essentials import (
    game
)
from scripts.game_structure.ui_elements import (
    UIImageButton,
    UISpriteButton,
    UISurfaceImageButton,
)
from scripts.patrol.patrol import Patrol
from scripts.utility import get_text_box_theme, ui_scale, ui_scale_blit, generate_sprite
from scripts.utility import ui_scale_dimensions
from .Screens import Screens
from ..cat.sprites import sprites
from ..game_structure.screen_settings import MANAGER, screen
from ..game_structure.windows import SymbolFilterWindow
from ..ui.generate_box import get_box, BoxStyles
from ..ui.generate_button import ButtonStyles, get_button_dict
from ..ui.get_arrow import get_arrow
from ..ui.icon import Icon

class MakeClanScreen(Screens):
    # UI images
    clan_frame_img = pygame.transform.scale(pygame.image.load(
        'resources/images/pick_clan_screen/clan_name_frame.png').convert_alpha(), (432, 100))
    name_clan_img = pygame.transform.scale(pygame.image.load(
        'resources/images/pick_clan_screen/name_clan_light.png').convert_alpha(), (1600, 1400))
    leader_img = pygame.transform.scale(pygame.image.load(
        'resources/images/pick_clan_screen/choose cat.png').convert_alpha(), (1600, 1400))
    leader_img_dark = pygame.transform.scale(pygame.image.load(
        'resources/images/pick_clan_screen/choose cat dark.png').convert_alpha(), (1600, 1400))
    deputy_img = pygame.transform.scale(pygame.image.load(
        'resources/images/pick_clan_screen/deputy_light.png').convert_alpha(), (1600, 1400))
    medic_img = pygame.transform.scale(pygame.image.load(
        'resources/images/pick_clan_screen/med_light.png').convert_alpha(), (1600, 1400))
    clan_img = pygame.transform.scale(pygame.image.load(
        'resources/images/pick_clan_screen/clan_light.png').convert_alpha(), (1600, 1400))
    bg_preview_border = pygame.transform.scale(
        pygame.image.load("resources/images/bg_preview_border.png").convert_alpha(), (466, 416))
    
    your_name_img = pygame.transform.scale(pygame.image.load(
        'resources/images/pick_clan_screen/Your name screen.png').convert_alpha(), (1600, 1400))
    your_name_img_dark = pygame.transform.scale(pygame.image.load(
        'resources/images/pick_clan_screen/Your name screen darkmode.png').convert_alpha(), (1600, 1400))
    your_name_txt1 = pygame.transform.scale(pygame.image.load(
        'resources/images/pick_clan_screen/your name text1.png').convert_alpha(), (796, 52))
    your_name_txt2 = pygame.transform.scale(pygame.image.load(
        'resources/images/pick_clan_screen/your name text2.png').convert_alpha(), (536, 52))
    
    #images for the customizing screen
    # sprite_preview_bg = pygame.transform.scale(pygame.image.load(
    #     'resources/images/sprite_preview.png').convert_alpha(), (1600, 1400))
    
    # sprite_preview_bg_dark = pygame.transform.scale(pygame.image.load(
    #     'resources/images/sprite_preview_dark.png').convert_alpha(), (1600, 1400))
    
    # poses_bg = pygame.transform.scale(pygame.image.load(
    #     'resources/images/poses_bg.png').convert_alpha(), (1600, 1400))
    
    # poses_bg_dark = pygame.transform.scale(pygame.image.load(
    #     'resources/images/poses_bg_dark.png').convert_alpha(), (1600, 1400))
    
    # choice_bg = pygame.transform.scale(pygame.image.load(
    #     'resources/images/custom_choice_bg.png').convert_alpha(), (1600, 1400))
    
    # choice_bg_dark = pygame.transform.scale(pygame.image.load(
    #     'resources/images/custom_choice_bg_dark.png').convert_alpha(), (1600, 1400))



    # This section holds all the information needed
    game_mode = 'expanded'  # To save the users selection before conformation.
    clan_name = ""  # To store the clan name before conformation
    leader = None  # To store the clan leader before conformation
    deputy = None
    med_cat = None
    members = []
    elected_camp = None
    your_cat = None

    # holds the symbol we have selected
    symbol_selected = None
    tag_list_len = 0
    # Holds biome we have selected
    biome_selected = None
    selected_camp_tab = 1
    selected_season = None
    # Camp number selected
    camp_num = "1"
    # Holds the cat we have currently selected.
    selected_cat = None
    # Hold which sub-screen we are on
    sub_screen = "game mode"
    # To hold the images for the sections. Makes it easier to kill them
    elements = {}
    tabs = {}
    symbol_buttons = {}

    # used in symbol screen only - parent container is in element dict
    text = {}

    def __init__(self, name="make_clan_screen"):
        super().__init__(name)
        # current page for symbol choosing
        self.current_page = 1

        self.rolls_left = game.config["clan_creation"]["rerolls"]
        self.menu_warning = None

    def screen_switches(self):

        # Reset variables
        self.game_mode = 'expanded'
        self.clan_name = ""
        self.selected_camp_tab = 1
        self.biome_selected = None
        self.selected_season = "Newleaf"
        self.symbol_selected = None
        self.choosing_rank = None
        self.leader = None  # To store the Clan leader before conformation
        self.deputy = None
        self.med_cat = None
        self.members = []
        self.clan_size = "medium"
        self.clan_age = "established"
        
        self.custom_cat = None
        self.elements = {}
        self.pname="SingleColour"
        self.colour="WHITE"
        self.white_patches=None
        self.eye_color="BLUE"
        self.eye_colour2=None
        self.tortiebase=None
        self.tortiecolour=None
        self.pattern=None
        self.tortiepattern=None
        self.vitiligo=None
        self.points=None
        self.paralyzed=False
        self.opacity=100
        self.scars=[]
        self.tint="None"
        self.skin="BLACK"
        self.white_patches_tint="None"
        self.kitten_sprite=0
        self.reverse=False
        self.skill = "Random"
        self.accessories=[]
        self.inventory = []
        self.sex = "male"
        self.personality = "troublesome"
        self.accessory = None
        self.permanent_condition = None
        self.preview_age = "kitten"
        self.page = 0
        self.adolescent_pose = 0
        self.adult_pose = 0
        self.elder_pose = 0
        self.faith = "flexible"
        game.choose_cats = {}
        self.skills = []
        for skillpath in SkillPath:
            for skill in skillpath.value:
                self.skills.append(skill)

        # Buttons that appear on every screen.
        self.menu_warning = pygame_gui.elements.UITextBox(
            "Note: going back to main menu resets the generated cats.",
            ui_scale(pygame.Rect((25, 25), (600, -1))),
            object_id=get_text_box_theme("#text_box_22_horizleft"),
            manager=MANAGER,
        )
        self.main_menu = UISurfaceImageButton(
            ui_scale(pygame.Rect((25, 50), (153, 30))),
            get_arrow(3) + " Main Menu",
            get_button_dict(ButtonStyles.SQUOVAL, (153, 30)),
            manager=MANAGER,
            object_id="@buttonstyles_squoval",
            starting_height=1,
        )
        create_example_cats()

        #for i in range(12):
        #    print("")
        #    print(game.choose_cats[i].genotype.agouti)

        # self.worldseed = randrange(10000)
        self.open_name_clan()

    def handle_event(self, event):
        if self.sub_screen == 'customize cat':
            self.handle_customize_cat_event(event)
        elif event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.main_menu:
                self.change_screen('start screen')
            if self.sub_screen == 'name clan':
                self.handle_name_clan_event(event)
            elif self.sub_screen == 'choose name':
                self.handle_choose_name_event(event)
            elif self.sub_screen == 'choose leader':
                self.handle_choose_leader_event(event)
            elif self.sub_screen == 'choose camp':
                self.handle_choose_background_event(event)
            elif self.sub_screen == "choose symbol":
                self.handle_choose_symbol_event(event)
            elif self.sub_screen == "saved screen":
                self.handle_saved_clan_event(event)
        
        elif event.type == pygame.KEYDOWN and game.settings['keybinds']:
            if self.sub_screen == 'name clan':
                self.handle_name_clan_key(event)
            elif self.sub_screen == "choose camp":
                self.handle_choose_background_key(event)
            elif self.sub_screen == "saved screen" and (
                event.key == pygame.K_RETURN or event.key == pygame.K_RIGHT
            ):
                self.change_screen("start screen")

    def handle_name_clan_event(self, event):
        if event.ui_element == self.elements["random"]:
            self.elements["name_entry"].set_text(self.random_clan_name())
        elif event.ui_element == self.elements["reset_name"]:
            self.elements["name_entry"].set_text("")
        elif event.ui_element == self.elements["next_step"]:
            new_name = sub(
                r"[^A-Za-z0-9 ]+", "", self.elements["name_entry"].get_text()
            ).strip()
            if not new_name:
                self.elements["error"].set_text("Your Clan's name cannot be empty")
                self.elements["error"].show()
                return
            if new_name.casefold() in [
                clan.casefold() for clan in game.switches["clan_list"]
            ]:
                self.elements["error"].set_text("A Clan with that name already exists.")
                self.elements["error"].show()
                return
            self.clan_name = new_name
            self.open_choose_leader()
        elif event.ui_element == self.elements["previous_step"]:
            self.clan_name = ""
            self.change_screen('start screen')
        elif event.ui_element == self.elements['small']:
            self.elements['small'].disable()
            self.elements['medium'].enable()
            self.elements['large'].enable()
            self.clan_size = "small"
        elif event.ui_element == self.elements['medium']:
            self.elements['small'].enable()
            self.elements['medium'].disable()
            self.elements['large'].enable()
            self.clan_size = "medium"
        elif event.ui_element == self.elements['large']:
            self.elements['small'].enable()
            self.elements['large'].disable()
            self.elements['medium'].enable()
            self.clan_size = "large"
        elif event.ui_element == self.elements["established"]:
            self.elements['established'].disable()
            self.elements['new'].enable()
            self.clan_age = "established"
        elif event.ui_element == self.elements["new"]:
            self.elements['established'].enable()
            self.elements['new'].disable()
            self.clan_age = "new"

    def handle_name_clan_key(self, event):
        if event.key == pygame.K_ESCAPE:
            self.change_screen("start screen")
        elif event.key == pygame.K_LEFT:
            if not self.elements["name_entry"].is_focused:
                self.clan_name = ""
        elif event.key == pygame.K_RIGHT:
            if not self.elements["name_entry"].is_focused:
                new_name = sub(
                    r"[^A-Za-z0-9 ]+", "", self.elements["name_entry"].get_text()
                ).strip()
                if not new_name:
                    self.elements["error"].set_text("Your Clan's name cannot be empty")
                    self.elements["error"].show()
                    return
                if new_name.casefold() in [
                    clan.casefold() for clan in game.switches["clan_list"]
                ]:
                    self.elements["error"].set_text(
                        "A Clan with that name already exists."
                    )
                    self.elements["error"].show()
                    return
                self.clan_name = new_name
                self.open_choose_leader()
        elif event.key == pygame.K_RETURN:
            new_name = sub(
                r"[^A-Za-z0-9 ]+", "", self.elements["name_entry"].get_text()
            ).strip()
            if not new_name:
                self.elements["error"].set_text("Your Clan's name cannot be empty")
                self.elements["error"].show()
                return
            if new_name.casefold() in [
                clan.casefold() for clan in game.switches["clan_list"]
            ]:
                self.elements["error"].set_text("A Clan with that name already exists.")
                self.elements["error"].show()
                return
            self.clan_name = new_name
            self.open_choose_leader()

    def random_clan_name(self):
        clan_names = names.names_dict["normal_prefixes"] + names.names_dict["clan_prefixes"]
        while True:
            chosen_name = choice(clan_names)
            if chosen_name.casefold() not in [clan.casefold() for clan in game.switches['clan_list']]:
                return chosen_name
            print("Generated clan name was already in use! Rerolling...")

    def handle_choose_leader_event(self, event):
        if event.ui_element in [
            self.elements["roll1"],
            self.elements["roll2"],
            self.elements["roll3"],
            self.elements["dice"],
        ]:
            self.elements["select_cat"].hide()
            create_example_cats()  # create new cats
            self.selected_cat = (
                None  # Your selected cat now no longer exists. Sad. They go away.
            )
            self.refresh_cat_images_and_info()  # Refresh all the images.
            self.rolls_left -= 1
            if game.config["clan_creation"]["rerolls"] == 3:
                event.ui_element.disable()
            else:
                self.elements["reroll_count"].set_text(str(self.rolls_left))
                if self.rolls_left == 0:
                    event.ui_element.disable()

        elif event.ui_element in [self.elements["cat" + str(u)] for u in range(0, 12)]:
            self.selected_cat = event.ui_element.return_cat_object()
            self.refresh_cat_images_and_info(self.selected_cat)
            self.refresh_text_and_buttons()
        elif event.ui_element == self.elements['select_cat']:
            self.your_cat = self.selected_cat
            self.selected_cat = None
            self.open_name_cat()
        elif event.ui_element == self.elements['previous_step']:
            self.clan_name = ""
            self.open_name_clan()
        # elif event.ui_element == self.elements['customize']:
            # self.open_customize_cat()

    def handle_choose_name_event(self, event):
        if event.ui_element == self.elements['next_step']:
            new_name = sub(r'[^A-Za-z0-9 ]+', "", self.elements["name_entry"].get_text()).strip()
            if not new_name:
                self.elements["error"].set_text("Your cat's name cannot be empty")
                self.elements["error"].show()
                return
            self.your_cat.name.prefix = new_name
            self.open_choose_background()
        elif event.ui_element == self.elements["random"]:
            self.elements["name_entry"].set_text(choice(names.names_dict["normal_prefixes"]))
        elif event.ui_element == self.elements['previous_step']:
            self.selected_cat = None
            self.open_choose_leader()

    def handle_create_other_cats(self):
        self.create_example_cats2()
        for cat in game.choose_cats.values():
            if cat.status == "warrior":
                if self.leader is None:
                    self.leader = cat
                elif self.deputy is None:
                    self.deputy = cat
                    cat.status = "deputy"
                elif self.med_cat is None:
                    self.med_cat = cat
                    cat.status = "medicine cat"
                else:
                    self.members.append(cat)
            else:
                self.members.append(cat)
        self.members.append(self.your_cat)

    def create_example_cats2(self):
        e = random.sample(range(12), 3)
        not_allowed = ['NOPAW', 'NOTAIL', 'HALFTAIL', 'NOEAR', 'BOTHBLIND', 'RIGHTBLIND', 'LEFTBLIND', 'BRIGHTHEART',
                    'NOLEFTEAR', 'NORIGHTEAR', 'MANLEG']
        c_size = 15
        backstories = ["clan_founder"]
        for i in range(1, 17):
            backstories.append(f"clan_founder{i}")
        if self.clan_age == "established":
            backstories = ['halfclan1', 'halfclan2', 'outsider_roots1', 'outsider_roots2', 'loner1', 'loner2', 'kittypet1', 'kittypet2', 'kittypet3', 'kittypet4', 'rogue1', 'rogue2', 'rogue3', 'rogue4', 'rogue5', 'rogue6', 'rogue7', 'rogue8', 'abandoned1', 'abandoned2', 'abandoned3', 'abandoned4', 'otherclan1', 'otherclan2', 'otherclan3', 'otherclan4', 'otherclan5', 'otherclan6', 'otherclan7', 'otherclan8', 'otherclan9', 'otherclan10', 'disgraced1', 'disgraced2', 'disgraced3', 'refugee1', 'refugee2', 'refugee3', 'refugee4', 'refugee5', 'tragedy_survivor1', 'tragedy_survivor2', 'tragedy_survivor3', 'tragedy_survivor4', 'tragedy_survivor5', 'tragedy_survivor6', 'guided1', 'guided2', 'guided3', 'guided4', 'orphaned1', 'orphaned2', 'orphaned3', 'orphaned4', 'orphaned5', 'orphaned6', 'outsider1', 'outsider2', 'outsider3', 'kittypet5', 'kittypet6', 'kittypet7', 'guided5', 'guided6', 'outsider4', 'outsider5', 'outsider6', 'orphaned7', 'halfclan4', 'halfclan5', 'halfclan6', 'halfclan7', 'halfclan8', 'halfclan9', 'halfclan10', 'outsider_roots3', 'outsider_roots4', 'outsider_roots5', 'outsider_roots6', 'outsider_roots7', 'outsider_roots8']

        if self.clan_size == "small":
            c_size = 10
        elif self.clan_size == 'large':
            c_size = 20
        for a in range(c_size):
            if a in e:
                game.choose_cats[a] = Cat(status='warrior', biome=None)
            else:
                r = random.randint(1,90)
                s = "warrior"
                if r > 85:
                    s = "medicine cat"
                elif r > 80:
                    s = "medicine cat apprentice"
                elif r > 40:
                    s = "warrior"
                elif r > 30:
                    s = "apprentice"
                elif r > 25:
                    s = "kitten"
                elif r > 20:
                    s = "elder"
                elif r > 15:
                    s = "mediator"
                elif r > 10:
                    s = "mediator apprentice"
                elif r > 5:
                    s = "queen"
                elif r >= 0:
                    s = "queen's apprentice"
                game.choose_cats[a] = Cat(status=s, biome=None)
            if game.choose_cats[a].moons >= 160:
                game.choose_cats[a].moons = choice(range(120, 155))
            elif game.choose_cats[a].moons == 0:
                game.choose_cats[a].moons = choice([1, 2, 3, 4, 5])

            # fucking inventory
            game.choose_cats[a].pelt.inventory = []

            if self.clan_age == "new":
                if game.choose_cats[a].status not in ['newborn', 'kitten']:
                    unique_backstories = ["clan_founder4", "clan_founder13", "clan_founder14", "clan_founder15"]
                    unique = choice(unique_backstories)
                    backstories = [story for story in backstories if story not in unique_backstories or story == unique]
                    game.choose_cats[a].backstory = choice(backstories)
                else:
                    game.choose_cats[a].backstory = 'clanborn'
            else:
                if random.randint(1,5) == 1 and game.choose_cats[a].status not in ['newborn', 'kitten']:
                    game.choose_cats[a].backstory = choice(backstories)
                else:
                    game.choose_cats[a].backstory = 'clanborn'

    def handle_choose_background_event(self, event):
        if event.ui_element == self.elements["previous_step"]:
            self.open_name_cat()
        elif event.ui_element == self.elements["forest_biome"]:
            self.biome_selected = "Forest"
            self.selected_camp_tab = 1
            self.refresh_text_and_buttons()
        elif event.ui_element == self.elements["mountain_biome"]:
            self.biome_selected = "Mountainous"
            self.selected_camp_tab = 1
            self.refresh_text_and_buttons()
        elif event.ui_element == self.elements["plains_biome"]:
            self.biome_selected = "Plains"
            self.selected_camp_tab = 1
            self.refresh_text_and_buttons()
        elif event.ui_element == self.elements["beach_biome"]:
            self.biome_selected = "Beach"
            self.selected_camp_tab = 1
            self.refresh_text_and_buttons()
        elif event.ui_element == self.tabs["tab1"]:
            self.selected_camp_tab = 1
            self.refresh_selected_camp()
        elif event.ui_element == self.tabs["tab2"]:
            self.selected_camp_tab = 2
            self.refresh_selected_camp()
        elif event.ui_element == self.tabs["tab3"]:
            self.selected_camp_tab = 3
            self.refresh_selected_camp()
        elif event.ui_element == self.tabs["tab4"]:
            self.selected_camp_tab = 4
            self.refresh_selected_camp()
        elif event.ui_element == self.tabs["tab5"]:
            self.selected_camp_tab = 5
            self.refresh_selected_camp()
        elif event.ui_element == self.tabs["tab6"]:
            self.selected_camp_tab = 6
            self.refresh_selected_camp()
        elif event.ui_element == self.tabs["newleaf_tab"]:
            self.selected_season = "Newleaf"
            self.refresh_text_and_buttons()
        elif event.ui_element == self.tabs["greenleaf_tab"]:
            self.selected_season = "Greenleaf"
            self.refresh_text_and_buttons()
        elif event.ui_element == self.tabs["leaffall_tab"]:
            self.selected_season = "Leaf-fall"
            self.refresh_text_and_buttons()
        elif event.ui_element == self.tabs["leafbare_tab"]:
            self.selected_season = "Leaf-bare"
            self.refresh_text_and_buttons()
        elif event.ui_element == self.elements["random_background"]:
            # Select a random biome and background
            self.biome_selected = self.random_biome_selection()
            if self.biome_selected in ["Forest", "Mountainous"]:
                self.selected_camp_tab = randrange(1, 5)
            else:
                self.selected_camp_tab = randrange(1, 4)
            self.selected_camp_tab = randrange(1, 4)
            self.refresh_selected_camp()
            self.refresh_text_and_buttons()
        elif event.ui_element == self.elements["next_step"]:
            self.open_choose_symbol()

    def handle_choose_background_key(self, event):
        if event.key == pygame.K_RIGHT:
            if self.biome_selected is None:
                self.biome_selected = "Forest"
            elif self.biome_selected == "Forest":
                self.biome_selected = "Mountainous"
            elif self.biome_selected == "Mountainous":
                self.biome_selected = "Plains"
            elif self.biome_selected == "Plains":
                self.biome_selected = "Beach"
            self.selected_camp_tab = 1
            self.refresh_text_and_buttons()
        elif event.key == pygame.K_LEFT:
            if self.biome_selected is None:
                self.biome_selected = "Beach"
            elif self.biome_selected == "Beach":
                self.biome_selected = "Plains"
            elif self.biome_selected == "Plains":
                self.biome_selected = "Mountainous"
            elif self.biome_selected == "Mountainous":
                self.biome_selected = "Forest"
            self.selected_camp_tab = 1
            self.refresh_text_and_buttons()
        elif event.key == pygame.K_UP and self.biome_selected is not None:
            if self.selected_camp_tab > 1:
                self.selected_camp_tab -= 1
                self.refresh_selected_camp()
        elif event.key == pygame.K_DOWN and self.biome_selected is not None:
            if self.selected_camp_tab < 6:
                self.selected_camp_tab += 1
                self.refresh_selected_camp()
        elif event.key == pygame.K_RETURN:
            self.save_clan()
            self.open_clan_saved_screen()

    def handle_choose_symbol_event(self, event):
        if event.ui_element == self.elements["previous_step"]:
            self.open_choose_background()
        elif event.ui_element == self.elements["page_right"]:
            self.current_page += 1
            self.refresh_symbol_list()
        elif event.ui_element == self.elements["page_left"]:
            self.current_page -= 1
            self.refresh_symbol_list()
        elif event.ui_element == self.elements["done_button"]:
            self.save_clan()
            self.open_clan_saved_screen()
        elif event.ui_element == self.elements["random_symbol_button"]:
            if self.symbol_selected:
                if self.symbol_selected in self.symbol_buttons:
                    self.symbol_buttons[self.symbol_selected].enable()
            self.symbol_selected = choice(sprites.clan_symbols)
            self.refresh_text_and_buttons()
        elif event.ui_element == self.elements["filters_tab"]:
            SymbolFilterWindow()
        else:
            for symbol_id, element in self.symbol_buttons.items():
                if event.ui_element == element:
                    if self.symbol_selected:
                        if self.symbol_selected in self.symbol_buttons:
                            self.symbol_buttons[self.symbol_selected].enable()
                    self.symbol_selected = symbol_id
                    self.refresh_text_and_buttons()

    def handle_saved_clan_event(self, event):
        if event.ui_element == self.elements["continue"]:
            self.change_screen("camp screen")

    def exit_screen(self):
        self.main_menu.kill()
        self.menu_warning.kill()
        self.clear_all_page()
        self.rolls_left = game.config["clan_creation"]["rerolls"]
        self.fullscreen_bgs = {}
        self.game_bgs = {}
        return super().exit_screen()

    def on_use(self):
        super().on_use()

        # Don't allow someone to enter no name for their clan
        if self.sub_screen == "name clan":
            if self.elements["name_entry"].get_text() == "":
                self.elements["next_step"].disable()
            elif self.elements["name_entry"].get_text().startswith(" "):
                self.elements["error"].set_text("Clan names cannot start with a space.")
                self.elements["error"].show()
                self.elements["next_step"].disable()
            elif self.elements["name_entry"].get_text().casefold() in [
                clan.casefold() for clan in game.switches["clan_list"]
            ]:
                self.elements["error"].set_text("A Clan with that name already exists.")
                self.elements["error"].show()
                self.elements["next_step"].disable()
            else:
                self.elements["error"].hide()
                self.elements["next_step"].enable()

            # Set the background for the name clan page - done here to avoid GUI layering issues
            screen.blit(self.name_clan_img, ui_scale_blit((0, 0)))

        elif self.sub_screen == 'choose name':
            if self.elements["name_entry"].get_text() == "":
                self.elements['next_step'].disable()
            elif self.elements["name_entry"].get_text().startswith(" "):
                self.elements["error"].set_text("Your name cannot start with a space.")
                self.elements["error"].show()
                self.elements['next_step'].disable()
            else:
                self.elements["error"].hide()
                self.elements['next_step'].enable()
        elif self.sub_screen == "choose symbol":
            if len(game.switches["disallowed_symbol_tags"]) != self.tag_list_len:
                self.tag_list_len = len(game.switches["disallowed_symbol_tags"])
                self.refresh_symbol_list()

        # refreshes symbol list when filters are changed
        # - done here bc refresh_symbol_list cannot be called from windows.py
        if self.sub_screen == "choose symbol":
            if len(game.switches["disallowed_symbol_tags"]) != self.tag_list_len:
                self.tag_list_len = len(game.switches["disallowed_symbol_tags"])
                self.refresh_symbol_list()

    def clear_all_page(self):
        """Clears the entire page, including layout images"""
        for image in self.elements:
            self.elements[image].kill()
        for tab in self.tabs:
            self.tabs[tab].kill()
        for button in self.symbol_buttons:
            self.symbol_buttons[button].kill()
        self.elements = {}

    def refresh_text_and_buttons(self):
        """Refreshes the button states and text boxes"""
        if self.sub_screen == "game mode":
            # Set the mode explanation text
            if self.game_mode == "classic":
                display_text = self.classic_mode_text
                display_name = "Classic Mode"
            elif self.game_mode == "expanded":
                display_text = self.expanded_mode_text
                display_name = "Expanded Mode"
            elif self.game_mode == "cruel season":
                display_text = self.cruel_mode_text
                display_name = "Cruel Season"
            else:
                display_text = ""
                display_name = "ERROR"
            self.elements["mode_details"].set_text(display_text)
            self.elements["mode_name"].set_text(display_name)

            # Update the enabled buttons for the game selection to disable the
            # buttons for the mode currently selected. Mostly for aesthetics, and it
            # make it very clear which mode is selected.
            if self.game_mode == "classic":
                self.elements["classic_mode_button"].disable()
                self.elements["expanded_mode_button"].enable()
                self.elements["cruel_mode_button"].enable()
            elif self.game_mode == "expanded":
                self.elements["classic_mode_button"].enable()
                self.elements["expanded_mode_button"].disable()
                self.elements["cruel_mode_button"].enable()
            elif self.game_mode == "cruel season":
                self.elements["classic_mode_button"].enable()
                self.elements["expanded_mode_button"].enable()
                self.elements["cruel_mode_button"].disable()
            else:
                self.elements["classic_mode_button"].enable()
                self.elements["expanded_mode_button"].enable()
                self.elements["cruel_mode_button"].enable()

            # Don't let the player go forwards with cruel mode, it's not done yet.
            if self.game_mode == "cruel season":
                self.elements["next_step"].disable()
            else:
                self.elements["next_step"].enable()
        # Show the error message if you try to choose a child for leader, deputy, or med cat.
        elif self.sub_screen in ['choose leader', 'choose deputy', 'choose med cat']:
            self.elements['select_cat'].show()
        # Refresh the choose-members background to match number of cat's chosen.
        elif self.sub_screen == "choose members":
            if len(self.members) == 0:
                self.elements["background"].set_image(
                    pygame.transform.scale(
                        pygame.image.load(
                            "resources/images/pick_clan_screen/clan_none_light.png"
                        ).convert_alpha(),
                        ui_scale_dimensions((800, 700)),
                    )
                )
                self.elements["next_step"].disable()
            elif len(self.members) == 1:
                self.elements["background"].set_image(
                    pygame.transform.scale(
                        pygame.image.load(
                            "resources/images/pick_clan_screen/clan_one_light.png"
                        ).convert_alpha(),
                        ui_scale_dimensions((800, 700)),
                    )
                )
                self.elements["next_step"].disable()
            elif len(self.members) == 2:
                self.elements["background"].set_image(
                    pygame.transform.scale(
                        pygame.image.load(
                            "resources/images/pick_clan_screen/clan_two_light.png"
                        ).convert_alpha(),
                        ui_scale_dimensions((800, 700)),
                    )
                )
                self.elements["next_step"].disable()
            elif len(self.members) == 3:
                self.elements["background"].set_image(
                    pygame.transform.scale(
                        pygame.image.load(
                            "resources/images/pick_clan_screen/clan_three_light.png"
                        ).convert_alpha(),
                        ui_scale_dimensions((800, 700)),
                    )
                )
                self.elements["next_step"].disable()
            elif 4 <= len(self.members) <= 6:
                self.elements["background"].set_image(
                    pygame.transform.scale(
                        pygame.image.load(
                            "resources/images/pick_clan_screen/clan_four_light.png"
                        ).convert_alpha(),
                        ui_scale_dimensions((800, 700)),
                    )
                )
                self.elements["next_step"].enable()
                # In order for the "previous step" to work properly, we must enable this button, just in case it
                # was disabled in the next step.
                self.elements["select_cat"].enable()
            elif len(self.members) == 7:
                self.elements["background"].set_image(
                    pygame.transform.scale(
                        pygame.image.load(
                            "resources/images/pick_clan_screen/clan_full_light.png"
                        ).convert_alpha(),
                        ui_scale_dimensions((800, 700)),
                    )
                )
                self.elements["select_cat"].disable()
                self.elements["next_step"].enable()

            # Hide the recruit cat button if no cat is selected.
            if self.selected_cat is not None:
                self.elements["select_cat"].show()
            else:
                self.elements["select_cat"].hide()

        elif self.sub_screen == "choose camp":
            # Enable/disable biome buttons
            if self.biome_selected == "Forest":
                self.elements["forest_biome"].disable()
                self.elements["mountain_biome"].enable()
                self.elements["plains_biome"].enable()
                self.elements["beach_biome"].enable()
            elif self.biome_selected == "Mountainous":
                self.elements["forest_biome"].enable()
                self.elements["mountain_biome"].disable()
                self.elements["plains_biome"].enable()
                self.elements["beach_biome"].enable()
            elif self.biome_selected == "Plains":
                self.elements["forest_biome"].enable()
                self.elements["mountain_biome"].enable()
                self.elements["plains_biome"].disable()
                self.elements["beach_biome"].enable()
            elif self.biome_selected == "Beach":
                self.elements["forest_biome"].enable()
                self.elements["mountain_biome"].enable()
                self.elements["plains_biome"].enable()
                self.elements["beach_biome"].disable()

            if self.selected_season == "Newleaf":
                self.tabs["newleaf_tab"].disable()
                self.tabs["greenleaf_tab"].enable()
                self.tabs["leaffall_tab"].enable()
                self.tabs["leafbare_tab"].enable()
            elif self.selected_season == "Greenleaf":
                self.tabs["newleaf_tab"].enable()
                self.tabs["greenleaf_tab"].disable()
                self.tabs["leaffall_tab"].enable()
                self.tabs["leafbare_tab"].enable()
            elif self.selected_season == "Leaf-fall":
                self.tabs["newleaf_tab"].enable()
                self.tabs["greenleaf_tab"].enable()
                self.tabs["leaffall_tab"].disable()
                self.tabs["leafbare_tab"].enable()
            elif self.selected_season == "Leaf-bare":
                self.tabs["newleaf_tab"].enable()
                self.tabs["greenleaf_tab"].enable()
                self.tabs["leaffall_tab"].enable()
                self.tabs["leafbare_tab"].disable()

            if self.biome_selected and self.selected_camp_tab:
                self.elements["next_step"].enable()

            # Deal with tab and shown camp image:
            self.refresh_selected_camp()
        elif self.sub_screen == "choose symbol":
            if self.symbol_selected:
                if self.symbol_selected in self.symbol_buttons:
                    self.symbol_buttons[self.symbol_selected].disable()
                # refresh selected symbol image
                self.elements["selected_symbol"].set_image(
                    pygame.transform.scale(
                        sprites.sprites[self.symbol_selected],
                        ui_scale_dimensions((100, 100)),
                    ).convert_alpha()
                )
                symbol_name = self.symbol_selected.replace("symbol", "")
                self.text["selected"].set_text(f"Selected Symbol: {symbol_name}")
                self.elements["selected_symbol"].show()
                self.elements["done_button"].enable()

    def refresh_selected_camp(self):
        """Updates selected camp image and tabs"""
        self.tabs["tab1"].kill()
        self.tabs["tab2"].kill()
        self.tabs["tab3"].kill()
        self.tabs["tab4"].kill()
        self.tabs["tab5"].kill()
        self.tabs["tab6"].kill()

        if self.biome_selected == "Forest":
            self.tabs["tab1"] = UIImageButton(
                ui_scale(pygame.Rect((95, 180), (154, 30))),
                "",
                object_id="#classic_tab",
                manager=MANAGER,
            )
            self.tabs["tab2"] = UIImageButton(
                ui_scale(pygame.Rect((108, 215), (154, 30))),
                "",
                object_id="#gully_tab",
                manager=MANAGER,
            )
            self.tabs["tab3"] = UIImageButton(
                ui_scale(pygame.Rect((95, 250), (154, 30))),
                "",
                object_id="#grotto_tab",
                manager=MANAGER,
            )
            self.tabs["tab4"] = UIImageButton(
                ui_scale(pygame.Rect((85, 285), (154, 30))),
                "",
                object_id="#lakeside_tab",
                manager=MANAGER,
            )
            self.tabs["tab5"] = UIImageButton(
                ui_scale(pygame.Rect((85, 320), (154, 30))),
                "",
                object_id="#pine_tab",
                manager=MANAGER,
            )
            self.tabs["tab6"] = UIImageButton(
                ui_scale(pygame.Rect((85, 355), (154, 30))),
                "",
                object_id="#birch_camp_tab",
                manager=MANAGER,
            )
        elif self.biome_selected == "Mountainous":
            self.tabs["tab1"] = UIImageButton(
                ui_scale(pygame.Rect((111, 180), (154, 30))),
                "",
                object_id="#cliff_tab",
                manager=MANAGER,
            )
            self.tabs["tab2"] = UIImageButton(
                ui_scale(pygame.Rect((90, 215), (154, 30))),
                "",
                object_id="#cave_tab",
                manager=MANAGER,
            )
            self.tabs["tab3"] = UIImageButton(
                ui_scale(pygame.Rect((42, 250), (179, 30))),
                "",
                object_id="#crystal_tab",
                manager=MANAGER,
            )
            self.tabs["tab4"] = UIImageButton(
                ui_scale(pygame.Rect((107, 285), (154, 30))),
                "",
                object_id="#ruins_tab",
                manager=MANAGER,
            )
            self.tabs["tab5"] = UIImageButton(
                ui_scale(pygame.Rect((107, 320), (154, 30))),
                "",
                object_id="#quarry_tab",
                manager=MANAGER,
            )
            self.tabs["tab6"] = UIImageButton(
                ui_scale(pygame.Rect((108, 355), (154, 30))),
                "",
                object_id="#ruins_tab",
                manager=MANAGER,
            )
        elif self.biome_selected == "Plains":
            self.tabs["tab1"] = UIImageButton(
                ui_scale(pygame.Rect((64, 180), (154, 30))),
                "",
                object_id="#grasslands_tab",
                manager=MANAGER,
            )
            self.tabs["tab2"] = UIImageButton(
                ui_scale(pygame.Rect((89, 215), (154, 30))),
                "",
                object_id="#tunnel_tab",
                manager=MANAGER,
            )
            self.tabs["tab3"] = UIImageButton(
                ui_scale(pygame.Rect((64, 250), (154, 30))),
                "",
                object_id="#wasteland_tab",
                manager=MANAGER,
            )
            self.tabs["tab4"] = UIImageButton(
                ui_scale(pygame.Rect((59, 320), (154, 30))),
                "",
                object_id="#taiga_camp_tab",
                manager=MANAGER,
            )
            self.tabs["tab5"] = UIImageButton(
                ui_scale(pygame.Rect((50, 355), (154, 30))),
                "",
                object_id="#desert_tab",
                manager=MANAGER,
            )
        elif self.biome_selected == "Beach":
            self.tabs["tab1"] = UIImageButton(
                ui_scale(pygame.Rect((76, 180), (154, 30))),
                "",
                object_id="#tidepool_tab",
                manager=MANAGER,
            )
            self.tabs["tab2"] = UIImageButton(
                ui_scale(pygame.Rect((65, 215), (154, 30))),
                "",
                object_id="#tidal_cave_tab",
                manager=MANAGER,
            )
            self.tabs["tab3"] = UIImageButton(
                ui_scale(pygame.Rect((70, 250), (154, 30))),
                "",
                object_id="#shipwreck_tab",
                manager=MANAGER,
            )
            self.tabs["tab4"] = UIImageButton(
                ui_scale(pygame.Rect((65, 320), (154, 30))),
                "",
                object_id="#tropical_island_tab",
                manager=MANAGER,
            )

        self.tabs["tab1"].disable() if self.selected_camp_tab == 1 else self.tabs[
            "tab1"
        ].enable()
        self.tabs["tab2"].disable() if self.selected_camp_tab == 2 else self.tabs[
            "tab2"
        ].enable()
        self.tabs["tab3"].disable() if self.selected_camp_tab == 3 else self.tabs[
            "tab3"
        ].enable()
        self.tabs["tab4"].disable() if self.selected_camp_tab == 4 else self.tabs[
            "tab4"
        ].enable()
        self.tabs["tab5"].disable() if self.selected_camp_tab == 5 else self.tabs[
            "tab5"
        ].enable()
        self.tabs["tab6"].disable() if self.selected_camp_tab == 6 else self.tabs[
            "tab6"
        ].enable()

        # I have to do this for proper layering.
        if "camp_art" in self.elements:
            self.elements["camp_art"].kill()
        if self.biome_selected:
            src = pygame.image.load(
                self.get_camp_art_path(self.selected_camp_tab)
            ).convert_alpha()
            self.elements["camp_art"] = pygame_gui.elements.UIImage(
                ui_scale(pygame.Rect((175, 170), (450, 400))),
                pygame.transform.scale(
                    src.copy(),
                    ui_scale_dimensions((450, 400)),
                ),
                manager=MANAGER,
            )
            self.get_camp_bg(src)

        self.draw_art_frame()

    def get_camp_bg(self, src=None):
        if src is None:
            src = pygame.image.load(
                self.get_camp_art_path(self.selected_camp_tab)
            ).convert_alpha()

        name = "_".join(
            [
                str(self.biome_selected),
                str(self.selected_camp_tab),
                self.selected_season,
            ]
        )
        if name not in self.game_bgs:
            self.game_bgs[
                name
            ] = scripts.screens.screens_core.screens_core.default_game_bgs[self.theme][
                "default"
            ]
            self.fullscreen_bgs[
                name
            ] = scripts.screens.screens_core.screens_core.process_blur_bg(src)

        self.set_bg(name)

    def refresh_selected_cat_info(self, selected=None):
        # SELECTED CAT INFO
        if selected is not None:
            if self.sub_screen == "choose leader":
                self.elements["cat_name"].set_text(
                    str(selected.name)
                )
            else:
                self.elements["cat_name"].set_text(str(selected.name))
            self.elements["cat_name"].show()
            self.elements["cat_info"].set_text(
                selected.genderalign
                + "\n"
                + str(
                    selected.age
                    + "\n"
                    + str(selected.personality.trait)
                    + "\n"
                    + str(selected.skills.skill_string())
                )
            if selected.permanent_condition:

                self.elements['cat_info'].set_text(selected.genderalign + "\n" +
                                                   str(selected.personality.trait) + "\n" +
                                                   str(selected.skills.skill_string()) + "\n" +
                                                   "permanent condition: " + list(selected.permanent_condition.keys())[0])
            )
            self.elements["cat_info"].show()

    def refresh_cat_images_and_info(self, selected=None):
        """Update the image of the cat selected in the middle. Info and image.
        Also updates the location of selected cats."""

        column_poss = [50, 100]

        # updates selected cat info
        self.refresh_selected_cat_info(selected)

        # CAT IMAGES
        for u in range(6):
            if "cat" + str(u) in self.elements:
                self.elements["cat" + str(u)].kill()
            if game.choose_cats[u] == selected:
                self.elements["cat" + str(u)] = self.elements[
                    "cat" + str(u)
                ] = UISpriteButton(
                    ui_scale(pygame.Rect((270, 200), (150, 150))),
                    pygame.transform.scale(
                        game.choose_cats[u].sprite, ui_scale_dimensions((150, 150))
                    ),
                    cat_object=game.choose_cats[u],
                )
            elif (
                game.choose_cats[u]
                in [self.leader, self.deputy, self.med_cat] + self.members
            ):
                self.elements["cat" + str(u)] = UISpriteButton(
                    ui_scale(pygame.Rect((650, 130 + 50 * u), (50, 50))),
                    game.choose_cats[u].sprite,
                    cat_object=game.choose_cats[u],
                    manager=MANAGER,
                )
                self.elements["cat" + str(u)].disable()
            else:
                self.elements["cat" + str(u)] = UISpriteButton(
                    ui_scale(pygame.Rect((column_poss[0], 130 + 50 * u), (50, 50))),
                    game.choose_cats[u].sprite,
                    tool_tip_text=self._get_cat_tooltip_string(game.choose_cats[u]),
                    cat_object=game.choose_cats[u],
                    manager=MANAGER,
                )
        for u in range(6, 12):
            if "cat" + str(u) in self.elements:
                self.elements["cat" + str(u)].kill()
            if game.choose_cats[u] == selected:
                self.elements["cat" + str(u)] = self.elements[
                    "cat" + str(u)
                ] = UISpriteButton(
                    ui_scale(pygame.Rect((270, 200), (150, 150))),
                    pygame.transform.scale(
                        game.choose_cats[u].sprite, ui_scale_dimensions((150, 150))
                    ),
                    cat_object=game.choose_cats[u],
                    manager=MANAGER,
                )
            elif (
                game.choose_cats[u]
                in [self.leader, self.deputy, self.med_cat] + self.members
            ):
                self.elements["cat" + str(u)] = UISpriteButton(
                    ui_scale(pygame.Rect((700, 200 + 50 * (u - 6)), (50, 50))),
                    game.choose_cats[u].sprite,
                    cat_object=game.choose_cats[u],
                    manager=MANAGER,
                )
                self.elements["cat" + str(u)].disable()
            else:
                self.elements["cat" + str(u)] = UISpriteButton(
                    ui_scale(
                        pygame.Rect((column_poss[1], 130 + 50 * (u - 6)), (50, 50))
                    ),
                    game.choose_cats[u].sprite,
                    tool_tip_text=self._get_cat_tooltip_string(game.choose_cats[u]),
                    cat_object=game.choose_cats[u],
                    manager=MANAGER,
                )

    def refresh_cat_images_and_info2(self, selected=None):
        """Update the image of the cat selected in the middle. Info and image.
        Also updates the location of selected cats."""

        column_poss = [50, 100]

        # updates selected cat info
        self.refresh_selected_cat_info(selected)

        # CAT IMAGES
        for u in range(6):
            if "cat" + str(u) in self.elements:
                self.elements["cat" + str(u)].kill()
            if game.choose_cats[u] == selected:
                self.elements["cat" + str(u)] = self.elements[
                    "cat" + str(u)
                ] = UISpriteButton(
                    ui_scale(pygame.Rect((310, 200), (150, 150))),
                    pygame.transform.scale(
                        game.choose_cats[u].sprite, ui_scale_dimensions((150, 150))
                    ),
                    cat_object=game.choose_cats[u],
                )
        for u in range(6, 12):
            if "cat" + str(u) in self.elements:
                self.elements["cat" + str(u)].kill()
            if game.choose_cats[u] == selected:
                self.elements["cat" + str(u)] = self.elements[
                    "cat" + str(u)
                ] = UISpriteButton(
                    ui_scale(pygame.Rect((310, 200), (150, 150))),
                    pygame.transform.scale(
                        game.choose_cats[u].sprite, ui_scale_dimensions((150, 150))
                    ),
                    cat_object=game.choose_cats[u],
                    manager=MANAGER,
                )
        
    def open_name_cat(self):
        """Opens the name cat screen"""
        
        self.clear_all_page()
        
        self.elements["leader_image"] = pygame_gui.elements.UIImage(ui_scale(pygame.Rect((290, 150), (200, 200))),
                                                                    pygame.transform.scale(
                                                                        self.your_cat.sprite,
                                                                        (100, 100)), manager=MANAGER)

        self.elements['background'] = pygame_gui.elements.UIImage(ui_scale(pygame.Rect((0, 0), (800, 700))),
                                                                    MakeClanScreen.your_name_img, manager=MANAGER)

        self.elements['text1'] = pygame_gui.elements.UIImage(ui_scale(pygame.Rect((260, 365), (398, 13))),
                                                                  MakeClanScreen.your_name_txt1, manager=MANAGER)
        self.elements['text2'] = pygame_gui.elements.UIImage(ui_scale(pygame.Rect((260, 395), (268, 13))),
                                                                  MakeClanScreen.your_name_txt2, manager=MANAGER)
        self.elements['background'].disable()
        self.elements["version_background"] = UIImageButton(ui_scale(pygame.Rect((725, 872), (700, 28))), "", object_id="blank_button", manager=MANAGER)
        self.elements["version_background"].disable()

        self.refresh_cat_images_and_info2()
        
        self.sub_screen = 'choose name'
        
        self.elements["random"] = UIImageButton(ui_scale(pygame.Rect((285, 448), (34, 34))), "",
                                                object_id="#random_dice_button"
                                                , manager=MANAGER)

        self.elements["error"] = pygame_gui.elements.UITextBox("", ui_scale(pygame.Rect((253, 655), (298, -1))),
                                                               manager=MANAGER,
                                                               object_id="#default_dark", visible=False)
        self.main_menu.kill()
        self.main_menu = UIImageButton(ui_scale(pygame.Rect((50, 50), (153, 30))), "", object_id="#main_menu_button"
                                       , manager=MANAGER)

        self.elements['previous_step'] = UIImageButton(ui_scale(pygame.Rect((253, 645), (147, 30))), "",
                                                       object_id="#previous_step_button", manager=MANAGER)
        self.elements['next_step'] = UIImageButton(ui_scale(pygame.Rect((400, 645), (147, 30))), "",
                                                   object_id="#next_step_button", manager=MANAGER)
        self.elements["name_entry"] = pygame_gui.elements.UITextEntryLine(ui_scale(pygame.Rect((325, 450), (140, 14)))
                                                                          , manager=MANAGER, initial_text=self.your_cat.name.prefix)
        self.elements["name_entry"].set_allowed_characters(
            list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_- "))
        self.elements["name_entry"].set_text_length_limit(11)

        self.elements["clan"] = pygame_gui.elements.UITextBox("-kit",
                                                            ui_scale(pygame.Rect((435, 453), (100, 25))),
                                                            object_id="#text_box_30_horizcenter",
                                                            manager=MANAGER)

    def refresh_symbol_list(self):
        # get symbol list
        symbol_list = sprites.clan_symbols.copy()
        symbol_attributes = sprites.symbol_dict

        # filtering out tagged symbols
        for symbol in sprites.clan_symbols:
            index = symbol[-1]
            name = symbol.strip("symbol1234567890")
            tags = symbol_attributes[name.capitalize()][f"tags{index}"]
            for tag in tags:
                if tag in game.switches["disallowed_symbol_tags"]:
                    if symbol in symbol_list:
                        symbol_list.remove(symbol)

        # separate list into chunks for pages
        symbol_chunks = self.chunks(symbol_list, 45)

        # clamp current page to a valid page number
        self.current_page = max(1, min(self.current_page, len(symbol_chunks)))

        # handles which arrow buttons are clickable
        if len(symbol_chunks) <= 1:
            self.elements["page_left"].disable()
            self.elements["page_right"].disable()
        elif self.current_page >= len(symbol_chunks):
            self.elements["page_left"].enable()
            self.elements["page_right"].disable()
        elif self.current_page == 1 and len(symbol_chunks) > 1:
            self.elements["page_left"].disable()
            self.elements["page_right"].enable()
        else:
            self.elements["page_left"].enable()
            self.elements["page_right"].enable()

        display_symbols = []
        if symbol_chunks:
            display_symbols = symbol_chunks[self.current_page - 1]

        # Kill all currently displayed symbols
        symbol_images = [ele for ele in self.elements if ele in sprites.clan_symbols]
        for ele in symbol_images:
            self.elements[ele].kill()
            if self.symbol_buttons:
                self.symbol_buttons[ele].kill()

        x_pos = 96
        y_pos = 270
        for symbol in display_symbols:
            self.elements[f"{symbol}"] = pygame_gui.elements.UIImage(
                ui_scale(pygame.Rect((x_pos, y_pos), (50, 50))),
                sprites.sprites[symbol],
                object_id=f"#{symbol}",
                starting_height=3,
                manager=MANAGER,
            )
            self.symbol_buttons[f"{symbol}"] = UIImageButton(
                ui_scale(pygame.Rect((x_pos - 12, y_pos - 12), (74, 74))),
                "",
                object_id=f"#symbol_select_button",
                starting_height=4,
                manager=MANAGER,
            )
            x_pos += 70
            if x_pos >= 715:
                x_pos = 96
                y_pos += 70

        if self.symbol_selected in self.symbol_buttons:
            self.symbol_buttons[self.symbol_selected].disable()

    def random_biome_selection(self):
        # Select a random biome and background
        old_biome = self.biome_selected
        possible_biomes = ["Forest", "Mountainous", "Plains", "Beach"]
        # ensuring that the new random camp will not be the same one
        if old_biome is not None:
            possible_biomes.remove(old_biome)
        chosen_biome = choice(possible_biomes)
        return chosen_biome

    def _get_cat_tooltip_string(self, cat: Cat):
        """Get tooltip for cat. Tooltip displays name, sex, age group, and trait."""

        return f"<b>{cat.name}</b><br>{cat.genderalign}<br>{cat.age}<br>{cat.personality.trait}"


    def open_name_clan(self):
        """Opens the name Clan screen"""
        self.clear_all_page()
        self.sub_screen = "name clan"

        # Create all the elements.
        self.elements["random"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((224, 595), (34, 34))),
            "\u2684",
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            manager=MANAGER,
            sound_id="dice_roll",
        )

        self.elements["error"] = pygame_gui.elements.UITextBox(
            "",
            ui_scale(pygame.Rect((506, 1310), (596, -1))),
            manager=MANAGER,
            object_id="#default_dark",
            visible=False,
        )

        self.elements["previous_step"] = UIImageButton(
            ui_scale(pygame.Rect((253, 635), (147, 30))),
            "",
            object_id="#previous_step_button",
            manager=MANAGER,
            starting_height=2,
        )
        self.elements["next_step"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((0, 635), (147, 30))),
            "Next Step " + get_arrow(3, arrow_left=False),
            get_button_dict(ButtonStyles.MENU_RIGHT, (147, 30)),
            object_id="@buttonstyles_menu_right",
            manager=MANAGER,
            starting_height=2,
            anchors={"left_target": self.elements["previous_step"]},
        )
        self.elements["next_step"].disable()
        self.elements["name_entry"] = pygame_gui.elements.UITextEntryLine(
            ui_scale(pygame.Rect((265, 597), (140, 29))),
            manager=MANAGER,
        )
        self.elements["name_entry"].set_allowed_characters(
            list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_- ")
        )
        self.elements["name_entry"].set_text_length_limit(11)
        self.elements["clan"] = pygame_gui.elements.UITextBox(
            "-Clan",
            ui_scale(pygame.Rect((375, 600), (100, 25))),
            object_id="#text_box_30_horizcenter_light",
            manager=MANAGER,
        )
        self.elements["reset_name"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((455, 595), (134, 30))),
            "reset name",
            get_button_dict(ButtonStyles.SQUOVAL, (134, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )
        self.elements["clan_size"] = pygame_gui.elements.UITextBox(
            "Clan Size: ",
            ui_scale(pygame.Rect((200, 55), (100, 25))),
            object_id="#text_box_30_horizcenter",
            manager=MANAGER)
        self.elements["clan_age"] = pygame_gui.elements.UITextBox(
            "Clan Age: ",
            ui_scale(pygame.Rect((200, 98), (100, 30))),
            object_id="#text_box_30_horizcenter",
            manager=MANAGER)
        
        self.elements["small"] = UIImageButton(ui_scale(pygame.Rect((300,50), (96, 30))), "Small", object_id="#clan_size_small", manager=MANAGER)

        self.elements["medium"] = UIImageButton(ui_scale(pygame.Rect((475,50), (96, 30))), "Medium", object_id="#clan_size_medium", manager=MANAGER)
        
        self.elements["large"] = UIImageButton(ui_scale(pygame.Rect((550,50), (96, 30))), "Large", object_id="#clan_size_large", manager=MANAGER)

        self.elements["medium"].disable()

        self.elements["established"] = UIImageButton(ui_scale(pygame.Rect((300,100), (96, 30))), "Old", object_id="#clan_age_old", tool_tip_text="The Clan has existed for many moons and cats' backstories will reflect this.",manager=MANAGER)
        self.elements["new"] = UIImageButton(ui_scale(pygame.Rect((475,100), (96, 30))), "New", object_id="#clan_age_new", tool_tip_text="The Clan is newly established and cats' backstories will reflect this.", manager=MANAGER)
        self.elements["established"].disable()

    def clan_name_header(self):
        self.elements["name_backdrop"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((292, 100), (216, 50))),
            self.clan_frame_img,
            manager=MANAGER,
        )
        self.elements["clan_name"] = pygame_gui.elements.UITextBox(
            self.clan_name + "Clan",
            ui_scale(pygame.Rect((292, 100), (216, 50))),
            object_id=ObjectID("#text_box_30_horizcenter_vertcenter", "#dark"),
            manager=MANAGER,
        )

    def open_choose_leader(self):
        """Set up the screen for the choose leader phase."""
        self.clear_all_page()
        self.sub_screen = "choose leader"

        self.elements["background"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((250, 500), (300, 35))),
            self.leader_img,
            manager=MANAGER,
        )

        self.elements["background"].disable()
        self.clan_name_header()

        # Roll_buttons
        x_pos = 155
        y_pos = 235
        self.elements["roll1"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((x_pos, y_pos), (34, 34))),
            "\u2684",
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            manager=MANAGER,
            sound_id="dice_roll",
        )
        y_pos += 40
        self.elements["roll2"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((x_pos, y_pos), (34, 34))),
            "\u2684",
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            manager=MANAGER,
            sound_id="dice_roll",
        )
        y_pos += 40
        self.elements["roll3"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((x_pos, y_pos), (34, 34))),
            "\u2684",
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            manager=MANAGER,
            sound_id="dice_roll",
        )

        _tmp = 80
        if self.rolls_left == -1:
            _tmp += 5
        self.elements["dice"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((_tmp, 435), (34, 34))),
            "\u2684",
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            manager=MANAGER,
            sound_id="dice_roll",
        )
        del _tmp
        self.elements["reroll_count"] = pygame_gui.elements.UILabel(
            ui_scale(pygame.Rect((100, 440), (50, 25))),
            str(self.rolls_left),
            object_id=get_text_box_theme(""),
            manager=MANAGER,
        )

        if game.config["clan_creation"]["rerolls"] == 3:
            if self.rolls_left <= 2:
                self.elements["roll1"].disable()
            if self.rolls_left <= 1:
                self.elements["roll2"].disable()
            if self.rolls_left == 0:
                self.elements["roll3"].disable()
            self.elements["dice"].hide()
            self.elements["reroll_count"].hide()
        else:
            if self.rolls_left == 0:
                self.elements["dice"].disable()
            elif self.rolls_left == -1:
                self.elements["reroll_count"].hide()
            self.elements["roll1"].hide()
            self.elements["roll2"].hide()
            self.elements["roll3"].hide()

        self.create_cat_info()
            

        self.elements["select_cat"] = UIImageButton(
            ui_scale(pygame.Rect((353, 360), (95, 30))),
            "",
            object_id="#recruit_button",
            starting_height=2,
            visible=False,
            manager=MANAGER,
        )

        # Next and previous buttons
        self.elements["previous_step"] = UIImageButton(
            ui_scale(pygame.Rect((253, 400), (147, 30))),
            "",
            object_id="#previous_step_button",
            manager=MANAGER,
            starting_height=2,
        )
        self.elements["next_step"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((0, 400), (147, 30))),
            "Next Step " + get_arrow(3, arrow_left=False),
            get_button_dict(ButtonStyles.MENU_RIGHT, (147, 30)),
            object_id="@buttonstyles_menu_right",
            manager=MANAGER,
            starting_height=2,
            anchors={"left_target": self.elements["previous_step"]},
        )
        self.elements["next_step"].disable()
        # self.elements['customize'] = UIImageButton(ui_scale(pygame.Rect((50,100),(118,30))), "", object_id="#customize_button", manager=MANAGER,  tool_tip_text = "Customize your own cat")

        # draw cats to choose from
        self.refresh_cat_images_and_info()

    def randomize_custom_cat(self):
        pelts = list(Pelt.sprites_names.keys())
        pelts.remove("Tortie")
        pelts.remove("Calico")
        pelts_tortie = pelts.copy()
        pelts_tortie.remove("SingleColour")
        pelts_tortie.remove("TwoColour")
        # pelts_tortie.append("Single")
        permanent_conditions = ['born without a leg', 'weak leg', 'twisted leg', 'born without a tail', 'paralyzed', 'raspy lungs', 'wasting disease', 'blind', 'one bad eye', 'failing eyesight', 'partial hearing loss', 'deaf', 'constant joint pain', 'seizure prone', 'allergies', 'persistent headaches']

        white_patches = ["FULLWHITE"] + Pelt.little_white + Pelt.mid_white + Pelt.high_white + Pelt.mostly_white
        self.pname= random.choice(pelts) if random.randint(1,3) == 1 else "Tortie"
        self.length=random.choice(["short", "medium", "long"])
        self.colour=random.choice(Pelt.pelt_colours)
        self.white_patches= choice(white_patches) if random.randint(1,2) == 1 else None
        self.eye_color=choice(Pelt.eye_colours)
        self.eye_colour2=choice(Pelt.eye_colours) if random.randint(1,10) == 1 else None
        self.tortiebase=choice(Pelt.tortiebases)
        self.tortiecolour=choice(Pelt.pelt_colours)
        self.pattern=choice(Pelt.tortiepatterns)
        self.tortiepattern=choice(pelts_tortie)
        self.vitiligo=choice(Pelt.vit) if random.randint(1,5) == 1 else None
        self.points=choice(Pelt.point_markings) if random.randint(1,5) == 1 else None
        self.scars=[choice(Pelt.scars1 + Pelt.scars2 + Pelt.scars3)] if random.randint(1,10) == 1 else []
        self.tint=choice(["pink", "gray", "red", "orange", "black", "yellow", "purple", "blue","dilute","warmdilute","cooldilute"]) if random.randint(1,5) == 1 else None
        self.skin=choice(Pelt.skin_sprites)
        self.white_patches_tint=choice(["offwhite", "cream", "darkcream", "gray", "pink"]) if random.randint(1,5) == 1 else None
        self.reverse= False if random.randint(1,2) == 1 else True
        self.skill = random.choice(self.skills)
        self.personality = choice(['troublesome', 'lonesome', 'impulsive', 'bullying', 'attention-seeker', 'charming', 'daring', 'noisy', 'nervous', 'quiet', 'insecure', 'daydreamer', 'sweet', 'polite', 'know-it-all', 'bossy', 'disciplined', 'patient', 'manipulative', 'secretive', 'rebellious', 'grumpy', 'passionate', 'honest', 'leader-like', 'smug'])
        self.accessory = choice(Pelt.plant_accessories + Pelt.wild_accessories + Pelt.collars + Pelt.flower_accessories + Pelt.plant2_accessories + Pelt.snake_accessories + Pelt.smallAnimal_accessories + Pelt.deadInsect_accessories + Pelt.aliveInsect_accessories + Pelt.fruit_accessories + Pelt.crafted_accessories + Pelt.tail2_accessories) if random.randint(1,5) == 1 else None
        self.permanent_condition = choice(permanent_conditions) if random.randint(1,30) == 1 else None
        self.faith = random.choice(["flexible", "starclan", "dark forest", "neutral"])


        self.kitten_sprite=random.randint(0,2)
        self.adolescent_pose = random.randint(0,2)
        self.adult_pose = random.randint(0,2)
        self.elder_pose = random.randint(0,2)
        

    def open_choose_background(self):
        # clear screen
        self.clear_all_page()
        self.sub_screen = "choose camp"

        # Next and previous buttons
        self.elements["previous_step"] = UIImageButton(
            ui_scale(pygame.Rect((253, 645), (147, 30))),
            "",
            object_id="#previous_step_button",
            manager=MANAGER,
            starting_height=2,
        )
        self.elements["next_step"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((0, 645), (147, 30))),
            "Next Step " + get_arrow(3, arrow_left=False),
            get_button_dict(ButtonStyles.MENU_RIGHT, (147, 30)),
            object_id="@buttonstyles_menu_right",
            manager=MANAGER,
            starting_height=2,
            anchors={"left_target": self.elements["previous_step"]},
        )
        self.elements["next_step"].disable()

        # Biome buttons
        self.elements["forest_biome"] = UIImageButton(
            ui_scale(pygame.Rect((196, 100), (100, 46))),
            "",
            object_id="#forest_biome_button",
            manager=MANAGER,
        )
        self.elements["mountain_biome"] = UIImageButton(
            ui_scale(pygame.Rect((304, 100), (106, 46))),
            "",
            object_id="#mountain_biome_button",
            manager=MANAGER,
        )
        self.elements["plains_biome"] = UIImageButton(
            ui_scale(pygame.Rect((424, 100), (88, 46))),
            "",
            object_id="#plains_biome_button",
            manager=MANAGER,
        )
        self.elements["beach_biome"] = UIImageButton(
            ui_scale(pygame.Rect((520, 100), (82, 46))),
            "",
            object_id="#beach_biome_button",
            manager=MANAGER,
        )

        # Camp Art Choosing Tabs, Dummy buttons, will be overridden.
        self.tabs["tab1"] = UIImageButton(
            ui_scale(pygame.Rect((0, 0), (0, 0))), "", visible=False, manager=MANAGER
        )
        self.tabs["tab2"] = UIImageButton(
            ui_scale(pygame.Rect((0, 0), (0, 0))), "", visible=False, manager=MANAGER
        )
        self.tabs["tab3"] = UIImageButton(
            ui_scale(pygame.Rect((0, 0), (0, 0))), "", visible=False, manager=MANAGER
        )
        self.tabs["tab4"] = UIImageButton(
            ui_scale(pygame.Rect((0, 0), (0, 0))), "", visible=False, manager=MANAGER
        )
        self.tabs["tab5"] = UIImageButton(
            ui_scale(pygame.Rect((0, 0), (0, 0))), "", visible=False, manager=MANAGER
        )
        self.tabs["tab6"] = UIImageButton(
            ui_scale(pygame.Rect((0, 0), (0, 0))), "", visible=False, manager=MANAGER
        )

        self.tabs["newleaf_tab"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((625, 275), (39, 34))),
            Icon.NEWLEAF,
            get_button_dict(ButtonStyles.ICON_TAB_LEFT, (39, 36)),
            object_id="@buttonstyles_icon_tab_left",
            manager=MANAGER,
            tool_tip_text="Switch starting season to Newleaf.",
        )
        self.tabs["greenleaf_tab"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((625, 25), (39, 34))),
            Icon.GREENLEAF,
            get_button_dict(ButtonStyles.ICON_TAB_LEFT, (39, 36)),
            object_id="@buttonstyles_icon_tab_left",
            manager=MANAGER,
            tool_tip_text="Switch starting season to Greenleaf.",
            anchors={"top_target": self.tabs["newleaf_tab"]},
        )
        self.tabs["leaffall_tab"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((625, 25), (39, 34))),
            Icon.LEAFFALL,
            get_button_dict(ButtonStyles.ICON_TAB_LEFT, (39, 36)),
            object_id="@buttonstyles_icon_tab_left",
            manager=MANAGER,
            tool_tip_text="Switch starting season to Leaf-fall.",
            anchors={"top_target": self.tabs["greenleaf_tab"]},
        )
        self.tabs["leafbare_tab"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((625, 25), (39, 34))),
            Icon.LEAFBARE,
            get_button_dict(ButtonStyles.ICON_TAB_LEFT, (39, 36)),
            object_id="@buttonstyles_icon_tab_left",
            manager=MANAGER,
            tool_tip_text="Switch starting season to Leaf-bare.",
            anchors={"top_target": self.tabs["leaffall_tab"]},
        )
        # Random background
        self.elements["random_background"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((255, 595), (290, 30))),
            "choose a random background",
            get_button_dict(ButtonStyles.SQUOVAL, (290, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )

        # art frame
        self.draw_art_frame()

    def open_choose_symbol(self):
        # clear screen
        self.clear_all_page()

        # set basics
        self.sub_screen = "choose symbol"

        self.elements["previous_step"] = UIImageButton(
            ui_scale(pygame.Rect((253, 645), (147, 30))),
            "",
            object_id="#previous_step_button",
            manager=MANAGER,
            starting_height=2,
        )
        self.elements["done_button"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((0, 645), (147, 30))),
            "Done " + get_arrow(5, arrow_left=False),
            get_button_dict(ButtonStyles.MENU_RIGHT, (147, 30)),
            object_id="@buttonstyles_menu_right",
            manager=MANAGER,
            starting_height=2,
            anchors={"left_target": self.elements["previous_step"]},
        )
        self.elements["done_button"].disable()

        # create screen specific elements
        self.elements["text_container"] = pygame_gui.elements.UIAutoResizingContainer(
            ui_scale(pygame.Rect((85, 105), (0, 0))),
            object_id="text_container",
            starting_height=1,
            manager=MANAGER,
        )
        self.text["clan_name"] = pygame_gui.elements.UILabel(
            ui_scale(pygame.Rect((0, 0), (-1, -1))),
            text=f"{self.clan_name}Clan",
            container=self.elements["text_container"],
            object_id=get_text_box_theme("#text_box_40"),
            manager=MANAGER,
            anchors={"left": "left"},
        )
        self.text["biome"] = pygame_gui.elements.UILabel(
            ui_scale(pygame.Rect((0, 5), (-1, -1))),
            text=f"{self.biome_selected}",
            container=self.elements["text_container"],
            object_id=get_text_box_theme("#text_box_30_horizleft"),
            manager=MANAGER,
            anchors={
                "top_target": self.text["clan_name"],
            },
        )
        self.text["leader"] = pygame_gui.elements.UILabel(
            ui_scale(pygame.Rect((0, 5), (-1, -1))),
            text=f"Your name: {self.your_cat.name}",
            container=self.elements["text_container"],
            object_id=get_text_box_theme("#text_box_30_horizleft"),
            manager=MANAGER,
            anchors={
                "top_target": self.text["biome"],
            },
        )
        self.text["recommend"] = pygame_gui.elements.UILabel(
            ui_scale(pygame.Rect((0, 5), (-1, -1))),
            text=f"Recommended Symbol: N/A",
            container=self.elements["text_container"],
            object_id=get_text_box_theme("#text_box_30_horizleft"),
            manager=MANAGER,
            anchors={
                "top_target": self.text["leader"],
            },
        )
        self.text["selected"] = pygame_gui.elements.UILabel(
            ui_scale(pygame.Rect((0, 15), (-1, -1))),
            text=f"Selected Symbol: N/A",
            container=self.elements["text_container"],
            object_id=get_text_box_theme("#text_box_30_horizleft"),
            manager=MANAGER,
            anchors={
                "top_target": self.text["recommend"],
            },
        )

        self.elements["random_symbol_button"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((496, 206), (34, 34))),
            "\u2684",
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            manager=MANAGER,
        )

        self.elements["symbol_frame"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((540, 90), (169, 166))),
            get_box(BoxStyles.FRAME, (169, 166), sides=(True, True, False, True)),
            object_id="@boxstyles_frame",
            starting_height=1,
            manager=MANAGER,
        )

        self.elements["page_left"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((47, 414), (34, 34))),
            Icon.ARROW_LEFT,
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            starting_height=1,
            manager=MANAGER,
        )
        self.elements["page_right"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((719, 414), (34, 34))),
            Icon.ARROW_RIGHT,
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            starting_height=1,
            manager=MANAGER,
        )
        self.elements["filters_tab"] = UIImageButton(
            ui_scale(pygame.Rect((100, 619), (78, 30))),
            "",
            object_id="#filters_tab_button",
            starting_height=1,
            manager=MANAGER,
        )
        self.elements["symbol_list_frame"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((76, 250), (650, 370))),
            get_box(BoxStyles.ROUNDED_BOX, (650, 370)),
            object_id="#symbol_list_frame",
            starting_height=2,
            manager=MANAGER,
        )

        if f"symbol{self.clan_name.upper()}0" in sprites.clan_symbols:
            self.text["recommend"].set_text(
                f"Recommended Symbol: {self.clan_name.upper()}0"
            )

        if not self.symbol_selected:
            if f"symbol{self.clan_name.upper()}0" in sprites.clan_symbols:
                self.symbol_selected = f"symbol{self.clan_name.upper()}0"

                self.text["selected"].set_text(
                    f"Selected Symbol: {self.clan_name.upper()}0"
                )

        if self.symbol_selected:
            symbol_name = self.symbol_selected.replace("symbol", "")
            self.text["selected"].set_text(f"Selected Symbol: {symbol_name}")

            self.elements["selected_symbol"] = pygame_gui.elements.UIImage(
                ui_scale(pygame.Rect((573, 127), (100, 100))),
                pygame.transform.scale(
                    sprites.sprites[self.symbol_selected],
                    ui_scale_dimensions((100, 100)),
                ).convert_alpha(),
                object_id="#selected_symbol",
                starting_height=2,
                manager=MANAGER,
            )
            self.refresh_symbol_list()
            while self.symbol_selected not in self.symbol_buttons:
                self.current_page += 1
                self.refresh_symbol_list()
            self.elements["done_button"].enable()
        else:
            self.elements["selected_symbol"] = pygame_gui.elements.UIImage(
                ui_scale(pygame.Rect((573, 127), (100, 100))),
                pygame.transform.scale(
                    sprites.sprites["symbolADDER0"],
                    ui_scale_dimensions((100, 100)),
                ).convert_alpha(),
                object_id="#selected_symbol",
                starting_height=2,
                manager=MANAGER,
                visible=False,
            )
            self.refresh_symbol_list()

    def open_clan_saved_screen(self):
        self.clear_all_page()
        self.sub_screen = "saved screen"

        self.elements["selected_symbol"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((350, 105), (100, 100))),
            pygame.transform.scale(
                sprites.dark_mode_symbol(sprites.sprites[self.symbol_selected])
                if game.settings["dark mode"]
                else sprites.sprites[self.symbol_selected],
                ui_scale_dimensions((100, 100)),
            ).convert_alpha(),
            object_id="#selected_symbol",
            starting_height=1,
            manager=MANAGER,
        )

        self.elements["leader_image"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((350, 125), (100, 100))),
            pygame.transform.scale(
               self.your_cat.sprite, ui_scale_dimensions((100, 100))
            ),
            starting_height=1,
            manager=MANAGER,
        )
        self.elements["continue"] = UISurfaceImageButton(
            ui_scale(pygame.Rect((346, 250), (102, 30))),
            "continue",
            get_button_dict(ButtonStyles.SQUOVAL, (102, 30)),
            object_id="@buttonstyles_squoval",
            sound_id="save",
        )
        self.elements["save_confirm"] = pygame_gui.elements.UITextBox(
            "Welcome to the world, ' + self.your_cat.name.prefix + 'kit!",
            ui_scale(pygame.Rect((100, 135), (600, 30))),
            object_id=get_text_box_theme("#text_box_30_horizcenter"),
            manager=MANAGER,
        )

        self.get_camp_bg()

        scripts.screens.screens_core.screens_core.rebuild_bgs()

    def save_clan(self):
        self.handle_create_other_cats()
        game.mediated.clear()
        game.patrolled.clear()
        game.cat_to_fade.clear()
        Cat.outside_cats.clear()
        Patrol.used_patrols.clear()
        convert_camp = {1: "camp1", 2: "camp2", 3: "camp3", 4: "camp4", 5: 'camp5', 6: 'camp6'}
        game.clan = Clan(
            name=self.clan_name,
            leader=self.leader,
            deputy=self.deputy,
            medicine_cat=self.med_cat,
            biome=self.biome_selected,
            camp_bg=convert_camp[self.selected_camp_tab],
            symbol=self.symbol_selected,
            self.game_mode, self.members,
            starting_season=self.selected_season,
            your_cat=self.your_cat
        )
        game.clan.your_cat.moons = -1
        game.clan.create_clan()
        # game.clan.starclan_cats.clear()
        game.cur_events_list.clear()
        game.herb_events_list.clear()
        Cat.grief_strings.clear()
        Cat.sort_cats()

    def get_camp_art_path(self, campnum) -> Optional[str]:
        if not campnum:
            return None

        leaf = self.selected_season.replace("-", "")

        camp_bg_base_dir = "resources/images/camp_bg/"
        start_leave = leaf.casefold()
        light_dark = "dark" if game.settings["dark mode"] else "light"

        biome = self.biome_selected.lower()

        return (
            f"{camp_bg_base_dir}/{biome}/{start_leave}_camp{campnum}_{light_dark}.png"
        )

    def chunks(self, L, n):
        return [L[x : x + n] for x in range(0, len(L), n)]

    def draw_art_frame(self):
        if "art_frame" in self.elements:
            self.elements["art_frame"].kill()
        self.elements["art_frame"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect(((0, 20), (466, 416)))),
            get_box(BoxStyles.FRAME, (466, 416)),
            manager=MANAGER,
            anchors={"center": "center"},
        )

    def create_cat_info(self):
        self.elements["cat_name"] = pygame_gui.elements.UITextBox(
            "",
            ui_scale(pygame.Rect((0, 10), (250, 60))),
            visible=False,
            object_id=get_text_box_theme("#text_box_30_horizcenter"),
            manager=MANAGER,
            anchors={
                "top_target": self.elements["name_backdrop"],
                "centerx": "centerx",
            },
        )

        # info for chosen cats:
        self.elements["cat_info"] = pygame_gui.elements.UITextBox(
            "",
            ui_scale(pygame.Rect((440, 220), (175, 125))),
            visible=False,
            object_id=get_text_box_theme("#text_box_26_horizcenter"),
            manager=MANAGER,
        )


make_clan_screen = MakeClanScreen()
