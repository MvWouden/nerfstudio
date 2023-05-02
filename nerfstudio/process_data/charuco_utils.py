from pathlib import Path


def charuco_to_json(output_dir: Path) -> int:
    """Converts COLMAP's camera.json and poses.json to a transforms JSON file.

    Args:
        output_dir: Path to the output directory.

    Returns:
        The number of registered images.
    """
    raise NotImplementedError
