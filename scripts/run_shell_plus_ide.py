import sys;

print("Python {} on {}".format(sys.version, sys.platform))
import django;

print("Django {}".format(django.get_version()))
sys.path.extend([WORKING_DIR_AND_PYTHON_PATHS])
if "setup" in dir(django): django.setup()
from django_extensions.management.shells import import_objects
from django.core.management.color import color_style

style = color_style(force_color=True)

globals().update(import_objects({"dont_load": [], "quiet_load": False}, style))

from django_extensions.management.debug_cursor import monkey_patch_cursordebugwrapper

monkey_patch_cursordebugwrapper(print_sql=True).__enter__()  # activate monkey patch inside context manager
import django_manage_shell;

django_manage_shell.run(PROJECT_ROOT)