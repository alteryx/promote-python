from functools import wraps
from schema import Schema, And

def validate_json(aSchema):
    if not isinstance(aSchema, Schema):
        raise Exception("validate_json can only accept a Schema class")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = args[0]
            aSchema.validate(data)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def main():
    @validate_json(Schema([{'name': And(str, len)}]))
    def foo(data):
        print('hi')


    @validate_json(Schema({'name': And(str, len)}))
    def ok(data):
        print('hi')


    ok({"name": "Greg"})
    foo({"name": "Greg"})


if __name__ == '__main__':
    main()
