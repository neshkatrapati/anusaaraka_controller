from nltk.featstruct import FeatStruct

dispatchRules = {}

class UnificationError(Exception):
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2

    def __str__(self):
        return "Unification Failed Between " + self.f1.__str__() + " and " + self.f2.__str__()

class UnificationInhertianceError(UnificationError):
    def __str__(self):
        return "Unification Inheritance Failed Between " + self.f1.__str__() + " and " + self.f2.__str__()


def dispatch(fs):
    """
    A decorator which takes a feature structure and calls a function based on whether the feature structure is unified with the new feature structure
    """
    def _dispatch(func):
        fsn = FeatStruct(fs)
        def _func (new_fs):
            """
            This is the actual validator function
            """

            new_fs= FeatStruct(new_fs)
            if fsn.unify(new_fs): # If the current fs (new_fs) unifies with the rule (fs)
                return func(new_fs)
            else:
                raise UnificationError(fsn, new_fs)
        dispatchRules[func.__name__] = _func # Add into a global dictionary. Makes it easy to 'mass-call' functions
        _func.fs = fsn
        return _func
    return _dispatch

def dispatch_or(*fs_mult):
    """
    A decorator which takes a feature structure and calls a function based on whether the feature structure is unified with the new feature structure
    """
    def _dispatch(func):
        fsns = [FeatStruct(fs) for fs in fs_mult]
        def _func (new_fs):
            """
            This is the actual validator function
            """

            new_fs= FeatStruct(new_fs)
            truth = False
            for fsn in fsns:
                if fsn.unify(new_fs): # If the current fs (new_fs) unifies with the rule (fs)
                    return func(new_fs)
            raise UnificationError(fsns[-1], new_fs)
        dispatchRules[func.__name__] = _func # Add into a global dictionary. Makes it easy to 'mass-call' functions
        _func.fs = fsns
        return _func
    return _dispatch





def inherit(func, fs='[]'):
    """
    A Decorator which takes a rule, unifies its feature structure with the newly specified feature structure (fs) and then calls dispatch.
    """
    fs = FeatStruct(fs)
    result_fs = func.fs.unify(fs)
    if result_fs:
        return dispatch(result_fs)
    else:
        raise UnificationInhertianceError(func.fs, fs)
