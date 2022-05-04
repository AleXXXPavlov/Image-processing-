from setuptools import setup

setup(
    name='text_line_drawer',
    entry_points={
        'console_scripts': [
            'text_line_drawer = textline:run',
        ],
    }
)
