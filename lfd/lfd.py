import argparse
import shutil
from pathlib import Path
from typing import Optional

import docker
import docker.errors as docker_err
import tempfile
from docker.models.images import Image

CLIENT = docker.from_env()
IMAGE_TAG = "lfd"
CURRENT_PATH = Path(__file__).parent
SIMILARITY_TAG = b"SIMILARITY:"


def find_similarity_in_logs(logs: bytes) -> float:
    """Get line from the logs where similarity is mentioned.

    :param logs: Unprocessed logs from the docker container after a command was
        run.
    :return: Similarity measure.
    """
    logs = logs.split()
    similarity_line: Optional[bytes] = None
    for index, line in enumerate(logs):
        if line.startswith(SIMILARITY_TAG):
            similarity_line = logs[index + 1]
            break
    return float(similarity_line)


def create_image_if_necessary() -> Image:
    """Check if image calculating distance and build it if it doesn't.

    :return: Built image.
    """
    try:
        return CLIENT.images.get(IMAGE_TAG)
    except docker_err.ImageNotFound:
        print("Docker image not found. Building (it may take a while) ...")
        return CLIENT.images.build(path="./", tag=IMAGE_TAG)[0]


def get_light_field_distance(obj_file1: str, obj_file2: str) -> float:
    """Calculate LFD for two shapes.

    :param obj_file1: Path to either *.ply file or *.obj in PLY format.
    :param obj_file2: Path to second file of the same format.
    :return: LFD value.
    """
    file1 = Path(obj_file1)
    file2 = Path(obj_file2)

    with tempfile.TemporaryDirectory() as volume_folder:
        vol_folder = Path(volume_folder)
        shutil.copy2(file1.as_posix(), vol_folder / file1.name)
        shutil.copy2(file2.as_posix(), vol_folder / file2.name)

        create_image_if_necessary()
        stdout = CLIENT.containers.run(
            image=IMAGE_TAG,
            command="./calculate_distance.sh {} {}".format(
                file1.with_suffix("").name, file2.with_suffix("").name
            ),
            detach=False,
            volumes={
                vol_folder.absolute(): {
                    "bind": "/usr/src/app/volume/",
                    "mode": "rw",
                }
            },
            security_opt=["seccomp=unconfined"],  # necessary for linux
            tty=True,
        )

        (vol_folder / file1.name).unlink()
        (vol_folder / file2.name).unlink()
    return find_similarity_in_logs(stdout)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Script that generates score for two shapes saved in Wavefront "
            "OBJ format"
        )
    )
    parser.add_argument(
        "file1",
        type=str,
        help="Path to the first *.obj file in Wavefront OBJ format",
    )

    parser.add_argument(
        "file2",
        type=str,
        help="Path to the second *obj file in Wavefront OBJ format",
    )

    args = parser.parse_args()

    lfd = get_light_field_distance(args.file1, args.file2)
    print("LFD: {:.4f}".format(lfd))


if __name__ == "__main__":
    main()
