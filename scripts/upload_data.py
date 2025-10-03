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


def apply_placeholders(
    original: str,
    experimenter: str,
    subject_id: str,
    session_date: date
) -> str:
    """Fill in session placeholders <EXPERIMENTER> <SUBJECT>, <YY>, <YYYY>, <MM>, and <DD>."""
    yy = session_date.strftime("%y")
    yyyy = session_date.strftime("%Y")
    mm = session_date.strftime("%m")
    dd = session_date.strftime("%d")
    applied = original.replace('<EXPERIMENTER>', experimenter).replace("<SUBJECT>", subject_id).replace("<YYYY>", yyyy).replace("<YY>", yy).replace("<MM>", mm).replace("<DD>", dd)
    return applied


def run_main(
    behavior_path: Path,
    behavior_txt_pattern: str,
    behavior_mat_pattern: str,
    ephys_path: Path,
    spikeglx_meta_pattern: str,
    openephys_oebin_pattern: str,
    remote_host: str,
    raw_data_path: Path,
    experimenter: str,
    subject: str,
    session_date: str,
    qualifier: str,
    username: str,
    password: str,
):
    # Resolve session-specific placeholders in glob patterns.
    behavior_txt_pattern = apply_placeholders(behavior_txt_pattern, experimenter, subject, session_date)
    behavior_mat_pattern = apply_placeholders(behavior_mat_pattern, experimenter, subject, session_date)
    spikeglx_meta_pattern = apply_placeholders(spikeglx_meta_pattern, experimenter, subject, session_date)
    openephys_oebin_pattern = apply_placeholders(openephys_oebin_pattern, experimenter, subject, session_date)

    # Collect files to upload as a list of (source_root, source_relative, destination_relative)
    to_upload = []

    # Locate behavior .mat and .txt within behavior_path.
    logging.info(f"Searching local behavior_root for .txt like: {behavior_txt_pattern}")
    session_mmddyyyy = session_date.strftime("%m%d%Y")
    for txt_match in behavior_path.glob(behavior_txt_pattern):
        txt_relative = txt_match.relative_to(behavior_path)
        logging.info(f"  {txt_relative}")
        destination_relative = Path(experimenter, subject, session_mmddyyyy, "behavior", txt_match.name)
        to_upload.append((behavior_path, txt_relative, destination_relative))

    logging.info(f"Searching local behavior_root for .mat like: {behavior_mat_pattern}")
    for mat_match in behavior_path.glob(behavior_mat_pattern):
        mat_relative = mat_match.relative_to(behavior_path)
        logging.info(f"  {mat_relative}")
        destination_relative = Path(experimenter, subject, session_mmddyyyy, "behavior", mat_match.name)
        to_upload.append((behavior_path, mat_relative, destination_relative))

    # Locate spikeglx meta files as representatives spikeglx run dirs.
    logging.info(f"Searching local ephys_root for .meta like: {spikeglx_meta_pattern}")
    spikeglx_metas = list(ephys_path.glob(spikeglx_meta_pattern))
    logging.info(f"Found .meta matches: {spikeglx_metas}")
    if spikeglx_metas:
        # Take the shortest match -- eg the nidq.meta, not a probe/ap.meta.
        spikeglx_meta = min(spikeglx_metas, key=lambda meta: len(meta.parts))
        run_dir = spikeglx_meta.parent
        logging.info(f"Found spikeglx run dir: {run_dir}")
        for spikglx_file in walk_flat(run_dir):
            spikglx_relative = spikglx_file.relative_to(ephys_path)
            logging.info(f"  {spikglx_relative}")
            destination_relative = Path(experimenter, subject, session_mmddyyyy, "ecephys", spikglx_file.relative_to(run_dir.parent))
            to_upload.append((ephys_path, spikglx_relative, destination_relative))

    # Locate openephys meta files as representatives recording dirs.
    logging.info(f"Searching local ephys_root for .oebin like: {openephys_oebin_pattern}")
    oebins = list(ephys_path.glob(openephys_oebin_pattern))
    logging.info(f"Found .oebin matches: {oebins}")
    if oebins:
        # Walk up several parents from an .oebin to find the recording dir.
        #   date/record_node/experiment/recording/structure.oebin
        oebin = oebins[0]
        run_dir = oebin.parent.parent.parent.parent
        logging.info(f"Found openephys run dir: {run_dir}")
        for openephys_file in walk_flat(run_dir):
            openephys_relative = openephys_file.relative_to(ephys_path)
            logging.info(f"  {openephys_relative}")
            destination_relative = Path(experimenter, subject, session_mmddyyyy, "ecephys", openephys_relative.relative_to(run_dir.parent))
            to_upload.append((ephys_path, openephys_relative, destination_relative))

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

            logging.info(f"Uploading to {raw_data_path}:")
            for source_root, source_relative, destination_relative in to_upload:
                source = Path(source_root, source_relative)
                destination = Path(raw_data_path, destination_relative)
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
        help="Glob pattern to match behavior .txt files within BEHAVIOR_ROOT. May include placeholders <EXPERIMENTER>, <SUBJECT>, <YYYY>, <YY>, <MM>, <DD> (default: %(default)s)",
        default="<SUBJECT>/**/*_<MM><DD><YY>_*.txt"
    )
    parser.add_argument(
        "--behavior-mat-pattern", "-M",
        type=str,
        help="Glob pattern to match behavior .mat files within BEHAVIOR_ROOT. May include placeholders <EXPERIMENTER>, <SUBJECT>, <YYYY>, <YY>, <MM>, <DD> (default: %(default)s)",
        default="<SUBJECT>/**/*_<MM><DD><YY>_*.mat"
    )
    parser.add_argument(
        "--ephys-root", "-E",
        type=str,
        help="Local root directory to search for a SpikeGLX run directory. (default: %(default)s)",
        default="/mnt/c/Users/labuser/Desktop/Data"
    )
    parser.add_argument(
        "--spikeglx-meta-pattern", "-S",
        type=str,
        help="Glob pattern to match SpikeGLX .meta files within EPHYS_ROOT. May include placeholders <EXPERIMENTER>, <SUBJECT>, <YYYY>, <YY>, <MM>, <DD> (default: %(default)s)",
        default="<SUBJECT>/**/*_<MM><DD><YYYY>_*.meta"
    )
    parser.add_argument(
        "--openephys-oebin-pattern", "-O",
        type=str,
        help="Glob pattern to match OpenEphys structure.oebin files within EPHYS_ROOT. May include placeholders <EXPERIMENTER>, <SUBJECT>, <YYYY>, <YY>, <MM>, <DD> (default: %(default)s)",
        default="<SUBJECT>/**/<YYYY>-<MM>-<DD>_*/*/*/*/structure.oebin"
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
        "--raw-data-root", "-a",
        type=str,
        help="Remote root directory containing lab raw data. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/raw_data/"
    )
    parser.add_argument(
        "--experimenter", "-e",
        type=str,
        help="Experimenter initials to group related data. (default: prompt for input)",
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

    cli_args = parser.parse_args(argv)

    # Prompt for missing input args as needed.
    behavior_path = Path(cli_args.behavior_root)
    logging.info(f"Uploading behavior files from : {behavior_path}")

    behavior_txt_pattern = cli_args.behavior_txt_pattern
    logging.info(f"Using behavior .txt pattern: {behavior_txt_pattern}")

    behavior_mat_pattern = cli_args.behavior_mat_pattern
    logging.info(f"Using behavior .mat pattern: {behavior_mat_pattern}")

    ephys_path = Path(cli_args.ephys_root)
    logging.info(f"Uploading ephys files from : {ephys_path}")

    spikeglx_meta_pattern = cli_args.spikeglx_meta_pattern
    logging.info(f"Using SpikeGLX .meta pattern: {spikeglx_meta_pattern}")

    openephys_oebin_pattern = cli_args.openephys_oebin_pattern
    logging.info(f"Using Open Ephys .oebin pattern: {openephys_oebin_pattern}")

    remote_host = cli_args.remote_host
    logging.info(f"Uploading files to remote host: {remote_host}")

    raw_data_path = Path(cli_args.raw_data_root)
    logging.info(f"Uploading files to remote raw data root: {raw_data_path}")

    experimenter = cli_args.experimenter
    if experimenter is None:
        experimenter = input("Experimenter initials: ").strip()
    logging.info(f"Uploading files for experimenter: {experimenter}")

    subject = cli_args.subject
    if subject is None:
        subject = input("Subject ID: ").strip()
    logging.info(f"Uploading files for subject id: {subject}")

    session_dates_string = cli_args.date
    if session_dates_string is None:
        session_dates_string = input("Session date MMDDYYYY: ").strip()
    session_date = datetime.strptime(session_dates_string, "%m%d%Y").date()
    logging.info(f"Uploading files for session date: {session_dates_string} ({session_date})")

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

    # Password will not be printed.
    password = getpass(f"Password for remote user {username}: ")

    try:
        run_main(
            behavior_path,
            behavior_txt_pattern,
            behavior_mat_pattern,
            ephys_path,
            spikeglx_meta_pattern,
            openephys_oebin_pattern,
            remote_host,
            raw_data_path,
            experimenter,
            subject,
            session_date,
            qualifier,
            username,
            password,
        )
    except:
        logging.error("Error uploading files.", exc_info=True)
        return -1


if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
