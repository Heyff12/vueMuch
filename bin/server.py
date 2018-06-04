# coding=utf-8

from gevent import monkey
monkey.patch_all()

import os
import sys

from qfcommon.base import loader
HOME = os.path.dirname(os.path.abspath(__file__))
loader.loadconf(HOME)
sys.path.append(os.path.dirname(HOME))


from qfcommon.base import logger, dbpool
from qfcommon.web import core, runner, cache
cache.install()
import dbenc

from bin import urls
from conf import config

if config.LOG_WHEN:
    log = logger.install(config.LOGFILE, when=config.LOG_WHEN)
else:
    log = logger.install(config.LOGFILE)


def _trans_token_db_conf(db_settings):
    import copy
    db_settings = copy.deepcopy(db_settings)

    ret = {}
    dbconf = dbenc.DBConf()

    for db_name, db_cfg in db_settings.items():
        token = db_cfg.pop('token')
        new_cfg = dbconf.get_dbpool(token, **db_cfg)

        ret[db_name] = new_cfg

    return ret


# 导入web urls
config.URLS = urls.urls
log.debug('<<< INSTALL DB>>>')
config.DATABASE = _trans_token_db_conf(config.dbcf)
dbpool.install(config.DATABASE)

app = core.WebApplication(config)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        config.PORT = int(sys.argv[2])
    runner.run_gevent(app, host=config.HOST, port=config.PORT)
