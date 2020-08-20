from django.conf import settings


# pylint: disable=unused-argument
def debug(context):
    return {'DEBUG': settings.DEBUG}
