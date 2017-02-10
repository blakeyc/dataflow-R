# dataflow-R
> Example boilerplate for using R with Dataflow

This is intended to be a point of reference starter boilerplate if you are
looking to use R in any parts of a workflow using Google Cloud Dataflow. The
project structure is an adaptation of the recommended structure of Dataflow/Beam
projects from the Juliaset example https://github.com/apache/beam/tree/master/sdks/python/apache_beam/examples/complete/juliaset

> Credit goes to Greg https://github.com/gregmcinnes for providing an example
of how to get R working using Python. I have slightly adjusted his original
example to give a slightly cleaner implementation and remove the task of using
`pip install rpy2` from the workflow code.

## Dependencies

* apache-beam-sdk (0.6.0.dev0)
* google-cloud-dataflow (0.5.1)

## Notes

* While this is a very basic workflow, it will still take just under 10 mins to
run on Dataflow as the worker has to install both R and any other dependencies.
* We have asked Google Cloud team, if there are any plans to release a Dataflow
image that contains R-base pre-installed.

## Using R

Please refer to the main documentation for rpy2 at https://rpy2.readthedocs.io/en/version_2.8.x/

It seems to be problematic if you try installing R libraries in the custom
commands during setup.py. It works better when you install the libraries
in the actual main code of your workflow.

    import rpy2.robjects as robjects
    from rpy2.robjects.packages import importr

    utils = importr('utils')

    # Install any required R packages
    utils.install_packages('stringr', repos='http://cran.us.r-project.org')

    # Import packages
    stringr = importr('stringr')

For production workflows where there are many dependencies, we may look at other
options like storing the frozen dependencies in Google Cloud Storage.

## Running Workflow

### Environment Setup

    PROJECT=your-google-cloud-project-id
    BUCKET=your-google-cloud-storage-bucket

### Locally

    python dataflow_R_main.py \
      --job_name dataflow-R \
      --runner DirectRunner \
      --output ./tmp/output

### Google Cloud DataFlow

    python dataflow_R_main.py \
      --job_name dataflow-R \
      --project $PROJECT \
      --runner DataflowRunner \
      --setup_file ./setup.py \
      --staging_location gs://$BUCKET/dataflow_R/staging \
      --temp_location gs://$BUCKET/dataflow_R/temp \
      --output gs://$BUCKET/dataflow_R/output \
      --num_workers 1
