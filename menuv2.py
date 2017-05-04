
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

from EPD import EPD

WHITE = "white"
BLACK = "black"

SCREEN_WIDTH = 264
SCREEN_HEIGHT = 176

FIRST_BUTTON_AREA = [(1, int(SCREEN_HEIGHT*0.7)+4), (int(SCREEN_WIDTH*0.25)-2, SCREEN_HEIGHT-2)]
SECOND_BUTTON_AREA = [(int(SCREEN_WIDTH*0.25)+4, int(SCREEN_HEIGHT*0.7)+4), (int(SCREEN_WIDTH*0.5)-2, SCREEN_HEIGHT-2)]
THIRD_BUTTON_AREA = [(int(SCREEN_WIDTH*0.5)+4, int(SCREEN_HEIGHT*0.7)+4), (int(SCREEN_WIDTH*0.75)-2, SCREEN_HEIGHT-2)]
FOURTH_BUTTON_AREA = [(int(SCREEN_WIDTH*0.75)+4, int(SCREEN_HEIGHT*0.7)+4), (int(SCREEN_WIDTH)-2, SCREEN_HEIGHT-2)]


font_letter = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf', 30)

book_icon = Image.open("images/book-icon.png")
mail_icon = Image.open("images/mail-icon.png")
rgb_icon = Image.open("images/rgb-icon.png")

#TO-DO
#story_icon = Image.open("images/story-icon.png") 
#up_icon = Image.open("images/up-icon.png")
#down_icon = Image.open("images/down-icon.png")
######

# screen = Image.new("L", (SCREEN_WIDTH, SCREEN_HEIGHT), color=WHITE)
# all_pixels = screen.load()


# draw = ImageDraw.Draw(screen)
# draw.line(xy=[(0, SCREEN_HEIGHT*0.7), (SCREEN_WIDTH, SCREEN_HEIGHT*0.7)], fill=BLACK, width=4)

# draw.line(xy=[(SCREEN_WIDTH*0.25, SCREEN_HEIGHT*0.7), (SCREEN_WIDTH*0.25, SCREEN_HEIGHT)], fill=BLACK, width=4)
# draw.line(xy=[(SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.7), (SCREEN_WIDTH*0.5, SCREEN_HEIGHT)], fill=BLACK, width=4)
# draw.line(xy=[(SCREEN_WIDTH*0.75, SCREEN_HEIGHT*0.7), (SCREEN_WIDTH*0.75, SCREEN_HEIGHT)], fill=BLACK, width=4)

# draw.text((0, int(SCREEN_HEIGHT*0.7)+12), "ESC", fill=BLACK, font=font_letter)

# screen.paste(mail_icon, (int(SCREEN_WIDTH*0.25)+10, int(SCREEN_HEIGHT*0.7)+10))
# screen.paste(book_icon, (int(SCREEN_WIDTH*0.5)+4, int(SCREEN_HEIGHT*0.7)+6))
# screen.paste(rgb_icon, (int(SCREEN_WIDTH*0.75)+10, int(SCREEN_HEIGHT*0.7)+4))


# screen.show()

epd = EPD()
epd.clear()


