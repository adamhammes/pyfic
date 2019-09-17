from sources.practicalguidetoevil.practicalguidetoevil import PracticalGuideToEvil

from .citadel import Citadel
from .fanficsme import FanficsMe
from .fanfictiondotnet import FanfictionDotNet
from .magnitude import OrdersOfMagnitude
from .pact import Pact
from .practicalguidetoevil import PracticalGuideToEvil
from .royalroad import RoyalRoadScraper
from .spacebattles import Spacebattles
from .twig import Twig
from .worm import Worm
from .worththecandle import WorthTheCandle


scrapers = [
    Worm(),
    FanfictionDotNet(),
    Citadel(),
    Pact(),
    OrdersOfMagnitude(),
    Spacebattles(),
    Twig(),
    FanficsMe(),
    PracticalGuideToEvil(),
    RoyalRoadScraper(),
    WorthTheCandle(),
]
