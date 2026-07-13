from pydantic import validate_call

TRANSFORMS = {}

def register_transform(name):
    def wrapper(func: Transform):
        TRANSFORMS[name] = func
        return func
    return wrapper

class Transform:
    def __repr__(self):
        return f"{self.__class__.__name__}()"

@register_transform("gaussian_smoothing_1d")
class GaussianSmoothing1d(Transform):
    @validate_call
    def __init__(self, sigma: float):
        self.sigma = sigma
        self.params = [sigma]

    def __call__(self, X):
        # do something with sigma
        print(self.sigma)
        return X

@register_transform("normalize")
class Normalize(Transform):
    @validate_call
    def __init__(self, k: float):
        self.k = k

    def __call__(self, X):
        # do something with k
        return X / self.k

@register_transform("double")
class Double(Transform):
    @validate_call
    def __init__(self):
        pass

    def __call__(self, X):
        # do something with k
        return 2 * X