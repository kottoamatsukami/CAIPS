#
# Эта библиотека была сделана после бесчисленных попыток оптимизировать систему из лабы
#

import decimal


# >---------------
# Hyper parameters:
PRECISION = 1000000

# >---------------

decimal.MAX_PREC = PRECISION


# Constants
pi = decimal.Decimal("3.14159265358979323846")