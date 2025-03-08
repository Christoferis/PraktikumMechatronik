# setup logging
import logging
from constants import MIN_LOG_LVL

logging.basicConfig(format='[%(levelname)s] %(message)s', level=MIN_LOG_LVL)

# import and run other things
import com_impl
import gp_layer
import ui