from .worm import Worm
from .fanfictiondotnet import FanfictionDotNet
from .citadel import Citadel
from .pact import Pact
from .magnitude import OrdersOfMagnitude
from .spacebattles import Spacebattles
from .twig import Twig

scrapers = [
    Worm(), FanfictionDotNet(), Citadel(), Pact(), OrdersOfMagnitude(), Spacebattles(), Twig()
]
