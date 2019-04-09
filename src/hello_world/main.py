import os

def handler(event, context):
    print(f'ARN: {context.invoked_function_arn}'
          f' Version: {context.function_version}')

    # if os.environ.get('STAGE') == 'prod':
    #     raise ValueError('Nope')

    print('Hello Berlin')

    return True
