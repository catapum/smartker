import textwrap
import datetime
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
from PIL import ImageFilter

from EPD import EPD

from data import msgs
from data import rgb_table
from data import books_history

import colours


WHITE = "white"
BLACK = "black"

SCREEN_WIDTH = 264
SCREEN_HEIGHT = 176

FIRST_BUTTON_AREA = [(1, int(SCREEN_HEIGHT*0.7)+4), (int(SCREEN_WIDTH*0.25)-2, SCREEN_HEIGHT-2)]
SECOND_BUTTON_AREA = [(int(SCREEN_WIDTH*0.25)+4, int(SCREEN_HEIGHT*0.7)+4), (int(SCREEN_WIDTH*0.5)-2, SCREEN_HEIGHT-2)]
THIRD_BUTTON_AREA = [(int(SCREEN_WIDTH*0.5)+4, int(SCREEN_HEIGHT*0.7)+4), (int(SCREEN_WIDTH*0.75)-2, SCREEN_HEIGHT-2)]
FOURTH_BUTTON_AREA = [(int(SCREEN_WIDTH*0.75)+4, int(SCREEN_HEIGHT*0.7)+4), (int(SCREEN_WIDTH)-2, SCREEN_HEIGHT-2)]

FIRST_MESSAGE_AREA = []
SECOND_MESSAGE_AREA = []
THIRD_MESSAGE_AREA = []

font_esc = ImageFont.truetype('Helvetica-Black.otf', 28)
font_message_header = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf', 16)
font_message_body = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerif.ttf', 14)
font_delete = ImageFont.truetype('Helvetica-Black.otf', 16)
font_question_mark = ImageFont.truetype('Helvetica-Black.otf', 60)

book_icon = Image.open("images/book-icon.png")
mail_icon = Image.open("images/mail-icon.png")
new_mail_icon = Image.open("images/new-mail-icon.png")
rgb_icon = Image.open("images/rgb-icon.png")
story_icon = Image.open("images/story.png")
up_icon = Image.open("images/up-icon.png")
down_icon = Image.open("images/down-icon.png")
trash_icon = Image.open("images/trash-icon.png")
check_icon = Image.open("images/check-icon.png")
equation = Image.open("images/equation.png")


#Books
the_wasp_factory = Image.open("images/the-wasp-factory.png")
middlesex = Image.open("images/middlesex.png")



epd = EPD()



class Screen(object):
    
    def __init__(self, *args, **kwargs):
        self.previous_screen = kwargs.get("previous_screen", None)
        self.button_1_text = "ESC"
        self.button_2_icon = None
        self.button_3_icon = None
        self.button_4_icon = None
        self.halt = False

    def display(self):
        if not self.halt:
            self.render()
            epd.display(self.image)
            epd.update()

    def open_image(self):
        if not self.halt:
            self.render()
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            self.image.show()

    def render(self):
        self.image = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT), color=WHITE)
        self.all_pixels = self.image.load()

        self.draw = ImageDraw.Draw(self.image)
        self.draw.line(xy=[(0, SCREEN_HEIGHT*0.7), (SCREEN_WIDTH, SCREEN_HEIGHT*0.7)], fill=BLACK, width=4)

        self.draw.line(xy=[(SCREEN_WIDTH*0.25, SCREEN_HEIGHT*0.7), (SCREEN_WIDTH*0.25, SCREEN_HEIGHT)], fill=BLACK, width=4)
        self.draw.line(xy=[(SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.7), (SCREEN_WIDTH*0.5, SCREEN_HEIGHT)], fill=BLACK, width=4)
        self.draw.line(xy=[(SCREEN_WIDTH*0.75, SCREEN_HEIGHT*0.7), (SCREEN_WIDTH*0.75, SCREEN_HEIGHT)], fill=BLACK, width=4)

        self.draw.text((2, int(SCREEN_HEIGHT*0.7)+10), self.button_1_text, fill=BLACK, font=font_esc)
        

    def press_1(self):
        #Go back
        self.halt = False
        self.visualize_button_press(FIRST_BUTTON_AREA)
        return self.previous_screen or self

    def press_2(self):
        self.visualize_button_press(SECOND_BUTTON_AREA)

    def press_3(self):
        self.visualize_button_press(THIRD_BUTTON_AREA)

    def press_4(self):
        self.visualize_button_press(FOURTH_BUTTON_AREA)


    def visualize_button_press(self, area):
        for x in range(area[0][0], area[1][0]):
            for y in range(area[0][1], area[1][1]):
                self.all_pixels[x,y] = 255 if self.all_pixels[x,y] < 200 else 0
        epd.display(self.image)
        epd.partial_update()



