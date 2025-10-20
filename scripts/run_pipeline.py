import sys
from os import environ
from argparse import ArgumentParser
from typing import Optional, Sequence
import logging
from datetime import datetime, timezone
from pathlib import Path
import subprocess
from contextlib import chdir


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


def run_main(
    work_dir_path: Path,
    nextflow: str,
    workflow_path: Path,
    config_path: Path,
    raw_data_root_path: Path,
    processed_data_root_path: Path,
    analysis_root_path: Path,
    experimenter: str,
    subject: str,
    date: str,
    run_name: str,
    nextflow_log_path: Path,
    pass_through_args: list[str],
    report_template_path: Path,
    process_detail_path: Path
) -> int:
    logging.info("Starting pipeline run.\n")

    pipeline_exit_code = 0

    run_command = [
        nextflow,
        "-C", config_path.as_posix(),
        "-log", nextflow_log_path.as_posix(),
        "run", workflow_path.as_posix(),
        "-name", run_name,
        "--raw_data_root", raw_data_root_path.as_posix(),
        "--processed_data_root", processed_data_root_path.as_posix(),
        "--analysis_root", analysis_root_path.as_posix(),
        "--experimenter", experimenter,
        "--subject", subject,
        "--date", date,
    ] + pass_through_args
    logging.info(f"Nextflow run command: {run_command}.")

    try:
        with chdir(work_dir_path):
            logging.info(f"Running from work dir: {work_dir_path}.")

            # We don't want dates like 03112025 to be parsed as ints -- we want to keep the leading "0"!
            env = environ.copy()
            env["NXF_DISABLE_PARAMS_TYPE_DETECTION"] = "1"
            process = subprocess.Popen(
                run_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=env
            )

            # Tail the Nextflow output as it comes.
            for line in process.stdout:
                logging.info(line.strip())

            exit_code = process.wait()
            if exit_code == 0:
                logging.info(f"Completed OK, exit code {exit_code}")
            else:
                logging.error(f"Completed with error, exit code {exit_code}")
                pipeline_exit_code = exit_code

    except Exception:
        logging.error(f"Error running Nextflow", exc_info=True)

    logging.info("Gathering pipeline logs.\n")

    log_command = [
        nextflow,
        "log", run_name,
        "-t", report_template_path.as_posix(),
    ]
    logging.info(f"Nextflow log command: {log_command}.")

    try:
        with chdir(work_dir_path):
            logging.info(f"Running from work dir: {work_dir_path}.")
            process = subprocess.Popen(
                log_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Write the Nextflow report to file.
            with open(process_detail_path, 'w') as f:
                for line in process.stdout:
                    f.write(line)

            exit_code = process.wait()
            if exit_code == 0:
                logging.info(f"Completed OK, exit code {exit_code}")
            else:
                logging.error(f"Completed with error, exit code {exit_code}")

    except Exception:
        logging.error(f"Error gathering Nextflow logs", exc_info=True)

    if pipeline_exit_code == 0:
        logging.info("OK\n")
    return pipeline_exit_code


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser(description="Run a Nextflow pipeline and aggregate logs to one place.")

    parser.add_argument(
        "--nextflow",
        type=str,
        help="Nextflow executable name or full path. (default: %(default)s)",
        default="./nextflow-25.04.6-dist"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to pipeline configuration file. (default: %(default)s)",
        default="geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config"
    )
    parser.add_argument(
        "--workflow",
        type=str,
        help="Path to pipeline workflow definition file. (default: %(default)s)",
        default="aind-ephys-pipeline/pipeline/main_multi_backend.nf"
    )
    parser.add_argument(
        "--report-template",
        type=str,
        help="Path to nextflow process detail report template. (default: %(default)s)",
        default="geffenlab-ephys-pipeline/scripts/process-detail-template.md"
    )
    parser.add_argument(
        "--work-dir",
        type=str,
        help="Working directory to run pipelines from. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/nextflow"
    )
    parser.add_argument(
        "--raw-data-root",
        type=str,
        help="Root folder with the lab's raw data. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/raw_data"
    )
    parser.add_argument(
        "--processed-data-root",
        type=str,
        help="Root folder with the lab's processed data. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/processed_data"
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
        default="AS20-minimal2"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date of the session to be processed DDMMYYYY. (default: %(default)s)",
        default="03112025"
    )

    (cli_args, pass_through_args) = parser.parse_known_args()
    work_dir_path = Path(cli_args.work_dir)
    workflow_path = Path(cli_args.workflow)
    config_path = Path(cli_args.config)
    report_template_path = Path(cli_args.report_template)
    raw_data_root_path = Path(cli_args.raw_data_root)
    processed_data_root_path = Path(cli_args.processed_data_root)
    analysis_root_path = Path(cli_args.analysis_root)

    # Choose a reasonably unique "run name" for this Nextflow run.
    # This allows us to aggregate process logs after the run completes.
    execution_time = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%Z')
    run_name = f"{workflow_path.stem}_{execution_time}"

    # Write logs to the sessions processed output subdirectory.
    logs_path = Path(processed_data_root_path, cli_args.experimenter, cli_args.subject, cli_args.date)
    logs_path.mkdir(exist_ok=True, parents=True)
    script_log_path = Path(logs_path, f"{run_name}_run_pipeline.log")
    nextflow_log_path = Path(logs_path, f"{run_name}_nextflow.log")
    process_detail_path = Path(logs_path, f"{run_name}_process_detail.md")
    set_up_logging(script_log_path)

    logging.info(f"From work dir {work_dir_path}")
    logging.info(f"Running workflow {workflow_path}")
    logging.info(f"With config {config_path}")
    logging.info(f"With pipeline params and Nextflow options {pass_through_args}")
    logging.info(f"Using Nextflow {cli_args.nextflow}")
    logging.info(f"Using raw data root {raw_data_root_path}")
    logging.info(f"Using processed data root {processed_data_root_path}")
    logging.info(f"Using analysis root {analysis_root_path}")
    logging.info(f"For experimenter {cli_args.experimenter}")
    logging.info(f"For session subject {cli_args.subject}")
    logging.info(f"For session date {cli_args.date}")
    logging.info(f"Writing Nextflow log to {nextflow_log_path}")
    logging.info(f"Using process detail report template {report_template_path}")
    logging.info(f"Writing process detail report to {process_detail_path}")

    try:
        run_main(
            work_dir_path,
            cli_args.nextflow,
            workflow_path,
            config_path,
            raw_data_root_path,
            processed_data_root_path,
            analysis_root_path,
            cli_args.experimenter,
            cli_args.subject,
            cli_args.date,
            run_name,
            nextflow_log_path,
            pass_through_args,
            report_template_path,
            process_detail_path
        )
    except:
        logging.error("Error running Nextflow pipeline.", exc_info=True)
        return -1

    logging.info(f"Wrote the Nextflow log to {nextflow_log_path}")
    logging.info(f"Wrote details of each Nextflow processing step to {process_detail_path}")
    logging.info(f"Wrote a copy of this console log to {script_log_path}")


if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
