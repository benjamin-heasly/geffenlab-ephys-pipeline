import sys
from argparse import ArgumentParser
from typing import Optional, Sequence
import logging
from datetime import datetime, timezone
from pathlib import Path


def set_up_logging(
    log_path: Path = None
):
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

):
    logging.info("Starting pipeline run.\n")

    logging.info("Gathering pipeline logs.\n")

    logging.info("OK\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser(description="Run a Nextflow pipeline and gather logs in one place.")

    parser.add_argument(
        "--nextflow", "-n",
        type=str,
        help="Nextflow executable name or full path. (default: %(default)s)",
        default="nextflow-25.04.6-dist"
    )
    parser.add_argument(
        "--nextflow-config", "-c",
        type=str,
        help="Path to pipeline configuration file. (default: %(default)s)",
        default="geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config"
    )
    parser.add_argument(
        "--nextflow-workflow", "-w",
        type=str,
        help="Path to pipeline workflow definition file. (default: %(default)s)",
        default="aind-ephys-pipeline/pipeline/main_multi_backend.nf"
    )
    parser.add_argument(
        "--nextflow-report-template", "-r",
        type=str,
        help="Path to nextflow process detail report template. (default: %(default)s)",
        default="geffenlab-ephys-pipeline/process_detail_template.md"
    )
    parser.add_argument(
        "--work-dir", "-W",
        type=str,
        help="Working directory to run pipelines from. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/nextflow"
    )
    parser.add_argument(
        "--work-env", "-e",
        type=str,
        help="Environment variable assignments to prepend when running Nextflow. (default: %(default)s)",
        default="NXF_DISABLE_PARAMS_TYPE_DETECTION=1"
    )
    parser.add_argument(
        "--data-root", "-D",
        type=str,
        help="Root folder with the lab's raw data. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/data"
    )
    parser.add_argument(
        "--analysis-root", "-A",
        type=str,
        help="Root folder with the lab's analysis products. (default: %(default)s)",
        default="/vol/cortex/cd4/geffenlab/analysis"
    )
    parser.add_argument(
        "--subject", "-s",
        type=str,
        help="Subject of the session to be processed. (default: %(default)s)",
        default="AS20-minimal2"
    )
    parser.add_argument(
        "--date", "-d",
        type=str,
        help="Date of the session to be processed DDMMYYYY. (default: %(default)s)",
        default="03112025"
    )

    (cli_args, pass_through_args) = parser.parse_known_args()

    nextflow_path = Path(cli_args.nextflow)
    work_dir_path = Path(cli_args.work_dir)
    workflow_path = Path(cli_args.nextflow_workflow)
    config_path = Path(cli_args.nextflow_config)
    report_template_path = Path(cli_args.nextflow_report_template)

    analysis_root_path = Path(cli_args.analysis_root)
    analysis_path = Path(analysis_root_path, cli_args.subject, cli_args.date)

    data_root_path = Path(cli_args.data_root)
    data_path = Path(data_root_path, cli_args.subject, cli_args.date)

    # Choose a reasonably unique "run name" for this Nextflow run.
    # This allows us to aggregate process logs after the run completes.
    execution_time = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%Z')
    run_name = f"{workflow_path.stem}_{execution_time}"

    # Choose where to write logs.
    script_log_path = Path(analysis_path, f"{run_name}_run_pipeline.log")
    nextflow_log_path = Path(analysis_path, f"{run_name}_nextflow.log")
    process_detail_path = Path(analysis_path, f"{run_name}_process_detail.md")
    set_up_logging(script_log_path)

    logging.info(f"From work dir {work_dir_path}")
    logging.info(f"Running workflow {workflow_path}")
    logging.info(f"With config {config_path}")
    logging.info(f"With pipeline params and Nextflow options {pass_through_args}")
    logging.info(f"Using Nextflow {nextflow_path}")
    logging.info(f"With command env {cli_args.work_env}")
    logging.info(f"Using data path {data_path}")
    logging.info(f"Using analysis path {analysis_path}")
    logging.info(f"Writing Nextflow log to {nextflow_log_path}")
    logging.info(f"Writing process detail report template {report_template_path}")
    logging.info(f"Writing process detail report to {process_detail_path}")

    try:
        run_main(
        )
    except:
        logging.error("Error running Nextflow pipeline.", exc_info=True)
        return -1


if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)


