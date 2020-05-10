import argparse
import functools
import inspect
import json
import sys
import os

# Mutable base class
class Mutable(object):

    # Initialization
    def __init__(self, value={}, root=True, name=None,
        args=False, auto=False, *vargs, **kwargs):

        # Convert all props to Mutable props
        self.__set__(self.__dict__)

        # Collect internal props
        self.__dot__ = chr(46)
        self.__type__ = type(value)
        self.__root__ = root

        # Set value
        self.__set__(self._load(value, auto))

        # Check for argument help in base class
        if hasattr(self.__class__, "help"):
            self.__help__ = self.__class__.help

        # Parse args and name
        if args: self._args()
        if name: self.__class__.__name__ = name

    # Custom get
    def __get__(self, inst=None, owner=None):

        # Return value
        if hasattr(self, "__value__"):
            return self.__value__

        # Return list
        if self.__type__ == list:
            return [self.__getattribute__(x) for x in self._fields()]

        return self

    # Custom getattribute
    def __getattribute__(self, key):
        v = object.__getattribute__(self, key)
        if hasattr(v, "__value__"):
            v = object.__getattribute__(v, "__value__")
        return v

    # Custom getitem
    def __getitem__(self, key):
        k = str(key).split(self.__dot__)

        # Handle lists
        if self.__type__ == list:
            try: v = self.__get__()[key]
            except: v = self.__get__()[int(k[0])]

        # Handle dicts
        elif hasattr(self, k[0]):
            v = getattr(self, k[0])

        # Others
        else:
            return None

        # Recurse key from mutable value or return
        if isinstance(v, Mutable):
            if len(k) > 1:
                return v[self.__dot__.join(k[1:])]
            else:
                return v.__get__()
        return v

    # Custom set
    def __set__(self, value):
        if hasattr(self, "__value__"):
            del self.__value__
        if isinstance(value, dict):
            for k, v in value.items():
                self.__dict__[str(k)] = Mutable(v, root=False)
        elif isinstance(value, list):
            for i in range(len(value)):
                self.__dict__[str(i)] = Mutable(value[i], root=False)
        else:
            self.__value__ = value

    # Custom setattr
    def __setattr__(self, key, value):
        if "__" in key:
            self.__dict__[key] = value
        else:
            self[key] = value

    # Custom setitem
    def __setitem__(self, key, value):

        # Not initialized
        if not hasattr(self, "__dot__"):
            self.__dict__[key] = value
            return value

        # Initialized
        k = str(key).split(self.__dot__)
        if hasattr(self, k[0]):
            v = object.__getattribute__(self, k[0])
            if isinstance(v, Mutable):
                if len(k) > 1:
                    v[self.__dot__.join(k[1:])] = value
                else:
                    v.__set__(value)
            else:
                self.__dict__[key] = value
        else:
            self.__dict__[key] = value

    # Returns iterable from self
    def __iter__(self):
        for k in self._fields():

            # Yield values for list
            if self.__type__ == list:
                yield self[k]

            # Otherwise yield keys and values, unless function
            elif type(self[k]) is not type(lambda _: _):
                yield k, self[k]

    # Base descriptor
    def __int__(self):
        return int(self.__get__())

    # Base descriptor
    def __float__(self):
        return float(self.__get__())

    # Base descriptor
    def __str__(self):
        if hasattr(self, "__value__"):
            return str(self.__value__)
        try:
            return json.dumps(dict(self), default=lambda x: dict(x))
        except:
            return json.dumps(self.__get__(), default=lambda x: dict(x))

    # Base descriptor
    def __repr__(self):
        if hasattr(self, "__value__"):
            return repr(self.__value__)
        try:
            return json.dumps(dict(self), default=lambda x: dict(x), indent=2, sort_keys=True)
        except:
            return json.dumps(self.__get__(), default=lambda x: dict(x), indent=2, sort_keys=True)

    # Base descriptor
    def __add__(self, value):
        if hasattr(self, "__value__"):
            return self.__value__ + value
        raise TypeError("Unsupported operand type(s) for +: '{0}' and '{1}'".format("Mutable", type(value)))

    # Base descriptor
    def __sub__(self, value):
        if hasattr(self, "__value__"):
            return self.__value__ - value
        raise TypeError("Unsupported operand type(s) for -: '{0}' and '{1}'".format("Mutable", type(value)))

    # Base descriptor
    def __mul__(self, value):
        if hasattr(self, "__value__"):
            return self.__value__ * value
        raise TypeError("Unsupported operand type(s) for *: '{0}' and '{1}'".format("Mutable", type(value)))

    # Base descriptor
    def __div__(self, value):
        if hasattr(self, "__value__"):
            return self.__value__ / value
        raise TypeError("Unsupported operand type(s) for /: '{0}' and '{1}'".format("Mutable", type(value)))

    # Base descriptor
    def __contains__(self, key):
        return hasattr(self, key)

    # Base descriptor
    def __len__(self):
        return len(self._fields())

    # Parses command line arguments
    def _args(self):
        parser = argparse.ArgumentParser(description=self.__class__.__name__)
        if __name__ != '__main__':
            parser.usage = argparse.SUPPRESS
        for p in self._props():
            v = self[p]

            # Argument help
            desc = ''
            if hasattr(self, "__help__") and p in self.__help__.keys():
                desc = self.__help__[p]

            # Boolean True enables automatic type description
            if desc == True:
                desc = "<{0}".format(str(type(v)).replace("'", "").split(" ")[-1])

            # Boolean false skips argument
            if desc != False:
                parser.add_argument('--{0}'.format(p),
                    type=type(v),
                    default=v,
                    help=str(desc),
                    metavar=''
                )

        # Parse arguments and collect values
        try:
            args, uknown = parser.parse_known_args()
            for k, v in args.__dict__.items():
                self[k] = v
        except:
            # TODO: A little hacky. Relies on the fact that top module has
            # smaller stack than others
            if inspect.getmodule(inspect.stack()[-3][0]).__name__ != '__main__':
                sys.exit(0)

    # Loads base value
    def _load(self, value, auto=False):
        if auto:
            value = self.__class__.__name__ + ".json"
        if self.__root__ and self.__type__ == str:
            if value.endswith('.json'):
                if os.path.exists(value):
                    with open(value, 'r') as jsonfile:
                        value = jsonfile.read()
                else:
                    raise ValueError("could not locate json file '{0}'".format(value))
            try:
                value = json.loads(value)
            except:
                pass
        return value

    # Expose func
    def load(self, value, auto=False):
        return self._load(value, auto)

    # Returns sorted fields
    def _fields(self):
        return sorted(filter(lambda x: "__" not in x, [x for x, y in self.__dict__.items()]))

    # Expose func
    def fields(self):
        return self._fields()

    # Returns props generator
    def _props(self, prev=None):
        for k, v in self.__dict__.items():
            if "__" not in k:
                if isinstance(v, Mutable):
                    if hasattr(v, "__value__"):
                        yield k if prev == None else prev + self.__dot__ + k
                    else:
                        for p in v._props(prev=k):
                            yield p if prev == None else prev + self.__dot__ + p

    # Expose func
    def props(self, prev=None):
        return self._props()

    # Saves self as json file
    def _save(self, path=".", pretty=True):
        if path == ".":
            path = self.__class__.__name__
        with open(path, 'w') as jsonfile:
            jsonfile.write(repr(self) if pretty else str(self))

    # Expose func
    def save(self, path=".", pretty=True):
        return self._save(path, pretty)

