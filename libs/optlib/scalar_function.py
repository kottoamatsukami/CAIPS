import numpy as np
import tqdm


class GradientDescent(object):
    def __init__(self, function) -> None:
        self.function = function