class MainScreen(Screen):


    def __init__(self, *args, **kwargs):
        super(MainScreen, self).__init__(*args, **kwargs)
        self.button_2_icon = mail_icon
        self.button_3_icon = book_icon
        self.button_4_icon = rgb_icon
        self.rgb_table = iter(colours.rgb_table)
        self.iteration = 0
        self.colour_found = True

    def render(self):
        super(MainScreen, self).render()
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("gmail.com",80))
            ip = s.getsockname()[0]
            s.close()
        except:
            ip = "unknown"
        if not self.colour_found:
            self.draw.text((20, 20), "NOT FOUND", fill=BLACK, font=font_esc)
        else:
            self.draw.text((20, 20), "SMARTKER", fill=BLACK, font=font_esc)
        self.draw.text((20, 100), "ip: " + ip , fill=BLACK, font=font_message_header)
        self.image.paste(self.button_2_icon, (int(SCREEN_WIDTH*0.25)+10, int(SCREEN_HEIGHT*0.7)+10))
        self.image.paste(self.button_3_icon, (int(SCREEN_WIDTH*0.5)+4, int(SCREEN_HEIGHT*0.7)+6))
        self.image.paste(self.button_4_icon, (int(SCREEN_WIDTH*0.75)+10, int(SCREEN_HEIGHT*0.7)+4))
        #self.image.paste(equation, (1,1))

    def press_2(self):
        #Go to messages
        super(MainScreen, self).press_2()
        return MessagesScreen(previous_screen=self)


    def press_3(self):
        #Go to list of books
        super(MainScreen, self).press_3()
        return BooksScreen(previous_screen=self)

    def press_4(self):
        #Go to read RGB
        super(MainScreen, self).press_4()
        #TO-DO: read rgb value and get book_id, page_no
        colour, table_entry = colours.closestEuclideanDistance(**colours.readColour())

        print table_entry
        try:
            self.colour_found = True
            return RGBScreen(previous_screen=self, book_id=table_entry["book_id"],
                             page_no=table_entry["page_no"],
                             recap=table_entry["recap"], title=table_entry["title"])
        except:
            self.colour_found = False
            return self


class MessagesScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(MessagesScreen, self).__init__(*args, **kwargs)
        self.button_2_icon = check_icon
        self.button_3_icon = down_icon
        self.button_4_icon = up_icon
        self.book_id = kwargs.get("book_id")
        self.page_no = kwargs.get("page_no")
        self.current_selected = 1

    def render(self, page=0):
        super(MessagesScreen, self).render()
        self.visible_messages = self.get_messages(self.book_id, self.page_no)[page*3:(page*3)+3]
        for idx, msg in enumerate(self.visible_messages, 1):
            
            from_ = (msg["from"][:10] + '..') if len(msg["from"]) > 10 else msg["from"]
            book = (msg["book_title"][:16] + '..') if len(msg["book_title"]) > 16 else msg["book_title"]
            
            self.draw.line(xy=[(20, idx*20), (SCREEN_WIDTH-10, idx*20)], fill=BLACK, width=3)
            self.draw.text((20, idx*20), from_+" - "+book, fill=BLACK, font=font_message_header)
            self.draw.line(xy=[(20, idx*20+20), (SCREEN_WIDTH-10, idx*20+20)], fill=BLACK, width=3)

            self.draw.polygon([(1,self.current_selected*20),(1,self.current_selected*20+20),(19, self.current_selected*20+10)], fill=BLACK)

        self.draw.text((20, 4*20), "More...", fill=BLACK, font=font_message_header)

        self.image.paste(self.button_2_icon, (int(SCREEN_WIDTH*0.25)+10, int(SCREEN_HEIGHT*0.7)+7))
        self.image.paste(self.button_3_icon, (int(SCREEN_WIDTH*0.5)+8, int(SCREEN_HEIGHT*0.7)+4))
        self.image.paste(self.button_4_icon, (int(SCREEN_WIDTH*0.75)+10, int(SCREEN_HEIGHT*0.7)+4))


    def move_cursor(self, unit=1):
        self.draw.polygon([(1,self.current_selected*20),(1,self.current_selected*20+20),(19, self.current_selected*20+10)], fill=WHITE)
        self.current_selected += unit
        self.draw.polygon([(1,self.current_selected*20),(1,self.current_selected*20+20),(19, self.current_selected*20+10)], fill=BLACK)


    def press_2(self):
        #Load message selected
        super(MessagesScreen, self).press_2()
        self.halt = False
        return SingleMessageScreen(previous_screen=self, msg=self.visible_messages[self.current_selected-1])


    def press_3(self):
        #Move cursor down
        
        super(MessagesScreen, self).press_3()
        self.move_cursor()
        super(MessagesScreen, self).press_3()


        if self.current_selected <= 3:
            self.halt = True
        elif self.current_selected == 4:
            self.halt = False
            self.current_selected = 1
        else:
            self.halt = False
        
        return self

    def press_4(self):
        #Move cursor up
        super(MessagesScreen, self).press_4()
        self.move_cursor(-1)
        super(MessagesScreen, self).press_4()
        if self.current_selected > 1:
            self.halt = True
        elif self.current_selected == 0:
            self.halt = False
            self.current_selected = 1
        else:
            self.halt = False
        
        return self


    def get_messages(self, book_id, page_no=0):
        if book_id:
            return [msg for msg in msgs if msg.get("book_id") == book_id and msg.get("page") <= page_no]
        else:
            #TO-DO return all read messages
            return [msg for msg in msgs if msg.get("read")]



class BooksScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(BooksScreen, self).__init__(*args, **kwargs)
        self.button_2_icon = story_icon
        self.button_3_icon = up_icon
        self.button_4_icon = down_icon
        self.current_selected = 1

    def get_books_history(self):
        print books_history
        books_history.sort(key=lambda x: x['accessed'])
        return (books_history[0], books_history[-1])
        

    def move_cursor(self, unit=1):
        offset = self.current_selected*1.5
        self.draw.polygon([(1, offset*20),(1, offset*20+20),(19, offset*20+10)], fill=WHITE)
        self.current_selected += unit
        self.draw.polygon([(1, offset*20),(1, offset*20+20),(19, offset*20+10)], fill=BLACK)


    def render(self, page=0):
        super(BooksScreen, self).render()
        least_recent, most_recent = self.get_books_history()

        self.draw.text((20, 10), "Least recent book", fill=BLACK, font=font_message_header)

        from_ = (least_recent["title"][:18] + '..') if len(least_recent["title"]) > 10 else least_recent["title"]
        book = (least_recent["accessed"][:10] + '..') if len(least_recent["accessed"]) > 16 else least_recent["accessed"]
        
        self.draw.line(xy=[(20, 30), (SCREEN_WIDTH-10, 30)], fill=BLACK, width=3)
        self.draw.text((20, 30), from_+" - "+book, fill=BLACK, font=font_message_header)
        self.draw.line(xy=[(20, 30+20), (SCREEN_WIDTH-10, 30+20)], fill=BLACK, width=3)

        self.draw.text((20, 60), "Most recent book", fill=BLACK, font=font_message_header)

        from_ = (most_recent["title"][:18] + '..') if len(most_recent["title"]) > 10 else most_recent["title"]
        book = (most_recent["accessed"][:10] + '..') if len(most_recent["accessed"]) > 16 else most_recent["accessed"]
        
        self.draw.line(xy=[(20, 80), (SCREEN_WIDTH-10, 80)], fill=BLACK, width=3)
        self.draw.text((20, 80), from_+" - "+book, fill=BLACK, font=font_message_header)
        self.draw.line(xy=[(20, 80+20), (SCREEN_WIDTH-10, 80+20)], fill=BLACK, width=3)
            

        self.draw.polygon([(1, 30),(1, 30+20),(19, 30+10)], fill=BLACK)

        self.image.paste(self.button_2_icon, (int(SCREEN_WIDTH*0.25)+10, int(SCREEN_HEIGHT*0.7)+7))
        self.image.paste(self.button_3_icon, (int(SCREEN_WIDTH*0.5)+8, int(SCREEN_HEIGHT*0.7)+4))
        self.image.paste(self.button_4_icon, (int(SCREEN_WIDTH*0.75)+10, int(SCREEN_HEIGHT*0.7)+4))

    def press_2(self):
        #Go to Story Screen
        super(BooksScreen, self).press_2()
        recap = self.get_books_history()[self.current_selected-1]["recap"]
        title = self.get_books_history()[self.current_selected-1]["title"]
        page_no = self.get_books_history()[self.current_selected-1]["page_no"]
        return StoryScreen(previous_screen=self, recap=recap, title=title, page_no=page_no)


    def press_3(self):
        #Move cursor down
        
        super(BooksScreen, self).press_3()
        self.move_cursor()
        super(BooksScreen, self).press_3()


        if self.current_selected <= 3:
            self.halt = True
        elif self.current_selected == 4:
            self.halt = False
            self.current_selected = 1
        else:
            self.halt = False
        
        return self

    def press_4(self):
        #Move cursor up
        super(BooksScreen, self).press_4()
        self.move_cursor(-1)
        super(BooksScreen, self).press_4()
        if self.current_selected > 1:
            self.halt = True
        elif self.current_selected == 0:
            self.halt = False
            self.current_selected = 1
        else:
            self.halt = False
        
        return self

class RGBScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(RGBScreen, self).__init__(*args, **kwargs)
        self.button_3_icon = mail_icon
        self.button_3_icon_alt = new_mail_icon
        self.button_4_icon = story_icon
        self.book_id = kwargs["book_id"]
        self.page_no = kwargs["page_no"]
        self.recap = kwargs["recap"]
        self.title = kwargs["title"]

    def render(self):
        super(RGBScreen, self).render()
        if self.book_id == 1:
            self.image.paste(self.button_3_icon, (int(SCREEN_WIDTH*0.5)+10, int(SCREEN_HEIGHT*0.7)+10))
        if self.book_id == 2:
            self.image.paste(self.button_3_icon_alt, (int(SCREEN_WIDTH*0.5)+5, int(SCREEN_HEIGHT*0.7)+8))

        self.image.paste(self.button_4_icon, (int(SCREEN_WIDTH*0.75)+10, int(SCREEN_HEIGHT*0.7)+4))
        if self.book_id == 3:
            self.image.paste(middlesex, (1,1))
        if self.book_id == 1:
            self.image.paste(the_wasp_factory, (1,1))
        if self.book_id == 5:
            self.image.paste(Image.open("images/scatterplot.png"), (1,1))
        

    def press_2(self):
        #Do Nothing
        return self


    def press_3(self):
        #Go to book messages
        super(RGBScreen, self).press_3()
        return MessagesScreen(previous_screen=self, book_id=self.book_id, page_no=self.page_no)

    def press_4(self):
        #Go to Story screen
        super(RGBScreen, self).press_4()
        return StoryScreen(previous_screen=self, recap=self.recap, title=self.title, page_no=self.page_no)

class SingleMessageScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(SingleMessageScreen, self).__init__(*args, **kwargs)
        self.button_2_icon = trash_icon
        self.button_3_icon = down_icon
        self.button_4_icon = up_icon
        self.msg = kwargs["msg"]
        self.current_page = 0
        self.font_aux = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf', 14)

    def render(self):
        super(SingleMessageScreen, self).render()
        from_ = (self.msg["from"][:20] + '..') if len(self.msg["from"]) > 20 else self.msg["from"]
        
        self.draw.text((10, 5), "From: " + from_, fill=BLACK, font=font_message_header)
        self.draw.line(xy=[(10, 25), (SCREEN_WIDTH-10, 25)], fill=BLACK, width=3)

        offset = 35
        lines = textwrap.wrap(self.msg["body"], width=40)
        self.total_pages = len(lines)/4 or 1
        lines = lines[self.current_page*4:(self.current_page+1)*4]

        for line in lines:
            self.draw.text((10, offset), line, font=self.font_aux, fill=BLACK)
            offset += font_message_body.getsize(line)[1]

        if self.current_page < self.total_pages - 1:
            
            self.draw.text((SCREEN_WIDTH-50, offset), "(More...)", font=self.font_aux, fill=BLACK)

        self.image.paste(self.button_2_icon, (int(SCREEN_WIDTH*0.25)+8, int(SCREEN_HEIGHT*0.7)+4))
        self.image.paste(self.button_3_icon, (int(SCREEN_WIDTH*0.5)+6, int(SCREEN_HEIGHT*0.7)+6))
        self.image.paste(self.button_4_icon, (int(SCREEN_WIDTH*0.75)+10, int(SCREEN_HEIGHT*0.7)+4))

        if not self.msg["read"]:
            self.msg["read"] = True


    def press_2(self):
        #Delete message
        super(SingleMessageScreen, self).press_2()
        super(SingleMessageScreen, self).press_2()
        return DeleteMessageScreen(previous_screen=self.previous_screen, msg=self.msg)

    def press_3(self):
        #Move cursor down
        if self.current_page == self.total_pages - 1:
            self.halt = True
        else:
            self.halt = False
        if self.current_page < self.total_pages - 1:
            self.current_page += 1

        super(SingleMessageScreen, self).press_3()
        super(SingleMessageScreen, self).press_3()
        return self

    def press_4(self):
        #Move cursor up
        if self.current_page == 0:
            self.halt = True
        else:
            self.halt = False
        if self.current_page > 0:
            self.current_page -= 1

        super(SingleMessageScreen, self).press_4()
        super(SingleMessageScreen, self).press_4()
        return self

class StoryScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(StoryScreen, self).__init__(*args, **kwargs)
        self.button_3_icon = down_icon
        self.button_4_icon = up_icon
        self.title = kwargs["title"]
        self.recap = kwargs["recap"]
        self.page_no = kwargs["page_no"]
        self.current_page = 0

    def display(self):
        if not self.halt:
            if self.title == "Hunter Hunter":
                self.comic_recap()
                return
            if self.title == "Textbook":
                self.scatterplot()
                return
            self.render()
            epd.display(self.image)
            epd.update()
            self.partial_recap()

    def render(self):
        super(StoryScreen, self).render()
        from_ = (self.title[:20] + '..') if len(self.title) > 20 else self.title + " p" + str(self.page_no)
        
        self.draw.text((10, 5), from_, fill=BLACK, font=font_message_header)
        self.draw.line(xy=[(10, 25), (SCREEN_WIDTH-10, 25)], fill=BLACK, width=3)

        self.image.paste(self.button_3_icon, (int(SCREEN_WIDTH*0.5)+6, int(SCREEN_HEIGHT*0.7)+6))
        self.image.paste(self.button_4_icon, (int(SCREEN_WIDTH*0.75)+10, int(SCREEN_HEIGHT*0.7)+4))

    def partial_recap(self):
        v_offset = 35
        h_offset = 10
        lines = textwrap.wrap(self.recap, width=40)
        self.total_pages = len(lines)/4 or 1
        lines = lines[self.current_page*4:(self.current_page+1)*4]

        for line in lines:
            for word in line.split():
                self.draw.text((h_offset, v_offset), word, font=font_message_body, fill=BLACK)
                epd.display(self.image)
                epd.partial_update()
                h_offset += font_message_body.getsize(word+" ")[0]
            h_offset = 10
            v_offset += font_message_body.getsize(line)[1]

        if self.current_page < self.total_pages - 1:
            self.draw.text((SCREEN_WIDTH-50, v_offset), "(More...)", font=font_message_body, fill=BLACK)
            epd.display(self.image)
            epd.partial_update()

    def comic_recap(self):
        images = ["hunter-1.png", "hunter-2.png", "hunter-3.png"]
        super(StoryScreen, self).render()
        for i in images:
            self.image.paste(Image.open("images/" + i), (1,1))
            epd.display(self.image)
            epd.update()
            time.sleep(1)



    def press_2(self):
        #do nothing
        self.halt = True
        return self


    def press_3(self):
        #Move cursor down
        if self.current_page == self.total_pages - 1:
            self.halt = True
        else:
            self.halt = False
        if self.current_page < self.total_pages - 1:
            self.current_page += 1

        super(StoryScreen, self).press_3()
        super(StoryScreen, self).press_3()
        return self

    def press_4(self):
        #Move cursor up
        if self.current_page == 0:
            self.halt = True
        else:
            self.halt = False
        if self.current_page > 0:
            self.current_page -= 1

        super(StoryScreen, self).press_4()
        super(StoryScreen, self).press_4()
        return self

class DeleteMessageScreen(Screen):
    
    def __init__(self, *args, **kwargs):
        super(DeleteMessageScreen, self).__init__(*args, **kwargs)
        self.button_1_text = "YES"
        self.button_2_text = "NO"
        self.msg_id = kwargs["msg"]["id"]
        self.msg = kwargs["msg"]

    def render(self):
        super(DeleteMessageScreen, self).render()
        from_ = (self.msg["from"][:20] + '..') if len(self.msg["from"]) > 20 else self.msg["from"]
        
        self.draw.text((10, 25), "Delete message From:", fill=BLACK, font=font_delete)
        self.draw.text((10, 55), from_, fill=BLACK, font=font_delete)
        self.draw.text((int(SCREEN_WIDTH*0.75)+20, 10), "?", fill=BLACK, font=font_question_mark)

        self.draw.text((int(SCREEN_WIDTH*0.25)+8, int(SCREEN_HEIGHT*0.7)+10), self.button_2_text, fill=BLACK, font=font_esc)

    def press_1(self):
        #TO-DO delete message
        self.halt = False
        super(DeleteMessageScreen, self).press_1()
        to_delete = False
        for idx, m in enumerate(msgs):
            if m["id"] == self.msg_id:
                to_delete = idx
        if to_delete != False:
            msgs.pop(to_delete)

        return self.previous_screen
        

    def press_2(self):
        #Do not delete message
        self.halt = False
        super(DeleteMessageScreen, self).press_2()
        return self.previous_screen


    def press_3(self):
        #do nothing
        self.halt = True
        return self
        

    def press_4(self):
        #do nothing
        self.halt = True
        return self
        





    