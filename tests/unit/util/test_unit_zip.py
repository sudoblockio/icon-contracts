import shutil

import pytest

from icon_contracts.utils.zip import unzip_safe


def test_zip_bomb_safe(chdir_fixtures, caplog):

    with pytest.raises(MemoryError):
        unzip_safe("10gb_zipbomb.zip", output_dir="out")

    shutil.rmtree("out")
    assert "Contract hash upload is too large" in caplog.text
