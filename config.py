#! usr/bin/env python

"""
@author:liqing
@email:626924971@qq.com
@tel:18674450812
@version:v1.0
function:set log
"""

from oslo_config import cfg
from oslo_log import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "demo"

logging.register_options(CONF)
logging.setup(CONF, DOMAIN)

LOG.info("Oslo Logging")
LOG.warning("Oslo Logging")
LOG.error("Oslo Logging")
