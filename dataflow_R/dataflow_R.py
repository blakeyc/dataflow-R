from __future__ import absolute_import

import argparse
import logging
import re

import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.utils.pipeline_options import PipelineOptions
from apache_beam.utils.pipeline_options import SetupOptions

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

# Create an instance of R
r = robjects.r
utils = importr('utils')
utils.chooseCRANmirror(ind=1)

# Install any required R packages
utils.install_packages('stringr')

# Import packages
stringr = importr('stringr')

# Example DoFn using the stringr R library
class StringLengthDoFn(beam.DoFn):
  """Determine the length of a string."""
  def process(self, context):
    string = context.element.strip()
    length = stringr.str_length(string)
    yield '%s,%s' % (string, length[0])

def run(argv=None):

    """ Main entry point; defines and runs the pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',
                        dest='output',
                        required=True,
                        help='Output file to write results to.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    """Pipeline Workflow Definition"""
    p = beam.Pipeline(argv=pipeline_args)

    (p
     | 'add_text' >> beam.Create(['Hello World!'])
     | 'string_length' >> beam.ParDo(StringLengthDoFn())
     | 'save' >> beam.io.WriteToText(known_args.output))

    # Run the actual process
    return p.run()
