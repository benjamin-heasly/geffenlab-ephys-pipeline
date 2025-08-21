import sys
from argparse import ArgumentParser
from typing import Optional, Sequence
import logging
from pathlib import Path
from datetime import datetime, date
from getpass import getpass


from fabric import Connection


def set_up_logging():
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def run_main(
    local_path: Path,
    remote_host: str,
    analysis_path: Path,
    analysis_subdirs: list[str],
    subject_id: str,
    session_date: date,
    username: str,
    password: str
):
    # Use consistent date formatting like MMDDYYYY.
    date_string = session_date.strftime("%m%d%Y")

    logging.info(f"Connecting to remote host: {remote_host}.")
    with Connection(host=remote_host, user=username, connect_kwargs={"password": password}) as c:
        try:
            # Call to open() will log connection attempts, results.
            c.open()

            # List subdirectories in the session analysis directory.
            remote_session_path = Path(analysis_path, subject_id, date_string)
            logging.info(f"Checking for remote analysis session directory {remote_session_path}:")
            c.run(f"ls {remote_session_path.as_posix()}")

            # Download selected subdirectories.
            for analysis_subdir in analysis_subdirs:
                logging.info(f"Checking for analysis session subdir {analysis_subdir}:")
                remote_subdir = Path(remote_session_path, analysis_subdir)
                try:
                    # Recursively find regular files within this subdirectory, if any.
                    result = c.run(f"find {remote_subdir.as_posix()} -type f")
                except Exception:
                    logging.warning(f"Not downloading from subdir: {analysis_subdir}")
                    continue

                # Download each file, preserving session subdirectory structure.
                remote_files = result.stdout.strip().split('\n')
                for remote_file in remote_files:
                    relative_file_path = Path(remote_file).relative_to(remote_session_path)
                    local_file_path = Path(local_path, subject_id, date_string, relative_file_path)
                    logging.info(f"Downloading to: {local_file_path}")
                    c.get(remote=remote_file, local=local_file_path.as_posix())

        except Exception as e:
            logging.warning(f"Download error: {e.args}")

    logging.info("OK.\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    set_up_logging()

    parser = ArgumentParser(description="Download pipeline results from eg cortex to the local machine.")

    parser.add_argument(
        "--local-root", "-l",
        type=str,
        help="Local root directory to receive donwloads. (default: %(default)s)",
        default="/mnt/c/Users/labuser/Desktop/ephys-pipeline-outputs/"
    )
    parser.add_argument(
        "--remote-host", "-r",
        type=str,
        help="Remote host (eg cortex) to connect to. (default: %(default)s)",
        default="128.91.19.199"
    )
    parser.add_argument(
        "--username", "-u",
        type=str,
        help="Remote (eg cortex) username. (default: prompt for input)",
        default=None
    )
    parser.add_argument(
        "--analysis-root", "-a",
        type=str,
        help="Remote root directory containing lab analysis results. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/analysis/"
    )
    parser.add_argument(
        "--subject-id", "-s",
        type=str,
        help="Subject id for a session that was processed. (default: prompt for input)",
        default=None
    )
    parser.add_argument(
        "--session-date", "-d",
        type=str,
        help="Date of a session that was processed: MMDDYYYY. (default: prompt for input)",
        default=None
    )
    parser.add_argument(
        "--analysis-subdirs", "-S",
        type=str,
        nargs="+",
        help="Subdirectories to download from within the remote ANALYSIS_ROOT/SUBJECT_ID/SESSION_DATE/. (default: %(default)s)",
        default=["synthesis", "nextflow", "sorted/nextflow", "sorted/visualization"]
    )

    cli_args = parser.parse_args(argv)

    # Prompt for missing input args as needed.
    local_path = Path(cli_args.local_root)
    logging.info(f"Downloading files to local root: {local_path}")

    remote_host = cli_args.remote_host
    logging.info(f"Downloading files from remote host: {remote_host}")

    analysis_path = Path(cli_args.analysis_root)
    logging.info(f"Downloading files from remote analysis root: {analysis_path}")

    analysis_subdirs = cli_args.analysis_subdirs
    logging.info(f"Downloading analysis session subdirs: {analysis_subdirs}")

    subject_id = cli_args.subject_id
    if subject_id is None:
        subject_id = input("Subject ID: ").strip()
    logging.info(f"Downloading files for subject id: {subject_id}")

    session_dates_string = cli_args.session_date
    if session_dates_string is None:
        session_dates_string = input("Session date MMDDYYYY: ").strip()

    session_date = datetime.strptime(session_dates_string, "%m%d%Y").date()
    logging.info(f"Downloading files for session date: {session_dates_string} ({session_date})")

    username = cli_args.username
    if username is None:
        username = input("Remote username: ").strip()
    logging.info(f"Downloading files as remote user: {username}")

    # Password will not be printed.
    password = getpass(f"Password for remote user {username}: ")

    try:
        run_main(
            local_path,
            remote_host,
            analysis_path,
            analysis_subdirs,
            subject_id,
            session_date,
            username,
            password
        )
    except:
        logging.error("Error downloading files.", exc_info=True)
        return -1


if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
