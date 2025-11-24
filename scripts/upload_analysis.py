import sys
from argparse import ArgumentParser
from typing import Optional, Sequence
import logging
from pathlib import Path
from datetime import datetime
from getpass import getpass


from fabric import Connection


def set_up_logging():
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def walk_flat(
    path: Path
) -> list[Path]:
    """walk() the given path and return a flat list of regular files."""
    flat_list = []
    for parent, dirs, files in path.walk():
        for file in files:
            flat_list.append(Path(parent, file))
    return flat_list


def run_main(
    local_analysis_path: Path,
    remote_host: str,
    remote_analysis_path: Path,
    experimenter: str,
    subject: str,
    session_dates: list[str],
    qualifier: str,
    username: str,
    group_permissions: str,
    other_permissions: str,
):
    # Collect files to upload as a list of (source_root, source_relative, destination_relative, session_mmddyyyy)
    to_upload = []

    for session_date in session_dates:
        session_mmddyyyy = session_date.strftime("%m%d%Y")
        logging.info(f"Looking for session date: {session_date} AKA {session_mmddyyyy}")

        # Locate local analysis files.
        local_analysis_subdir = Path(local_analysis_path, experimenter, subject, session_mmddyyyy)
        logging.info(f"Looking in local analysis subdir: {local_analysis_subdir}")

        for local_file in walk_flat(local_analysis_subdir):
            relative = local_file.relative_to(local_analysis_path)
            logging.info(f"  {relative}")
            to_upload.append((local_analysis_path, relative, relative, session_mmddyyyy))

    if qualifier:
        logging.info(f"Keeping only files that match qualifier: {qualifier}")
        to_upload = [item for item in to_upload if qualifier in item[1].as_posix()]

    if not to_upload:
        logging.warning("No files to upload.")
        return

    logging.info(f"Planning to create {len(to_upload)} files in remote dir {remote_analysis_path}:")
    for source_root, source_relative, destination_relative, session_mmddyyyy in to_upload:
        logging.info(f"  {destination_relative}")

    # Confirm before uploading
    go_ahead = input(f"Do you want to upload these {len(to_upload)} files?  Type 'yes' to proceed: ").strip()
    if go_ahead != "yes":
        logging.warning("Stopping without uploading files.")
        return

    logging.warning("Proceeding to upload files.")

    # Password will not be printed.
    password = getpass(f"Password for remote user {username}: ")

    logging.info(f"Connecting to remote host: {remote_host}.")
    with Connection(host=remote_host, user=username, connect_kwargs={"password": password}) as c:
        try:
            # Call to open() will log connection attempts, results.
            c.open()

            # Upload each individual file.
            logging.info(f"Uploading to {remote_analysis_path}:")
            for source_root, source_relative, destination_relative, session_mmddyyyy in to_upload:
                source = Path(source_root, source_relative)
                destination = Path(remote_analysis_path, destination_relative)
                logging.info(f"  {destination_relative}")
                c.run(f"mkdir -p {destination.parent.as_posix()}")
                c.put(source.as_posix(), destination.as_posix())

            # Set directory and file permissions for each unique session date.
            session_paths = {
                Path(remote_analysis_path, experimenter, subject, session_mmddyyyy)
                for _, _, _, session_mmddyyyy in to_upload
            }
            for session_path in session_paths:
                logging.info(f"Setting 'group' and 'other' permissions for session dir {session_path}:")
                c.run(f"chmod -R g{group_permissions} {session_path.as_posix()}")
                c.run(f"chmod -R o{other_permissions} {session_path.as_posix()}")

        except Exception as e:
            logging.warning(f"Upload error: {e.args}")

    logging.info("OK.\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    set_up_logging()

    parser = ArgumentParser(description="Upload a session analysis/ subdir from local, back to cortex.")

    parser.add_argument(
        "--local-analysis-root", "-L",
        type=str,
        help="Local root directory with session analysis subdirs. (default: %(default)s)",
        default="./pipeline-results/analysis"
    )
    parser.add_argument(
        "--remote-host", "-r",
        type=str,
        help="Remote host (eg cortex) to connect to. (default: %(default)s)",
        default="128.91.19.199"
    )
    parser.add_argument(
        "--remote-analysis-root", "-A",
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
        "--qualifier", "-q",
        type=str,
        help="Additional text that must match uploaded file names, for example 'training', 'test', or 'ap.bin'. (default: None, upload all files)",
        default=None
    )
    parser.add_argument(
        "--user", "-u",
        type=str,
        help="Remote (eg cortex) username. (default: prompt for input)",
        default=None
    )
    parser.add_argument(
        "--group-permissions", "-g",
        type=str,
        help="Permission to set on uploaded dirs and files, for users in the same group. (default: %(default)s)",
        default="+rwx"
    )
    parser.add_argument(
        "--other-permissions", "-o",
        type=str,
        help="Permission to set on uploaded dirs and files, for other users (the universe). (default: %(default)s)",
        default="-rwx"
    )

    cli_args = parser.parse_args(argv)

    # Prompt for missing input args as needed.
    local_analysis_path = Path(cli_args.local_analysis_root).expanduser().resolve()
    logging.info(f"Uploading files from local analysis root: {local_analysis_path}")

    remote_host = cli_args.remote_host
    logging.info(f"Uploading files to remote host: {remote_host}")

    remote_analysis_path = Path(cli_args.remote_analysis_root)
    logging.info(f"Uploading files to remote analysis root: {remote_analysis_path}")

    experimenter = cli_args.experimenter
    if experimenter is None:
        experimenter = input("Experimenter initials: ").strip()
    logging.info(f"Uploading files for experimenter: {experimenter}")

    subject = cli_args.subject
    if subject is None:
        subject = input("Subject ID: ").strip()
    logging.info(f"Uploading files for subject id: {subject}")

    session_dates_strings = cli_args.date
    if not session_dates_strings:
        session_dates_strings = input("Session date MMDDYYYY (multiple dates may be separated by spaces): ").strip().split(' ')
    session_dates = [datetime.strptime(s, "%m%d%Y").date() for s in session_dates_strings]
    session_dates_formated = [str(d) for d in session_dates]
    logging.info(f"Uploading files for session date(s): {session_dates_formated}")

    qualifier = cli_args.qualifier
    if qualifier is None:
        qualifier = input("Qualifier like 'training','ap.bin', 'recording1', etc.  Leave blank to upload all: ").strip()
    if qualifier:
        logging.info(f"Uploading files matching qualifier: {qualifier}.")
    else:
        logging.info(f"Uploading all files.")

    username = cli_args.user
    if username is None:
        username = input("Remote username: ").strip()
    logging.info(f"Uploading files as remote user: {username}")

    try:
        run_main(
            local_analysis_path,
            remote_host,
            remote_analysis_path,
            experimenter,
            subject,
            session_dates,
            qualifier,
            username,
            cli_args.group_permissions,
            cli_args.other_permissions,
        )
    except:
        logging.error("Error uploading files.", exc_info=True)
        return -1


if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
