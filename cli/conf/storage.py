from cli.conf.constants import LocalCoreComponentFilepaths
from cli.conf.extract import get_dirnames, get_filename_dir_pairs

from pydantic import BaseModel

from cli.conf.types import FolderFilePair


class ConfigExistStorage:
    """
    A storage container for boolean values for the following config checks:
    1. `zentra/models` folder exists
    2. `zentra/models` setup file exists
    3. `zentra/models` setup file is valid with required elements
    """

    def __init__(self) -> None:
        self.models_folder_exists = False
        self.config_file_exists = False
        self.config_file_valid = False

    def app_configured(self) -> bool:
        """Checks if Zentra has already been configured correctly."""
        return all(
            [
                self.models_folder_exists,
                self.config_file_exists,
                self.config_file_valid,
            ]
        )


class SetupPathStorage(BaseModel):
    """
    A storage container for file and folder paths specific to `zentra init`.

    Parameters:
    - config (str) - the filepath to the zentra models config file
    - models (str) - the directory path to the zentra models folder
    - local (str) - the directory path to the local zentra config folder
    - demo (str) - the directory path to the local zentra config demo folder
    - local_config (str) - the filepath to the local zentra models config file
    """

    config: str
    models: str
    local: str
    demo: str
    local_config: str


class GeneratePathStorage(BaseModel):
    """
    A storage container for file and folder paths specific to `zentra generate`.

    Parameters:
    - config (str) - the filepath to the zentra models config file
    - models (str) - the directory path to the zentra models folder
    - component (str) - the directory path to the local zentra component folder
    - zentra (str) - the directory path to the zentra generate component folder
    """

    config: str
    models: str
    component: str
    generate: str


class CountStorage(BaseModel):
    """A simple storage container for Zentra model counts."""

    generate: int = 0
    remove: int = 0


class ModelFileStorage(BaseModel):
    """A storage container for storing Zentra model (library, filename) pairs."""

    generate: FolderFilePair = []
    remove: FolderFilePair = []
    existing: FolderFilePair = []

    counts: CountStorage = CountStorage()


class BasicNameStorage(BaseModel):
    """A simple storage container for Zentra page and component names."""

    pages: list[str] = []
    components: list[str] = []


class ModelStorage(BaseModel):
    """A storage container for Zentra model filenames."""

    base_files: FolderFilePair = get_filename_dir_pairs(
        parent_dir=LocalCoreComponentFilepaths.ROOT, sub_dir="base"
    )
    folders_to_generate: list[str] = get_dirnames(LocalCoreComponentFilepaths.ROOT)

    base_names: BasicNameStorage = BasicNameStorage()
    pages: ModelFileStorage = ModelFileStorage()
    components: ModelFileStorage = ModelFileStorage()
