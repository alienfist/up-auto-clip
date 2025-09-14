# -*- coding: UTF-8 -*-
# logger.py

import logging

def setup_logger():
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

setup_logger()

logger = logging.getLogger(__name__)
