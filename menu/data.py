
from collections import namedtuple
from itertools import cycle

RGBKey = namedtuple("RGBKey", ["red", "green", "blue"])


rgb_table = {RGBKey(101, 96, 58): {"book_id": 4, "page_no": 99, "recap":"", "title": "Hunter Hunter"},
             RGBKey(64, 92, 96): {"book_id": 3, "page_no": 120, "recap":"Desdemona wants her brother to find a nice gal, so she tries to hook him up with some of the girls in the village.", "title": "Middlesex"},
             RGBKey(44, 95, 112): {"book_id": 1, "page_no": 92, "recap":"Eric began to set dogs to the fire, and feed children with worms. He was taken to the hospital, but he managed to escape.", "title": "The Wasp Factory"},
             RGBKey(22, 90, 152): "D",
             RGBKey(38, 92, 130): "N",
             RGBKey(26, 87, 139): "U",
             RGBKey(46, 123, 81): {"book_id": 3, "page_no": 122, "recap":"Those girls just don't do it for him, though. Lefty jokes that he should just marry Desdemona. You are my third cousin, too. Third cousins can marry.", "title": "Middlesex"},
             RGBKey(30, 92, 143): "J",
             #RGBKey(118, 78, 88): "L",
             RGBKey(118, 78, 88): {"book_id": 1, "page_no": 124, "recap":"Once upon a time...", "title": "The Wasp Factory"},
             RGBKey(122, 77, 61): {"book_id": 3, "page_no": 120, "recap":"Those girls just don't do it for him, though. Lefty jokes that he should just marry Desdemona. You are my third cousin, too. Third cousins can marry.", "title": "Middlesex"},
             RGBKey(120, 75, 70): {"book_id": 5, "page_no": 48, "recap":"", "title": "Textbook"},}




msgs = [{"from": "Dad",
                        "book_id": 1,
                        "book_title": "The Wasp Factory", 
                        "read": False,
                        "page": 10,
                        "id": 1,
                        "body": """This book is definitely not appropiated to your little sister yet. Don't let her read it."""},
                  {"from": "Louisa",
                    "id": "1",
                       "read": True,
                       "book_id": 1,
                       "page": 20,
                       "book_title": "The Wasp Factory", 
                       "body": """I'm so happy you recommended this book to me. This chapter was brilliant."""},
                  {"from": "Guillermo",
                       "read": True,
                       "book_id": 2,
                       "page": 70,
                       "id": "3",
                       "book_title": "Middlesex", 
                       "body": """It's amazing how well this books describes how was life in Greece at the beginning of the XX century. It reminds me a lot of our holidays there. Mwah!"""}
                  ]

books_history = [{"accessed": "2010-04-01", "book_id": 1, "page_no": 77, "recap":"Once upon a time...", "title": "The Wasp Factory"},
                 {"accessed": "2014-04-01", "book_id": 2, "page_no": 100, "recap":"Once upon a time...", "title": "The Corrections"}
                 ]

rgb_table_iter = [{"book_id": 1, "page_no": 77, "recap":"Eric began to set dogs to the fire, and feed children with worms. He was taken to the hospital, but he managed to escape.", "title": "The Wasp Factory"},
                      {"book_id": 2, "page_no": 115, "recap":"Desdemona wants her brother to find a nice gal, so she tries to hook him up with some of the girls in the village. Those girls just don't do it for him, though. Lefty jokes that he should just marry Desdemona. You are my third cousin, too. Third cousins can marry", "title": "Middlesex"}]