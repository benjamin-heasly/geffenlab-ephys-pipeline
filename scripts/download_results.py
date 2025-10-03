import sys
from argparse import ArgumentParser
from typing import Optional, Sequence
import logging
from pathlib import Path
from datetime import datetime, date
from getpass import getpass
import fnmatch


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
    processed_data_path: Path,
    analysis_path: Path,
    log_patterns: list[str],
    processed_subdirs: list[str],
    experimenter: str,
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

            # List files and subdirectories in the session analysis directory.
            remote_analysis_path = Path(analysis_path, experimenter, subject_id, date_string)
            logging.info(f"Checking for remote analysis session directory {remote_analysis_path}:")
            analysis_result = c.run(f"ls {remote_analysis_path.as_posix()}")

            # Download all the "analysis" files.
            try:
                # Recursively find regular files within the analysis subdirectory.
                analysis_result = c.run(f"find {remote_analysis_path.as_posix()} -type f")

                # Download each file, preserving session subdirectory structure.
                analysis_files = analysis_result.stdout.strip().split('\n')
                for analysis_file in analysis_files:
                    relative_file_path = Path(analysis_file).relative_to(remote_analysis_path)
                    local_file_path = Path(local_path, experimenter, subject_id, date_string, relative_file_path)
                    logging.info(f"Downloading to: {local_file_path}")
                    c.get(remote=analysis_file, local=local_file_path.as_posix())

            except Exception:
                logging.warning(f"Error downloading from analysis session directory.")

            # List files and subdirectories in the session processed data directory.
            remote_processed_data_path = Path(processed_data_path, experimenter, subject_id, date_string)
            logging.info(f"Checking for remote processed data session directory {remote_processed_data_path}:")
            processed_result = c.run(f"ls {remote_processed_data_path.as_posix()}")

            # Download log files from the session processed data subdirectory.
            processed_list = processed_result.stdout.strip().split('\n')
            processed_logs = []
            for log_pattern in log_patterns:
                processed_logs += fnmatch.filter(processed_list, log_pattern)
            print(f"Found session processing logs: {processed_logs}")
            for processed_log in processed_logs:
                remote_log_path = Path(remote_processed_data_path, processed_log)
                local_log_path = Path(local_path, experimenter, subject_id, date_string, processed_log)
                logging.info(f"Downloading to: {local_log_path}")
                c.get(remote=remote_log_path, local=local_log_path.as_posix())

            # Download selected processing subdirectories.
            for processed_subdir in processed_subdirs:
                logging.info(f"Checking for processed data subdir {processed_subdir}:")
                remote_subdir = Path(remote_processed_data_path, processed_subdir)
                try:
                    # Recursively find regular files within this subdirectory, if any.
                    subdir_result = c.run(f"find {remote_subdir.as_posix()} -type f")
                except Exception:
                    logging.warning(f"Not downloading from subdir: {processed_subdir}")
                    continue

                # Download each file, preserving session subdirectory structure.
                remote_files = subdir_result.stdout.strip().split('\n')
                for remote_file in remote_files:
                    relative_file_path = Path(remote_file).relative_to(remote_processed_data_path)
                    local_file_path = Path(local_path, experimenter, subject_id, date_string, relative_file_path)
                    logging.info(f"Downloading to: {local_file_path}")
                    c.get(remote=remote_file, local=local_file_path.as_posix())

        except Exception as e:
            logging.warning(f"Download error: {e.args}")

    logging.info("OK.\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    set_up_logging()

    parser = ArgumentParser(description="Download pipeline results from eg cortex to the local machine.")

    parser.add_argument(
        "--local-root", "-L",
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
        "--user", "-u",
        type=str,
        help="Remote (eg cortex) username. (default: prompt for input)",
        default=None
    )
    parser.add_argument(
        "--processed-data-root", "-P",
        type=str,
        help="Remote root directory containing lab analysis results. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/processed_data/"
    )
    parser.add_argument(
        "--analysis-root", "-A",
        type=str,
        help="Remote root directory containing lab analysis results. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/analysis/"
    )
    parser.add_argument(
        "--experimenter", "-e",
        type=str,
        help="Experimenter initials for a session that was processed. (default: prompt for input)",
        default=None
    )
    parser.add_argument(
        "--subject", "-s",
        type=str,
        help="Subject id for a session that was processed. (default: prompt for input)",
        default=None
    )
    parser.add_argument(
        "--date", "-d",
        type=str,
        help="Date of a session that was processed: MMDDYYYY. (default: prompt for input)",
        default=None
    )
    parser.add_argument(
        "--log-patterns", "-l",
        type=str,
        nargs="+",
        help="File name patterns to match logs within the remote PROCESSED_DATA_ROOT/EXPERIMENTER/SUBJECT_ID/SESSION_DATE/. (default: %(default)s)",
        default=["*.log", "*.md"]
    )
    parser.add_argument(
        "--processed-subdirs", "-S",
        type=str,
        nargs="+",
        help="Subdirectories to download from within the remote PROCESSED_DATA_ROOT/EXPERIMENTER/SUBJECT_ID/SESSION_DATE/. (default: %(default)s)",
        default=["nextflow", "sorted/nextflow", "sorted/visualization"]
    )

    cli_args = parser.parse_args(argv)

    # Prompt for missing input args as needed.
    local_path = Path(cli_args.local_root)
    logging.info(f"Downloading files to local root: {local_path}")

    remote_host = cli_args.remote_host
    logging.info(f"Downloading files from remote host: {remote_host}")

    processed_data_path = Path(cli_args.processed_data_root)
    logging.info(f"Downloading files from remote processed data root: {processed_data_path}")

    analysis_path = Path(cli_args.analysis_root)
    logging.info(f"Downloading files from remote analysis root: {analysis_path}")

    log_patterns = cli_args.log_patterns
    logging.info(f"Downloading processing logs that match patterns: {log_patterns}")

    processed_subdirs = cli_args.processed_subdirs
    logging.info(f"Downloading processed data subdirs: {processed_subdirs}")

    experimenter = cli_args.subject
    if subject is None:
        experimenter = input("Experimenter initials: ").strip()
    logging.info(f"Downloading files for experimenter: {experimenter}")

    subject = cli_args.subject
    if subject is None:
        subject = input("Subject ID: ").strip()
    logging.info(f"Downloading files for subject id: {subject}")

    session_dates_string = cli_args.date
    if session_dates_string is None:
        session_dates_string = input("Session date MMDDYYYY: ").strip()
    session_date = datetime.strptime(session_dates_string, "%m%d%Y").date()
    logging.info(f"Downloading files for session date: {session_dates_string} ({session_date})")

    username = cli_args.user
    if username is None:
        username = input("Remote username: ").strip()
    logging.info(f"Downloading files as remote user: {username}")

    # Password will not be printed.
    password = getpass(f"Password for remote user {username}: ")

    try:
        run_main(
            local_path,
            remote_host,
            processed_data_path,
            analysis_path,
            log_patterns,
            processed_subdirs,
            experimenter,
            subject,
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
