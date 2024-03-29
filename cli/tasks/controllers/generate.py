import os

import typer

from cli.conf.constants import GenerateSuccessCodes
from cli.conf.create import make_directories
from cli.conf.extract import extract_file_pairs_from_list, get_filename_dir_pairs
from cli.conf.format import name_from_camel_case
from cli.conf.move import remove_folder_file_pairs, transfer_folder_file_pairs
from cli.conf.storage import ModelStorage, GeneratePathStorage
from cli.conf.types import FolderFilePair
from cli.tasks.controllers.base import BaseController, status

from zentra.core import Zentra


class GenerateControllerHelper:
    """
    A class for helper functions used across multiple GenerateControllers.

    Parameters:
    - zentra (zentra.core.Zentra) - the Zentra application containing components to generate
    - paths (storage.GeneratePathStorage) - a path storage container with paths specific to the controller
    """

    def __init__(self, zentra: Zentra, paths: GeneratePathStorage):
        self.zentra = zentra
        self.paths = paths
        self.storage = ModelStorage()

        self.storage.base_names.components = zentra.names.components
        self.storage.base_names.pages = zentra.names.pages

    def _get_and_format_models(self, base_names: list[str]) -> list[str]:
        """Retrieves the Zentra model base names and converts them into a suitable format for file processing."""
        return [f"{name_from_camel_case(name)}.tsx" for name in base_names]

    def _make_needed_dirs(self) -> None:
        """Makes the needed directories in the Zentra generate folder."""
        for dir in self.storage.folders_to_generate:
            make_directories(os.path.join(self.paths.generate, dir))

    def _generate_files(self, sub_dir: str) -> None:
        """Create a list of Zentra model files in the generate folder."""
        transfer_folder_file_pairs(
            self.storage.components.generate,
            self.paths.component,
            self.paths.generate,
            src_sub_dir=sub_dir,
        )

    def _remove_files(self) -> None:
        """Removes a list of Zentra models from the generate folder."""
        remove_folder_file_pairs(self.storage.components.remove, self.paths.generate)

    def _check_for_uploadthing(
        self, generate_list: FolderFilePair, filenames: list[str]
    ) -> FolderFilePair:
        """Checks for uploadthings `FileUpload` in a list of Zentra model filenames. If it exists, we extract the required filenames and add them to the `generate_list`. If it doesn't, we return the `generate_list` as is."""
        if "file-upload.tsx" in filenames:
            uploadthing_files = extract_file_pairs_from_list(
                self.storage.base_files, ["uploadthing"], idx=0
            )
            generate_list += uploadthing_files
        else:
            self.storage.folders_to_generate.remove("uploadthing")

        return generate_list

    def _get_existing_models(self) -> FolderFilePair:
        """Retrieves a list of existing models."""
        return get_filename_dir_pairs(parent_dir=self.paths.generate)

    def _get_model_updates(
        self, old: FolderFilePair, new: FolderFilePair
    ) -> FolderFilePair:
        """Extracts the difference between two lists of `FolderFilePair`s to detect Zentra model changes."""
        same = list(set(old) & set(new))
        return list(set(old + new) - set(same))

    def _get_model_changes(
        self,
        model_updates: FolderFilePair,
    ) -> tuple[FolderFilePair, FolderFilePair]:
        """Provides two lists of `FolderFilePair` changes. In the form of: `(to_remove, to_add)`."""
        to_remove, to_add = [], []
        existing_models_set = set(self.storage.components.existing)

        for model in model_updates:
            if model in existing_models_set:
                to_remove.append(model)
                self.storage.components.counts.remove += 1
            else:
                to_add.append(model)
                self.storage.components.counts.generate += 1

        return to_remove, to_add

    def _check_for_new_components(
        self, generate_list: FolderFilePair, existing_models: FolderFilePair
    ) -> None:
        """Checks for new components based on two lists of `FolderFilePairs`. Raises a success msg if there are none."""
        if generate_list == existing_models:
            raise typer.Exit(code=GenerateSuccessCodes.NO_NEW_COMPONENTS)

    def _filter_ut(self, components: FolderFilePair) -> FolderFilePair:
        """A helper function for calculating the correct number of components, factoring in that `uploadthing` has multiple files."""
        filtered = []
        ut_found = False

        for model in components:
            if model[0] == "uploadthing":
                if not ut_found:
                    filtered.append(model)
                    ut_found = True
            else:
                filtered.append(model)
        return filtered

    def _store_components(self, model_updates: FolderFilePair) -> None:
        """Stores the `component` attributes into `self.storage`."""
        self.storage.components.remove, self.storage.components.generate = (
            self._get_model_changes(model_updates)
        )

        self.storage.components.counts.generate = len(
            self._filter_ut(self.storage.components.generate)
        )
        self.storage.components.counts.remove = len(
            self._filter_ut(self.storage.components.remove)
        )


class GenerateController(BaseController, GenerateControllerHelper):
    """
    A controller for handling tasks that generate the Zentra components.

    Parameters:
    - zentra (zentra.core.Zentra) - the Zentra application containing components to generate
    - paths (storage.GeneratePathStorage) - a path storage container with paths specific to the controller
    """

    def __init__(self, zentra: Zentra, paths: GeneratePathStorage) -> None:
        react_str = "[cyan]React[/cyan]"
        zentra_str = "[magenta]Zentra[/magenta]"

        tasks = [
            (self.extract_models, f"Extracting {zentra_str} models"),
            (self.update_files, f"Handling {react_str} component files"),
            (self.update_template_files, f"Configuring {react_str} components"),
        ]

        GenerateControllerHelper.__init__(self, zentra, paths)
        BaseController.__init__(self, tasks)

    @status
    def extract_models(self) -> None:
        """Extracts the Zentra models and prepares them for file generation."""
        formatted_names = self._get_and_format_models(
            self.storage.base_names.components
        )

        generate_list = extract_file_pairs_from_list(
            self.storage.base_files, formatted_names
        )
        generate_list = self._check_for_uploadthing(generate_list, formatted_names)
        existing_models = self._get_existing_models()

        self._check_for_new_components(generate_list, existing_models)

        self.storage.components.existing = existing_models
        model_updates = self._get_model_updates(existing_models, generate_list)
        self._store_components(model_updates)

    @status
    def update_files(self) -> None:
        """Creates or removes the React components based on the extracted models."""
        if self.storage.components.counts.generate != 0:
            self._make_needed_dirs()
            self._generate_files(sub_dir="base")

        if self.storage.components.counts.remove != 0:
            self._remove_files()

    @status
    def update_template_files(self) -> None:
        """Updates the React components based on the Zentra model attributes."""
        pass
        # Steps 6 to 8
