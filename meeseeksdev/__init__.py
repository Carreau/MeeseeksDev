import os
import base64
import signal

org_whitelist = ['MeeseeksBox', 'Jupyter', 'IPython', 'JupyterLab', 'Carreau',
        'matplotlib', 'scikit-learn', 'pandas-dev']

usr_whitelist = [
        'Carreau',
        'gnestor',
        'ivanov',
        'fperez',
        'mpacer',
        'minrk',
        'takluyver',
        'sylvaincorlay',
        'ellisonbg',
        'blink1073',
        'damianavila',
        'jdfreder',
        'rgbkrk',
        'tacaswell',
        'willingc',
        'jhamrick',
        'lgpage',
        'jasongrout',
        'ian-r-rose',
        #matplotlib people
        'tacaswell',
        'QuLogic',
        'anntzer',
        'NelleV',
        'dstansby',
        'efiring',
        'choldgraf',
        'dstansby',
        'dopplershift',
        'jklymak',
        'weathergod',
        'timhoffm',
        #pandas-dev
        'jreback',
        'jorisvandenbossche',
        'gfyoung',
        'TomAugspurger',
        ]

# https://github.com/integrations/meeseeksdev/installations/new
# already ? https://github.com/organizations/MeeseeksBox/settings/installations/4268
# https://github.com/integration/meeseeksdev

def load_config_from_env():
    """
    Load the configuration, for now stored in the environment
    """
    config={}

    integration_id = os.environ.get('GITHUB_INTEGRATION_ID')
    botname = os.environ.get('GITHUB_BOT_NAME', None)

    if not integration_id:
        raise ValueError('Please set GITHUB_INTEGRATION_ID')

    if not botname:
        raise ValueError('Need to set a botname')
    if "@" in botname:
        print("Don't include @ in the botname !")

    botname = botname.replace('@','')
    at_botname = '@'+botname
    integration_id = int(integration_id)

    config['key'] = base64.b64decode(bytes(os.environ.get('B64KEY'), 'ASCII'))
    config['botname'] = botname
    config['at_botname'] = at_botname
    config['integration_id'] = integration_id
    config['webhook_secret'] = os.environ.get('WEBHOOK_SECRET')

    return Config(**config).validate()

from .meeseeksbox.core import MeeseeksBox
from .meeseeksbox.core import Config
from .meeseeksbox.commands import replyuser, zen, backport, tag, untag, pep8ify, quote, say, party
from .commands import close, open as _open, migrate_issue_request, ready, merge, help_make

def main():
    print('====== (re) starting ======')
    config = load_config_from_env()
    config.org_whitelist = org_whitelist + [o.lower() for o in org_whitelist]
    config.user_whitelist = usr_whitelist + [u.lower() for u in usr_whitelist]
    commands = {
        'hello': replyuser,
        'zen': zen,
        'backport': backport,
        'migrate': migrate_issue_request,
        'tag': tag,
        'untag': untag,
        'open': _open,
        'close': close,
        'autopep8': pep8ify,
        'ready': ready,
        'merge': merge,
        'say': say,
        'party': party,
    }
    commands['help'] = help_make(commands)
    box = MeeseeksBox(commands=commands, config=config)

    signal.signal(signal.SIGTERM, box.sig_handler)
    signal.signal(signal.SIGINT, box.sig_handler)

    box.start()


if __name__ == "__main__":
    main()
