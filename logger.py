import logging
from rich.logging import RichHandler
from rich.console import Console


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

LOGGER = logging.getLogger("rich")

# Configure rich console
console = Console()
