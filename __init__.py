from aqt import mw, browser
from aqt.qt import *
from anki.hooks import addHook
from aqt.utils import tooltip, askUser
from anki.consts import CARD_TYPE_NEW

class ease_reset:
    
    def setup_menu(self):
        action = QAction("Reset Ease of Current Deck", mw);
        action.triggered.connect(self.reset_selected_cards);
        mw.form.menuTools.addAction(action);

    def reset_selected_cards(self) -> None:
        deck_id = mw.col.decks.get_current_id();
        if not deck_id:
            tooltip("No current deck selected.");
            return None
        
        deck_name = mw.col.decks.name_if_exists(deck_id)
        if None == deck_name:
            tooltip("Invalid deck name.")
            return None

        result = askUser("Reset ease of all cards in deck \'{0}\'?".format(deck_name), None, None, False, None, "Reset Ease"); 
        if False == result:
            return None

        cards = mw.col.decks.cids(deck_id, False);
        if not cards:
            tooltip("No cards found.");
            return None;
        
        for card_id in cards:
            card = mw.col.get_card(card_id);
            if card == None:
                break
           
            # Avoid messing with new cards.
            if card.type == CARD_TYPE_NEW:
                continue

            # Avoid changing cards that already have the default ease.
            # This is so you don't have to sync every single card again.
            if card.factor == 2500:
                continue

            card.factor = 2500;
            card.flush();

        tooltip("Ease Reset")


def ease_reset_init():
    if False == hasattr(mw, 'ease_reset'):
        mw.ease_reset = ease_reset();
        mw.ease_reset.setup_menu();
addHook("profileLoaded", ease_reset_init);

#def ease_reset_finalize():
#    mw.ease_reset = None;
