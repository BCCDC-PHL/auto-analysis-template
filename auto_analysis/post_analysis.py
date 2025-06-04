import csv
import datetime
import glob
import json
import logging
import os
import shutil

from . import parsers


def post_analysis_pipeline_1(config, pipeline, run):
    """
    Perform post-analysis tasks for the first pipeline.

    :param config: The config dictionary
    :type config: dict
    :param pipeline: The pipeline dictionary
    :type pipeline: dict
    :param run: The run dictionary
    :type run: dict
    :return: None
    :rtype: None
    """
    logging.info(json.dumps({
        "event_type": "post_analysis_started",
        "sequencing_run_id": run['sequencing_run_id'],
        "pipeline": pipeline,
        "run": run,
    }))
    sequencing_run_id = run['sequencing_run_id']
    analysis_run_output_dir = os.path.join(config['analysis_output_dir'], sequencing_run_id)
    pipeline_short_name = pipeline['name'].split('/')[1]
    pipeline_minor_version = ''.join(pipeline['version'].rsplit('.', 1)[0])
    analysis_pipeline_output_dir = pipeline.get('parameters', {}).get('outdir', None)
    logging.debug(json.dumps({
        "event_type": "analysis_pipeline_output_dir",
        "sequencing_run_id": sequencing_run_id,
        "analysis_pipeline_output_dir": analysis_pipeline_output_dir
    }))

    #
    # ...do whatever you need to do after this pipeline completes

    return None


def post_analysis_pipeline_2(config, pipeline, run):
    """
    Perform post-analysis tasks for the basic-nanopore-qc pipeline.

    :param config: The config dictionary
    :type config: dict
    :param pipeline: The pipeline dictionary
    :type pipeline: dict
    :param run: The run dictionary
    :type run: dict
    :return: None
    :rtype: None
    """
    logging.info(json.dumps({
        "event_type": "post_analysis_started",
        "sequencing_run_id": run['sequencing_run_id'],
        "pipeline": pipeline,
        "run": run,
    }))
    sequencing_run_id = run['sequencing_run_id']
    analysis_run_output_dir = os.path.join(config['analysis_output_dir'], sequencing_run_id)

    pipeline_short_name = pipeline['name'].split('/')[1]
    pipeline_minor_version = ''.join(pipeline['version'].rsplit('.', 1)[0])
    analysis_pipeline_output_dir = pipeline.get('parameters', {}).get('outdir', None)
    logging.debug(json.dumps({
        "event_type": "analysis_pipeline_output_dir",
        "sequencing_run_id": sequencing_run_id,
        "analysis_pipeline_output_dir": analysis_pipeline_output_dir
    }))
    
    return None


def post_analysis(config, pipeline, run, analysis_mode):
    """
    Perform post-analysis tasks for a pipeline.

    :param config: The config dictionary
    :type config: dict
    :param pipeline: The pipeline dictionary
    :type pipeline: dict
    :param run: The run dictionary
    :type run: dict
    :param analysis_mode: The analysis mode
    :type analysis_mode: str
    :return: None
    """
    pipeline_name = pipeline['name']
    pipeline_short_name = pipeline_name.split('/')[1]
    pipeline_version = pipeline['version']
    delete_pipeline_work_dir = pipeline.get('delete_work_dir', True)
    sequencing_run_id = run['sequencing_run_id']
    base_analysis_work_dir = config['analysis_work_dir']

    # The work_dir includes a timestamp, so we need to glob to find the most recent one
    work_dir_glob = os.path.join(base_analysis_work_dir, 'work-' + sequencing_run_id + '_' + pipeline_short_name + '_' + '*')
    work_dirs = glob.glob(work_dir_glob)
    if len(work_dirs) > 0:
        work_dir = work_dirs[-1]
    else:
        work_dir = None

    if work_dir and delete_pipeline_work_dir:
        try:
            shutil.rmtree(work_dir, ignore_errors=True)
            logging.info(json.dumps({
                "event_type": "analysis_work_dir_deleted",
                "sequencing_run_id": sequencing_run_id,
                "analysis_work_dir_path": work_dir
            }))
        except OSError as e:
            logging.error(json.dumps({
                "event_type": "delete_analysis_work_dir_failed",
                "sequencing_run_id": analysis_run_id,
                "analysis_work_dir_path": analysis_work_dir
            }))
    else:
        if not work_dir or not os.path.exists(work_dir):
            logging.warning(json.dumps({
                "event_type": "analysis_work_dir_not_found",
                "sequencing_run_id": sequencing_run_id,
                "analysis_work_dir_glob": work_dir_glob
            }))
        elif not delete_pipeline_work_dir:
            logging.info(json.dumps({
                "event_type": "skipped_deletion_of_analysis_work_dir",
                "sequencing_run_id": sequencing_run_id,
                "analysis_work_dir_path": work_dir
            }))

    if pipeline_name == 'BCCDC-PHL/pipeline-1':
        return post_analysis_pipeline_1(config, pipeline, run)
    elif pipeline_name == 'BCCDC-PHL/pipeline-2':
        return post_analysis_pipeline_2(config, pipeline, run)
    else:
        logging.warning(json.dumps({
            "event_type": "post_analysis_not_implemented",
            "sequencing_run_id": sequencing_run_id,
            "pipeline_name": pipeline_name
        }))
        return None
