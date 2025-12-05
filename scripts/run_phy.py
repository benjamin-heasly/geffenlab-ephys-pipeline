import sys
from os import getuid, getgid, environ
from argparse import ArgumentParser, BooleanOptionalAction
from typing import Optional, Sequence
import logging
from datetime import datetime, timezone
from pathlib import Path
import subprocess


def set_up_logging(
    log_path: Path = None
):
    """Set up to copy logs to stdout (the console) and to a log file."""
    logging.root.handlers = []
    handlers = [
        logging.StreamHandler(sys.stdout)
    ]
    if log_path and log_path.parent.exists():
        handlers.append(logging.FileHandler(log_path))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )
    logging.info(f"Writing logs for this script to stdout and {log_path}")


def run_phy_in_docker(
    docker_image: str,
    docker_run_args: list[str],
    gpu_device: str,
    x11: bool,
    user: str,
    params_py: Path
) -> int:
    logging.info("Starting Phy run.\n")

    phy_dir = params_py.parent.absolute().as_posix()

    if gpu_device and gpu_device != 'none':
        gpus = ["--gpus", f"'device=${gpu_device}'"]
    else:
        gpus = []

    if x11:
        x11_args = ["--volume", "/tmp/.X11-unix:/tmp/.X11-unix", "--env", "DISPLAY"]
        if "XAUTHORITY" in environ:
            x_authority_host = Path(environ["XAUTHORITY"]).absolute().as_posix()
            x_authority_container = "/var/.Xauthority"
            x11_args += ["--volume", f"{x_authority_host}:{x_authority_container}", "--env", f"XAUTHORITY={x_authority_container}"]
    else:
        x11_args = []
    
    if not user:
        user_args = []
    elif user == 'self':
        user_args = ["--user", f"{getuid()}:{getgid()}"]
    else:
        user_args = ["--user", user]

    step_args = [
        "--data-root", phy_dir,
        "--params-py-pattern", params_py.name,
    ]
    docker_run_command = [
        "docker",
        "run",
    ] + docker_run_args + gpus + x11_args + user_args + [
        "--volume", f"{phy_dir}:{phy_dir}",
        "--workdir", phy_dir,
        docker_image,
        "conda_run", "python", "/opt/code/run_phy.py"
    ] + step_args

    logging.info(f"Running Phy with Docker command: {docker_run_command}.")

    process = subprocess.Popen(
        docker_run_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Tail the container output as it comes.
    for line in process.stdout:
        logging.info(line.strip())

    exit_code = process.wait()
    if exit_code == 0:
        logging.info(f"OK\n")
    else:
        logging.error(f"Completed with error, exit code {exit_code}")

    return exit_code


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser(description="Run Phy in a Docker container for maual sorting curation.")

    parser.add_argument(
        "--docker-image", "-I",
        type=str,
        help="Which Docker image to use for running Phy. (default: %(default)s)",
        default="ghcr.io/benjamin-heasly/geffenlab-phy-desktop:v0.0.4"
    )
    parser.add_argument(
        "--docker-run-args", "-D",
        type=str,
        nargs="*",
        help="Args to pass to 'docker run ...'. (default: %(default)s)",
        default=["--rm"]
    )
    parser.add_argument(
        "--gpu-device", "-G",
        type=str,
        help="Which gpu device to use with Docker: integer device index, string device GUID, or 'none' (default: %(default)s)",
        default=0
    )
    parser.add_argument("--x11",
        action=BooleanOptionalAction,
        help="Whether or not to configure an X11 display for the Docker container. (default: %(default)s)",
        default=True
    )
    parser.add_argument("--user",
        type=str,
        help="Specify a user:group to run as in the container, or 'self' to use the caller's uid:gid, omit to use the system or image default. (default: %(default)s)",
        default=None
    )
    parser.add_argument(
        "--analysis-root",
        type=str,
        help="Root folder with the lab's take-home analysis products. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/analysis"
    )
    parser.add_argument(
        "--experimenter",
        type=str,
        help="Experimenter initials for the session to be processed. (default: %(default)s)",
        default="BH"
    )
    parser.add_argument(
        "--subject",
        type=str,
        help="Subject of the session to be processed. (default: %(default)s)",
        default="AS20-minimal3"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date of the session to be processed DDMMYYYY. (default: %(default)s)",
        default="03112025"
    )
    parser.add_argument(
        "--params-py-pattern", "-p",
        type=str,
        help="Glob pattern to locate Phy params.py file(s) within ANALYSYS_ROOT/EXPERIMENTER/SUBJECT/DATE/ (default: %(default)s)",
        default="**/params.py"
    )

    cli_args = parser.parse_args()

    # Write logs to the sessions processed output subdirectory.
    data_path = Path(cli_args.analysis_root, cli_args.experimenter, cli_args.subject, cli_args.date)
    execution_time = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%Z')
    script_log_path = Path(data_path, f"run_phy_{execution_time}.log")
    set_up_logging(script_log_path)

    logging.info(f"Using Docker image: {cli_args.docker_image}")
    logging.info(f"Using 'docker run' args: {cli_args.docker_run_args}")
    logging.info(f"Using GPU device: {cli_args.gpu_device}")
    logging.info(f"Configuring X11 display: {cli_args.x11}")
    logging.info(f"Running container as user and group: {cli_args.user}")
    logging.info(f"Looking for phy/ data in: {data_path}")
    logging.info(f"Looking for params.py files(s) matchign pattern: {cli_args.params_py_pattern}")

    try:
        params_py_matches = list(data_path.glob(cli_args.params_py_pattern))
        match_count = len(params_py_matches)
        params_py_matches.sort()
        logging.info(f"Found {match_count} params.py matches within {data_path}")
        if match_count < 1:
            raise ValueError(f"Found no params.py matching pattern {cli_args.params_py_pattern} within {data_path}")
        elif match_count == 1:
            params_py_path = params_py_matches[0]
        else:
            logging.info(f"Please choose one:")
            for index, params_py_match in enumerate(params_py_matches):
                logging.info(f"  {index}: {params_py_match.relative_to(data_path)}")
            params_py_index = int(input(f"Choose by number 0-{match_count - 1}: ").strip())
            params_py_path = params_py_matches[params_py_index]
        logging.info(f"Using params.py: {params_py_path}")

        main_exit_code = run_phy_in_docker(
            cli_args.docker_image,
            cli_args.docker_run_args,
            cli_args.gpu_device,
            cli_args.x11,
            cli_args.user,
            params_py_path
        )

    except:
        logging.error("Error running Phy.", exc_info=True)
        return -1

    return main_exit_code


if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
