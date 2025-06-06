import pytest

from src.utilities.utilities import Utilities

def pytest_addoption(parser):
    """Add custom command line options for pytest."""
    parser.addoption("--file_ext", action="store", default="html", help="File extension to search for (default: html)")
    parser.addoption("--target_dir", action="store", default="./out", help="Source directory to search in (default: ./out)")


@pytest.fixture
def file_ext(request):
    """Fixture to provide the list of files from the target directory with given extensions for tests."""
    return request.config.getoption("--file_ext")


@pytest.fixture
def target_dir(request):
    """Fixture to provide the list of files from the target directory with given extensions for tests."""
    return request.config.getoption("--target_dir")


@pytest.fixture
def file_list(request):
    """Fixture to provide the list of files from the target directory with given extensions for tests."""
    given_dir = request.config.getoption("--target_dir")
    given_extension = request.config.getoption("--file_ext")
    return Utilities().get_all_files_in_folder(folder_path=given_dir, file_ext=given_extension, resursive=True)


def pytest_generate_tests(metafunc):
    """Generate tests for different file extensions."""

    # This section is specific to the keyword search functionality
    # ------------------------------------------------------------------
    if "target_dir" in metafunc.fixturenames:
        metafunc.parametrize("target_dir", metafunc.config.getoption("target_dir"))
    if "file_ext" in metafunc.fixturenames:
        metafunc.parametrize("file_ext", ["html"], ids=["HTML"])
    if "file_list" in metafunc.fixturenames:
        given_dir = metafunc.config.getoption("target_dir")
        given_extension = metafunc.config.getoption("file_ext")
        files = Utilities().get_all_files_in_folder(folder_path=given_dir, file_ext=given_extension, resursive=True)
        print(f"\nPrepared file list is: {files}\n")
        metafunc.parametrize("file_list", files)
    # ------------------------------------------------------------------