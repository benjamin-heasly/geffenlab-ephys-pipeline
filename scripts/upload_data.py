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


def walk_flat(
    path: Path
) -> list[Path]:
    """walk() the given path and return a flat list of regular files."""
    flat_list = []
    for parent, dirs, files in path.walk():
        for file in files:
            flat_list.append(Path(parent, file))
    return flat_list


def apply_session(
    original: str,
    subject_id: str,
    session_date: date
) -> str:
    """Fill in session placeholders <SUBJECT>, <MMDDYY>, and <MMDDYYYY>."""
    session_mmddyyyy = session_date.strftime("%m%d%Y")
    session_mmddyy = session_date.strftime("%m%d%y")
    return original.replace("<SUBJECT>", subject_id).replace("<MMDDYY>", session_mmddyy).replace("<MMDDYYYY>", session_mmddyyyy)


def run_main(
    behavior_path: Path,
    behavior_txt_pattern: str,
    behavior_mat_pattern: str,
    spikeglx_path: Path,
    spikeglx_nidq_pattern: str,
    remote_host: str,
    data_path: Path,
    subject: str,
    session_date: str,
    username: str,
    password: str,
    qualifier: str
):
    # Resolve session-specific placeholders in glob patterns.
    behavior_txt_pattern = apply_session(behavior_txt_pattern, subject, session_date)
    behavior_mat_pattern = apply_session(behavior_mat_pattern, subject, session_date)
    spikeglx_nidq_pattern = apply_session(spikeglx_nidq_pattern, subject, session_date)

    # Collect files to upload as a list of (source_root, source_relative, destination_relative)
    to_upload = []

    # Locate behavior .mat and .txt within behavior_path.
    logging.info(f"Searching local behavior_root for .txt like: {behavior_txt_pattern}")
    session_mmddyyyy = session_date.strftime("%m%d%Y")
    for txt_match in behavior_path.glob(behavior_txt_pattern):
        txt_relative = txt_match.relative_to(behavior_path)
        logging.info(f"  {txt_relative}")
        destination_relative = Path(subject, session_mmddyyyy, "behavior", txt_match.name)
        to_upload.append((behavior_path, txt_relative, destination_relative))

    logging.info(f"Searching local behavior_root for .mat like: {behavior_mat_pattern}")
    for mat_match in behavior_path.glob(behavior_mat_pattern):
        mat_relative = mat_match.relative_to(behavior_path)
        logging.info(f"  {mat_relative}")
        destination_relative = Path(subject, session_mmddyyyy, "behavior", mat_match.name)
        to_upload.append((behavior_path, mat_relative, destination_relative))

    # Locate spikeglx nidq.meta files as representatives of overall run dirs.
    logging.info(f"Searching local spikeglx_root for nidq.meta like: {spikeglx_nidq_pattern}")
    for nidq_match in spikeglx_path.glob(spikeglx_nidq_pattern):
        run_dir = nidq_match.parent
        for spikglx_file in walk_flat(run_dir):
            spikglx_relative = spikglx_file.relative_to(spikeglx_path)
            logging.info(f"  {spikglx_relative}")
            destination_relative = Path(subject, session_mmddyyyy, "ecephys", spikglx_file.relative_to(run_dir.parent))
            to_upload.append((spikeglx_path, spikglx_relative, destination_relative))

    if qualifier:
        logging.info(f"Keeping only files that match qualifier: {qualifier}")
        to_upload = [item for item in to_upload if qualifier in item[1].as_posix()]

    if not to_upload:
        logging.warning("No files to upload.")
        return

    logging.info(f"Planning to create {len(to_upload)} files in remote data_root:")
    for source_root, source_relative, destination_relative in to_upload:
        logging.info(f"  {destination_relative}")

    # Confirm before uploading
    go_ahead = input("Do you want to upload these files?  Type 'yes' to proceed: ").strip()
    if go_ahead != "yes":
        logging.warning("Stopping without uploading files.")
        return

    logging.warning("Proceeding to upload files.")

    logging.info(f"Connecting to remote host: {remote_host}.")
    with Connection(host=remote_host, user=username, connect_kwargs={"password": password}) as c:
        try:
            # Call to open() will log connection attempts, results.
            c.open()

            logging.info(f"Uploading to {data_path}:")
            for source_root, source_relative, destination_relative in to_upload:
                source = Path(source_root, source_relative)
                destination = Path(data_path, destination_relative)
                logging.info(f"  {destination_relative}")
                c.run(f"mkdir -p {destination.parent.as_posix()}")
                c.put(source.as_posix(), destination.as_posix())

        except Exception as e:
            logging.warning(f"Upload error: {e.args}")

    logging.info("OK.\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    set_up_logging()

    parser = ArgumentParser(description="Upload raw session data from the local machine to cortex.")

    parser.add_argument(
        "--behavior-root", "-b",
        type=str,
        help="Local root directory to search for behavior files. (default: %(default)s)",
        default="/mnt/c/Users/labuser/Desktop/Data"
    )
    parser.add_argument(
        "--behavior-txt-pattern", "-T",
        type=str,
        help="Glob pattern to match behavior .txt files within BEHAVIOR_ROOT. May include placeholders <SUBJECT>, <MMDDYY> and <MMDDYYYY> (default: %(default)s)",
        default="<SUBJECT>/**/*_<MMDDYY>_*.txt"
    )
    parser.add_argument(
        "--behavior-mat-pattern", "-M",
        type=str,
        help="Glob pattern to match behavior .mat files within BEHAVIOR_ROOT. May include placeholders <SUBJECT>, <MMDDYY> and <MMDDYYYY> (default: %(default)s)",
        default="<SUBJECT>/**/*_<MMDDYY>_*.mat"
    )
    parser.add_argument(
        "--spikeglx-root", "-g",
        type=str,
        help="Local root directory to search for a SpikeGLX run directory. (default: %(default)s)",
        default="/mnt/c/Users/labuser/Desktop/Data"
    )
    parser.add_argument(
        "--spikeglx-nidq-pattern", "-G",
        type=str,
        help="Glob pattern to match SpikeGLX nidq .meta files within SPIKEGLX_ROOT. May include placeholders <SUBJECT>, <MMDDYY> and <MMDDYYYY> (default: %(default)s)",
        default="<SUBJECT>/**/*_<MMDDYYYY>_*.nidq.meta"
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
        "--data-root", "-a",
        type=str,
        help="Remote root directory containing lab data. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/data/"
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

    cli_args = parser.parse_args(argv)

    # Prompt for missing input args as needed.
    behavior_path = Path(cli_args.behavior_root)
    logging.info(f"Uploading behavior files from : {behavior_path}")

    behavior_txt_pattern = cli_args.behavior_txt_pattern
    logging.info(f"Using behavior .txt pattern: {behavior_txt_pattern}")

    behavior_mat_pattern = cli_args.behavior_mat_pattern
    logging.info(f"Using behavior .mat pattern: {behavior_mat_pattern}")

    spikeglx_path = Path(cli_args.spikeglx_root)
    logging.info(f"Uploading SpikeGLX files from : {spikeglx_path}")

    spikeglx_nidq_pattern = cli_args.spikeglx_nidq_pattern
    logging.info(f"Using SpikeGLX nidq pattern: {spikeglx_nidq_pattern}")

    remote_host = cli_args.remote_host
    logging.info(f"Uploading files to remote host: {remote_host}")

    data_path = Path(cli_args.data_root)
    logging.info(f"Uploading files to remote data root: {data_path}")

    subject = cli_args.subject
    if subject is None:
        subject = input("Subject ID: ").strip()
    logging.info(f"Uploading files for subject id: {subject}")

    session_dates_string = cli_args.session_date
    if session_dates_string is None:
        session_dates_string = input("Session date MMDDYYYY: ").strip()
    session_date = datetime.strptime(session_dates_string, "%m%d%Y").date()
    logging.info(f"Uploading files for session date: {session_dates_string} ({session_date})")

    qualifier = cli_args.qualifier
    if qualifier is None:
        qualifier = input("Qualifier like 'training', or 'ap.bin'.  Leave blank to upload all: ").strip()
    if qualifier:
        logging.info(f"Uploading files matching qualifier: {qualifier}.")
    else:
        logging.info(f"Uploading all files.")

    username = cli_args.user
    if username is None:
        username = input("Remote username: ").strip()
    logging.info(f"Uploading files as remote user: {username}")

    # Password will not be printed.
    password = getpass(f"Password for remote user {username}: ")

    try:
        run_main(
            behavior_path,
            behavior_txt_pattern,
            behavior_mat_pattern,
            spikeglx_path,
            spikeglx_nidq_pattern,
            remote_host,
            data_path,
            subject,
            session_date,
            username,
            password,
            qualifier
        )
    except:
        logging.error("Error uploading files.", exc_info=True)
        return -1


if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
