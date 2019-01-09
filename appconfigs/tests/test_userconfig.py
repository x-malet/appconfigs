# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright © Jean-Sébastien Gosselin
# Licensed under the terms of the MIT License
# (https://github.com/jnsebgosselin/appconfigs)
# -----------------------------------------------------------------------------

# ---- Standard imports
import os.path as osp
import filecmp

# ---- Third party imports
import pytest

# ---- Local imports
from appconfigs.user import UserConfig

NAME = 'user_config_tests'
CONF_VERSION = '0.1.0'
DEFAULTS = [
    ('main',
        {'first_option': 'value',
         'second_option': 24.567,
         'third_option': 22,
         'fourth_option': True}
     )
]


# ---- Pytest fixtures
@pytest.fixture
def configdir(tmpdir):
    return osp.join(str(tmpdir), 'UserConfigTests')


# ---- Tests
@pytest.mark.parametrize("backup_value", [True, False])
def test_files_creation(configdir, backup_value):
    """
    Test that the .ini, .bak, and default files are created as expected in the
    specified app config directory.
    """
    conf = UserConfig(NAME, defaults=DEFAULTS, load=True, path=configdir,
                      backup=backup_value, version=CONF_VERSION, raw_mode=True)

    assert conf.get_filename() == osp.join(configdir, NAME + '.ini')
    assert osp.exists(conf.get_filename())
    assert osp.exists(osp.join(conf.path, 'defaults'))
    assert osp.exists(osp.join(conf.path, 'defaults', 'defaults-0.1.0.ini'))
    assert osp.exists(conf.get_filename() + '.bak') is False

    # Init UserConfig a second time to trigger the creation of a backup file.
    conf = UserConfig(NAME, defaults=DEFAULTS, load=True, path=configdir,
                      backup=backup_value, version=CONF_VERSION, raw_mode=True)

    assert osp.exists(conf.get_filename() + '.bak') is backup_value
    if backup_value is True:
        assert filecmp.cmp(conf.get_filename(), conf.get_filename() + '.bak',
                           shallow=False)


if __name__ == "__main__":
    pytest.main(['-x', osp.basename(__file__), '-v', '-rw', '-s'])