# REPLACING

# cd /vol/cortex/cd4/geffenlab/nextflow
# conda activate geffen-pipelines

# NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
#   -C geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config \
#   run aind-ephys-pipeline/pipeline/main_multi_backend.nf \
#   --subject AS20-minimal2 \
#   --date 03112025

# NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
#   -C geffenlab-ephys-pipeline/aind-ephys-pipeline/my-configuration.config \
#   run aind-ephys-pipeline/pipeline/main_multi_backend.nf \
#   --params_file geffenlab-ephys-pipeline/aind-ephys-pipeline/my-parameters.json \
#   --gpu_device 2
#   ...

# cd /vol/cortex/cd4/geffenlab/nextflow
# conda activate geffen-pipelines

# NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
#   -C geffenlab-ephys-pipeline/pipeline/cortex.config \
#   run geffenlab-ephys-pipeline/pipeline/main.nf \
#   --subject AS20-minimal2 \
#   --date 03112025

# NXF_DISABLE_PARAMS_TYPE_DETECTION=1 ./nextflow-25.04.6-dist \
#   -C geffenlab-ephys-pipeline/pipeline/my_config.config \
#   run geffenlab-ephys-pipeline/pipeline/main.nf \
#   --catgt_run 'AS20_03112025_trainingSingle6Tone2024_Snk3.1' \
#   --catgt_gate 0 \
#   --catgt_trigger 0 \
#   ...


# ARGS
# work_dir /vol/cortex/cd4/geffenlab/nextflow
# work_env NXF_DISABLE_PARAMS_TYPE_DETECTION=1

# data_root = '/vol/cortex/cd4/geffenlab/data'
# analysis_root = '/vol/cortex/cd4/geffenlab/analysis'
# subject = 'AS20-minimal2'
# date = '03112025'

# log *choose file in analysis/processed subdir for session*

# nextflow_executable ./nextflow-25.04.6-dist
# nextflow_config geffenlab-ephys-pipeline/aind-ephys-pipeline/cortex.config
# nextflow_pipeline aind-ephys-pipeline/pipeline/main_multi_backend.nf
# nextflow_report_template geffenlab-ephys-pipeline/report_template.md


# nextflow_run_name *pick unique*
# nextflow_log *choose file in analysis/processed subdir for session*
# nextflow_process_logs *choose subdir in analysis/processed subdir for session*

# nextflow options
#   -resume

# pipeline params
#   --subject AS20-minimal2 \
#   --date 03112025
#   --params_file geffenlab-ephys-pipeline/aind-ephys-pipeline/my-parameters.json \
#   --gpu_device 2
#   --catgt_run 'AS20_03112025_trainingSingle6Tone2024_Snk3.1' \
#   --catgt_gate 0 \
#   --catgt_trigger 0 \


# DO
#
# Create the analysis subdir if needed
#
# decide where logged outputs will go, based on data coords.
# pick a reasonably unique "run name" based on data coords, date?
#
# log to console and to script log file
# cook up a big Nextflow run command
#   choose the executable path
#   disable CLI arg type guessing
#   choose nextflow config -C
#   choose nextflow pipeline to run
#   choose nextflow top-level log in the session processed directory
#   pass along the data coords like --data_root, --analysis_root, --subject, --date
#   pass along unstructured --params and -options
#
# log the command
#
# change to work_dir with context lib
# run the command
# tail stdout and stderr
# write stdout and stderr to script log
# log stdout and stderr to console
#
# regardless of success or failure
# Cook up a Nextflow log command
#   use chosen run name
#   use chosen report template
# log the command
#
# change to work_dir with context lib
# run the command
# grab output and save to session processed directory