class Screen():
    
    def __init__(self,previous_screen=None):
        self.previous_screen = previous_screen
        self.button_1_text = "ESC"
        self.button_2_icon = None
        self.button_3_icon = None
        self.button_4_icon = None

    def render():
        self.image = Image.new("L", (SCREEN_WIDTH, SCREEN_HEIGHT), color=WHITE)
        self.all_pixels = image.load()

        draw = ImageDraw.Draw(image)
        draw.line(xy=[(0, SCREEN_HEIGHT*0.7), (SCREEN_WIDTH, SCREEN_HEIGHT*0.7)], fill=BLACK, width=4)

        draw.line(xy=[(SCREEN_WIDTH*0.25, SCREEN_HEIGHT*0.7), (SCREEN_WIDTH*0.25, SCREEN_HEIGHT)], fill=BLACK, width=4)
        draw.line(xy=[(SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.7), (SCREEN_WIDTH*0.5, SCREEN_HEIGHT)], fill=BLACK, width=4)
        draw.line(xy=[(SCREEN_WIDTH*0.75, SCREEN_HEIGHT*0.7), (SCREEN_WIDTH*0.75, SCREEN_HEIGHT)], fill=BLACK, width=4)

        draw.text((0, int(SCREEN_HEIGHT*0.7)+12), self.button_1_text, fill=BLACK, font=font_letter)

        image.paste(self.button_2_icon, (int(SCREEN_WIDTH*0.25)+10, int(SCREEN_HEIGHT*0.7)+10))
        image.paste(self.button_3_icon, (int(SCREEN_WIDTH*0.5)+4, int(SCREEN_HEIGHT*0.7)+6))
        image.paste(self.button_4_icon, (int(SCREEN_WIDTH*0.75)+10, int(SCREEN_HEIGHT*0.7)+4))
        epd.display(image)
        epd.update()

    def press_1():
        #Go back
        self.visualize_button_press(FIRST_BUTTON_AREA)
        return self.previous_screen

    def press_2():
        self.visualize_button_press(SECOND_BUTTON_AREA)

    def press_3():
        self.visualize_button_press(THIRD_BUTTON_AREA)

    def press_4():
        self.visualize_button_press(FOURTH_BUTTON_AREA)


    def visualize_button_press(self, area):
        for x in range(area[0][0], area[1][0]):
            for y in range(area[0][1], area[1][1]):
                self.all_pixels[x,y] = 255 if not all_pixels[x,y] else 0
        epd.display(self.image)
        epd.partial_update()



class MainScreen(Screen):


    def __init__(self):
        self.button_2_icon = mail_icon
        self.button_3_icon = book_icon
        self.button_4_icon = rgb_icon


    def press_1():
        super(Screen, self).press_1()
        pass

    def press_2():
        #Go to messages
        super(Screen, self).press_2()
        return MessagesScreen


    def press_3():
        #Go to list of books
        super(Screen, self).press_3()
        return BooksScreen

    def press_4():
        #Go to read RGB
        super(Screen, self).press_4()
        return RGBScreen


class MessagesScreen(Screen):

    def __init__(self):
        pass


    def press_2():
        #Load message selected
        return SingleMessageScreen


    def press_3():
        #Move cursor down
        pass

    def press_4():
        #Move cursor up
        pass

class BooksScreen(Screen):
    def __init__(self):
        self.button_2_icon = story_icon
        self.button_3_icon = up_icon
        self.button_4_icon = down_icon


    def press_2():
        #Go to Story Screen
        return StoryScreen


    def press_3():
        #Move cursor down
        pass

    def press_4():
        #Move cursor up
        pass

class RGBScreen(Screen):
    def __init__(self):
        self.button_2_icon = mail_icon
        self.button_3_icon = story_icon


    def press_2():
        #Do Nothing
        pass


    def press_3():
        #Go to book messages
        return SingleMessageScreen

    def press_4():
        #Go to Story screen
        return StoryScreen

class SingleMessageScreen(Screen):
    def __init__(self):
        pass

    def press_2():
        #Do Nothing
        return DeleteMessageScreen


    def press_3():
        #Move cursor down
        pass

    def press_4():
        #Move cursor up
        pass

class StoryScreen(Screen):
    def __init__(self):
        pass

    def press_2():
        #Do Nothing
        pass


    def press_3():
        #Move cursor down
        pass

    def press_4():
        #Move cursor up
        pass

class DeleteMessageScreen(Screen):
    
    def __init__(self):
        pass


    def press_1():
        #Delete message
        pass

    def press_2():
        #Do not delete message
        pass


    def press_3():
        #do nothing
        pass

    def press_4():
        #do nothing
        pass





    