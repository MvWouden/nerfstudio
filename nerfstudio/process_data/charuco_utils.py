from pathlib import Path


def charuco_to_json(output_dir: Path) -> int:
    """Converts COLMAP's camera.json and poses.json to a transforms JSON file.

    Args:
        output_dir: Path to the output directory.

    Returns:
        The number of registered images.
    """
    raise NotImplementedError


def run_charuco_pipeline(
    image_dir: Path,
    charuco_dir: Path,
    camera_model: CameraModel,
    verbose: bool = False,
) -> None:
    """Run the ChArUco camera/pose estimation pipeline on the images.

    Args:
        image_dir: Path to the directory containing the images.
        charuco_dir: Path to the output directory.
        camera_model: Camera model to use.
        verbose: If True, logs the output of the command.
    """
    raise NotImplementedError
