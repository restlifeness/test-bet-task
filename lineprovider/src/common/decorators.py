
from typing import Callable, Any
from functools import wraps
from inspect import iscoroutinefunction

from .utils import is_pytest_running


def return_side_effect(
    effect: Callable[..., Any],
    attr: str | None = None,
    skip_on_tests: bool = False,
) -> Callable[..., Any]:
    """
    A decorator that adds a side effect to the return value of an asynchronous class or object method.

    This decorator can be used to execute a given side effect function on the return value
    of another function. The side effect can either act on the entire result or on a specific
    attribute of the result if specified.

    :param effect: The side effect function to be executed. This function should accept
                   one argument, which will be the return value of the decorated function
                   or an attribute of it.
    :param attr: The name of the attribute of the result object on which to apply the side effect.
                 If set to None, the side effect is applied directly to the entire result object.
                 For example, if the result has an attribute `data` and attr is set to `"data"`,
                 the effect will be applied to `result.data`.
    :param skip_on_tests: A flag to indicate whether to skip the side effect when running in a
                          testing environment. If set to True, the side effect will not be applied
                          when the function is executed in tests.
    :return: The decorated function, which will execute the side effect on the return value
             or its specified attribute.
    """
    def decorator(method: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(method)
        async def wrapper(obj, *args: Any, **kwargs: Any) -> Any:
            result = await method(obj, *args, **kwargs)

            if attr and not hasattr(result, attr):
                raise AttributeError(
                    f"AttributeError: The attribute '{attr}' does not exist in the object of type "
                    f"'{type(obj).__name__}' passed to the method '{method.__name__}' decorated by "
                    f"'return_side_effect'. Please ensure that the object has the specified attribute "
                    f"or check if the attribute name is correct."
                )

            return_value = result if not attr else getattr(result, attr)

            if skip_on_tests and is_pytest_running():
                return result

            if iscoroutinefunction(effect):
                await effect(return_value)
                return result

            effect(result if not attr else getattr(result, attr))
            return result
        return wrapper
    return decorator
