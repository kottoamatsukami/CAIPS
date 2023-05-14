import numpy as np
import tqdm
import itertools
#from numba import njit


class Grid(object):
    def __init__(self, start: float, stop: float, step: float, x: str, y: str) -> None:
        self.start = start
        self.stop = stop
        self.step = step
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return 'Grid({}, {})'.format(self.x, self.y)


class GDUniformGrid(object):
    def __init__(self) -> None:
        self.grid = None
        self.grid_size = 0
        self.best_solution = None
        self.best_criterion = float('inf')

    def optimize(
            self,
            function,
            vector_length: int,
            min_value: float,
            max_value: float,
            step: float,
            iters: int,
            criterion,
            target: float,
    ):
        self.grid = itertools.combinations_with_replacement(
            self.xrange(
                start=min_value,
                stop=max_value,
                step=step
            ),
            r=vector_length
        )
        self.grid_size = round(abs(max_value-min_value)/step)**vector_length

        pbar = tqdm.tqdm(self.grid, total=self.grid_size)
        for x in pbar:
            x = self.__calculate(
                f=function,
                x=np.array(x),
                iters=iters,
            )
            if criterion(function(x)) < self.best_criterion:
                self.best_solution = x
                self.best_criterion = criterion(function(x))
                pbar.set_description(f"Best: {self.best_criterion:.5f}")
                print(f"\n\n {x} \n\n")
                if criterion(function(x)) <= target:
                    return self.best_solution
        return self.best_solution

#    @njit(fast_math=True)
    def __calculate(self, f, x: np.array, iters=100):
        y = f(x)
        jac = np.eye(len(x))
        for iteration in range(iters):
            u = self.calculate_omicron(jac, y)
            x -= u * jac.T @ y
            y = f(x)
            jac = self.calculate_jacobian(f, x)
        return x


    @staticmethod
    def xrange(start: float, stop: float, step: float) -> float:
        if start == stop:
            return start
        start -= step
        while start <= stop:
            start += step
            yield start

    @staticmethod
    def calculate_jacobian(f, x, dx=1e-8):
        n = len(x)
        func = f(x)
        jac = np.zeros((n, n))
        for j in range(n):
            dxj = (abs(x[j]) * dx if x[j] != 0 else dx)
            x_plus = [(xi if k != j else xi + dxj) for k, xi in enumerate(x)]
            jac[:, j] = (f(x_plus) - func) / dxj
        return jac

    @staticmethod
    def calculate_omicron(jacobian, y):
        first_part = np.dot(y, jacobian @ jacobian.T @ y)
        second_part = np.dot(jacobian @ jacobian.T @ y, jacobian @ jacobian.T @ y)
        return first_part / second_part


def MSELoss(x: np.array) -> float:
    return np.sqrt(np.sum(x * x))



def SomeFunc(x: np.array) -> np.array:
    """4 parameters"""
    x1, x2 = x[:2]
    y1, y2 = x[2:]

    res = np.zeros(len(x))
    res[0] = x1 * y2**3
    res[1] = np.sin(x2) - np.cos(y1)*np.e

    return res