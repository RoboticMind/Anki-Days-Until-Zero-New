# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect, tr
# import all of the Qt GUI library
from aqt.qt import *

from aqt import gui_hooks

#for type hints
from aqt.deckbrowser import DeckBrowser
from aqt.overview import OverviewContent

from math import ceil, inf
from datetime import datetime, timedelta
import bs4

"""
    Runs right after the deck browser generates HTML
    Uses BeautifulSoup to modify the HTML before actually rendered
"""
def on_deck_browser_will_render_content(deck_browser: DeckBrowser, content: OverviewContent):
    soup = bs4.BeautifulSoup(content.tree, features="lxml")

    #change table headers
    soup.tr.attrs["colspan"] = 6

    th = soup.new_tag("th", attrs={"align":"center"})
    th.string = "Days to 0 new"
    #add one before the end
    headers = soup.tr.findChildren()
    headers[len(headers) - 2].insert_after(th)


    #change entries
    mapping = {}
    decks = mw.col.decks.all()
    for deck in decks:
        deck_id = deck["id"]
        
        if deck_id==1: #skip, not in UI
            continue 
        
        #check if a per deck setting is set
        per_deck_limit = deck["newLimit"]

        #get conf to get per day count
        #not perfect with sub decks, doesn't look at if a sub deck is limiting factor
        if not per_deck_limit:
            deck_conf_id = deck["conf"]
            config = mw.col.decks.get_config(deck_conf_id)
            per_day = config["new"]["perDay"]
        else:
            per_day = per_deck_limit
        
        #find all the new cards, excluding suspended cards
        deck_name = deck["name"]
        query = "is:new -is:suspended deck:\"{}\"".format(deck_name)
        new_cards = len(mw.col.find_cards(query))

        if per_day == 0:
            days_left = inf
        else:
            days_left = new_cards / per_day
        
        if days_left == inf:
            future_date = datetime.max
        else:
            future_date = datetime.now() + timedelta(days=ceil(days_left))

        #eg. May 21 if current year, May 2040 if further ahead
        date_fmt:str
        if days_left == 0:
            date_fmt = "done"
        elif future_date.year != datetime.now().year:
            date_fmt = "%b %Y"
        else:
            date_fmt = "%b %d"
        done_date = future_date.strftime(date_fmt)

        row = soup.find("tr", {"id": str(deck_id)})
        if not row: #collapsed or other similar scenarios
            continue 

        #add the days + date to the row
        #html looks something like
        #<td>x days<span class="zero-count">(date)</span></td>
        new_entry = soup.new_tag("td", align="center")
        new_entry.string = "{:.1f} days ".format(days_left)

        day_count = soup.new_tag("span", attrs={"class":"zero-count"})
        day_count.string = "(" + done_date + ")"
        new_entry.append(day_count)

        row_entries = row.findChildren()
        last_entry = row_entries[len(row_entries) - 2]
        last_entry.parent.insert_before(new_entry)

    content.tree = str(soup)
    print(soup.prettify())

gui_hooks.deck_browser_will_render_content.append(on_deck_browser_will_render_content)