# Class decorator
def mutable(cls):
    class ClassWrapper(Mutable, cls):
        def __init__(self, *args, **kwargs):
            # Check class __init__ method to find what arguments are accepted
            vargs, kwvars, var, defaults = inspect.getargspec(cls.__init__.__func__)

            # Only pass known kwargs to base class
            _kwargs = {}
            for k, v in kwargs.items():
                if k in vargs:
                    _kwargs[k] = v

            # If positional arguments are accepted ['self', '...'] then pass args
            if len(vargs) > 1:
                if len(args) > 1:
                    # First argument is always mutable value
                    cls.__init__(self, *(args[1:]), **_kwargs)
                else:
                    # Only pass keyword arguments
                    cls.__init__(self, **_kwargs)
            # Otherwise don't pass args
            else:
                cls.__init__(self)

            # Check if name should be overridden
            if 'name' not in kwargs.keys():
                self.__class__.__name__ = str(cls).split(".")[-1]

            # Check if class has help legend
            try:
                self.__help__ = cls.help
            except:
                pass

            # Ensure value arg
            if len(args) == 0: args = ({}, )

            # Collect functions that collide with mutable methods
            funcs = filter(

                # Matchin names in class
                lambda a: "_" not in a[0] and a[0] in \

                # Function names in mutable
                map(lambda b: b[0], [y for y in inspect.getmembers(Mutable, predicate=inspect.ismethod)]),

                # Function names in class
                [x for x in inspect.getmembers(cls, predicate=inspect.ismethod)]
            )

            # Since mutable accepts *args, **kwargs we can safely pass all kwargs.
            # and we only pass args that were not consumed by base class
            Mutable.__init__(self, *((args[0],) + args[len(vargs):]) , **kwargs)

            # Swap colliding functions and automatically convert to bound methods
            for item in funcs:
                setattr(self, item[0], functools.partial(item[1], self))

    return ClassWrapper

if __name__ == '__main__':
    print Mutable()
