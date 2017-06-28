from .worm import Worm
from .fanfictiondotnet import FanfictionDotNet
from .citadel import Citadel
from .pact import Pact
from .magnitude import OrdersOfMagnitude
from .spacebattles import Spacebattles

scrapers = [
    Worm(), FanfictionDotNet(), Citadel(), Pact(), OrdersOfMagnitude(), Spacebattles()
]
