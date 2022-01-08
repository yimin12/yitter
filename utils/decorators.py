from rest_framework.response import Response
from rest_framework import status
from functools import wraps

def required_params(request_attr='query_params', params=None):
    """
    when we use @required_params(params=['some_params'], the required_params function should return decorator,
    this decorator is view_func which is encapsulated by @required_params, notes: use mutable params is not
    a good practise
    """
    if params is None:
        params = []

    def decorator(view_func):
        """
        decorator use wraps to parse view_func to _wrapped_view, the instance is the self within view_func
        """
        @wraps(view_func)
        def _wrapped_view(instance, request, *args, **kwargs):
            data = getattr(request, request_attr)
            missing_params = [
                param for param in params if param not in data
            ]
            if missing_params:
                params_str = ','.join(missing_params)
                return Response({
                    'message': u'missing {} in request'.format(params_str),
                    'success': False,
                }, status=status.HTTP_400_BAD_REQUEST)
            # after check by @required_params
            return view_func(instance, request, *args, **kwargs)
        return _wrapped_view
    return decorator
