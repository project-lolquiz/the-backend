import os

os.environ['ENV'] = 'qa'

import main
import threading


def before_all(context):
    context.world = threading.local()
    context.world.client = main.app.test_client()
