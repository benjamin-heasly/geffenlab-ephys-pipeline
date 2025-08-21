import sys
from argparse import ArgumentParser
from typing import Optional, Sequence
import logging
from pathlib import Path
from datetime import datetime, date
from getpass import getpass
from fnmatch import fnmatchcase


from fabric import Connection


def set_up_logging():
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def run_main(
    behavior_path: Path,
    spikeglx_path: Path,
    remote_host: str,
    data_path: Path,
    subject_id: str,
    session_date: str,
    username: str,
    password: str,
    upload_filter: str
):
    # Use consistent date formatting like MMDDYYYY and MMDDYY.
    date_string_yyyy = session_date.strftime("%m%d%Y")
    date_string_yy = session_date.strftime("%m%d%y")

    # Locate behavior .mat and .txt within behavior_path, using date and subject.

    # Locate files in spikeglx run dir within spikeglx_path, using date and subject.


    logging.info(f"Connecting to remote host: {remote_host}.")
    with Connection(host=remote_host, user=username, connect_kwargs={"password": password}) as c:
        try:
            # Call to open() will log connection attempts, results.
            c.open()

            # Upload each file we found above.
            # Continue valiantly if there was an error.
            # Able to filter these based on a pattern (to retry failures).
            #if not upload_filter or fnmatchcase(file, upload_filter)

        except Exception as e:
            logging.warning(f"Upload error: {e.args}")

    logging.info("OK.\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    set_up_logging()

    parser = ArgumentParser(description="Upload raw session data from the local machine to cortex.")

    parser.add_argument(
        "--behavior-root", "-b",
        type=str,
        help="Local root directory where behavior data are located. (default: %(default)s)",
        default="TODO"
    )
    parser.add_argument(
        "--spikeglx-root", "-g",
        type=str,
        help="Local root directory where spikeglx data are located. (default: %(default)s)",
        default="TODO"
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
        "--data-root", "-a",
        type=str,
        help="Remote root directory containing lab data. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/data/"
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
        "--upload-filter", "-f",
        type=str,
        help="Unix shell wildcard pattern to filter which files are uploaded (eg to retry *.txt, *ap.bin, *nidq.bin, etc.). (default: upload all files)",
        default=None
    )

    cli_args = parser.parse_args(argv)

    # Prompt for missing input args as needed.
    behavior_path = Path(cli_args.behavior_root)
    logging.info(f"Uploading behavior files from : {behavior_path}")

    spikeglx_path = Path(cli_args.spikeglx_root)
    logging.info(f"Uploading SpikeGLX files from : {spikeglx_path}")

    remote_host = cli_args.remote_host
    logging.info(f"Uploading files to remote host: {remote_host}")

    data_path = Path(cli_args.data_path)
    logging.info(f"Uploading files to remote data root: {data_path}")

    subject_id = cli_args.subject_id
    if subject_id is None:
        subject_id = input("Subject ID: ").strip()
    logging.info(f"Uploading files for subject id: {subject_id}")

    session_dates_string = cli_args.session_date
    if session_dates_string is None:
        session_dates_string = input("Session date MMDDYYYY: ").strip()

    session_date = datetime.strptime(session_dates_string, "%m%d%Y").date()
    logging.info(f"Uploading files for session date: {session_dates_string} ({session_date})")

    username = cli_args.username
    if username is None:
        username = input("Remote username: ").strip()
    logging.info(f"Uploading files as remote user: {username}")

    upload_filter = cli_args.upload_filter
    if upload_filter is None:
        upload_filter = input("Upload filter (None = upload all, or eg *.txt, *ap.bin, *nidq.bin, etc.): ").strip()
    if upload_filter:
        logging.info(f"Uploading files matching filter: {upload_filter}")
    else:
        logging.info(f"Uploading all files.")

    # Password will not be printed.
    password = getpass(f"Password for remote user {username}: ")

    try:
        run_main(
            behavior_path,
            spikeglx_path,
            remote_host,
            data_path,
            subject_id,
            session_date,
            username,
            password,
            upload_filter
        )
    except:
        logging.error("Error uploading files.", exc_info=True)
        return -1


if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
