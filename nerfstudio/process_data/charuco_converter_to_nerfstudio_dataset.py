# Copyright 2022 The Nerfstudio Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Class to process images or video including a ChArUco board into a nerfstudio dataset."""

from dataclasses import dataclass
from typing import List, Tuple

from rich.console import Console
from typing_extensions import Literal

from nerfstudio.process_data import process_data_utils, charuco_utils
from nerfstudio.process_data.base_converter_to_nerfstudio_dataset import (
    BaseConverterToNerfstudioDataset,
)

CONSOLE = Console(width=120)


@dataclass
class ChArUcoConverterToNerfstudioDataset(BaseConverterToNerfstudioDataset):
    """Class to process images or video including a ChArUco board into a nerfstudio dataset."""

    camera_type: Literal["perspective"] = "perspective"
    """Camera model to use."""
    num_downscales: int = 3
    """Number of times to downscale the images. Downscales by 2 each time. For example a value of 3 will downscale the
       images by 2x, 4x, and 8x."""
    num_frames_target: int = 300
    """Target number of frames to use for the dataset if data is video, results may not be exact."""
    skip_image_processing: bool = False
    """If True, skips copying and downscaling of images and only runs ChArUco board pipeline if possible"""
    crop_factor: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
    """Portion of the image to crop. All values should be in [0,1]. (top, bottom, left, right)"""
    crop_bottom: float = 0.0
    """Portion of the image to crop from the bottom.
       Can be used instead of `crop-factor 0.0 [num] 0.0 0.0` Should be in [0,1].
    """

    def main(self) -> None:
        """Process images or video including a ChArUco board into a nerfstudio dataset."""
        summary_log = []

        # Copy images (and first extract from video if necessary)
        self._generate_images_dir()

        # Downscale images
        if not self.skip_image_processing:
            summary_log += process_data_utils.downscale_images(
                self.image_dir,
                self.num_downscales,
                verbose=self.verbose,
            )

        self._run_charuco_pipeline()
        summary_log += self._save_transforms()

        CONSOLE.log("[bold green]:tada: :tada: :tada: All DONE :tada: :tada: :tada:")

        for summary in summary_log:
            CONSOLE.log(summary)

    def _run_charuco_pipeline(self) -> None:
        raise NotImplementedError

    def _generate_images_dir(self) -> List[str]:
        summary_log = []

        # Video input
        if self.data.is_file():
            log, num_frames = process_data_utils.convert_video_to_images(
                self.data,
                image_dir=self.image_dir,
                num_frames_target=self.num_frames_target,
                crop_factor=self.crop_factor,
                verbose=self.verbose,
            )[0]
            summary_log.append(log)

        # Image input
        elif self.data.is_dir():
            image_rename_map_paths =process_data_utils.copy_images(
                self.data, image_dir=self.image_dir, crop_factor=self.crop_factor, verbose=self.verbose
            )
            num_frames = len(image_rename_map_paths)
        else:
            raise RuntimeError(f"Data path '{self.data}' must be a file or directory.")

        if num_frames == 0:
            raise RuntimeError("No usable images in the data folder.")

        summary_log.append(f"Starting with {num_frames} images")
        return summary_log

    def _save_transforms(self) -> List[str]:
        """Save ChArUco board transforms into the output folder."""
        if not (self.output_dir / "camera.json").exists() or (self.output_dir / "poses.json").exists():
            CONSOLE.log(
                "[bold yellow]Warning: Could not find existing ChArUco results. " "Not generating transforms.json"
            )
            return []

        with CONSOLE.status("[bold yellow]Saving results to transforms.json", spinner="balloon"):
            num_estimated = charuco_utils.charuco_to_json(output_dir=self.output_dir)
        return [f"Estimated pose for {num_estimated} images"]

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.camera_type != "perspective":
            raise RuntimeError(f"camera_type '{self.camera_type}' not supported for ChArUco board.")

        if self.crop_bottom < 0.0 or self.crop_bottom > 1:
            raise RuntimeError("crop_bottom must be set between 0 and 1.")

        if self.crop_bottom > 0.0:
            self.crop_factor = (0.0, self.crop_bottom, 0.0, 0.0)
