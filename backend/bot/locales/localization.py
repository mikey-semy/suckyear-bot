import logging
from pathlib import Path
from fluent.runtime import FluentLocalization, FluentResourceLoader
from bot.utils.plural import ru_plural

def setup_localization(base_path: Path = Path(__file__).parent) -> FluentLocalization:
    logging.info("""Loading localization from %s""", base_path)
    locales_path = base_path.joinpath("locales")
    l10n_loader = FluentResourceLoader(str(locales_path) + "/{locale}")
    
    return FluentLocalization(
        ["ru"],
        ["strings.ftl", "errors.ftl"],
        l10n_loader,
        functions={'PLURAL': ru_plural}
    )