# ignore deprecation warning for prompt_toolkit
# workaround https://github.com/xonsh/xonsh/issues/4409
# __import__('warnings').simplefilter('ignore', DeprecationWarning, 882)

import warnings

warnings.filterwarnings(
    'ignore',
    message='There is no current event loop',
    category=DeprecationWarning,
    module='prompt_toolkit',
)
