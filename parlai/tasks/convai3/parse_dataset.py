## This script parses the ConvAI3 dataset into a ParlAI format.
## The dataset has the following format:
# topic_id	initial_request	topic_desc	clarification_need	facet_id	facet_desc	question_id	question	answer
# 201	I would like to know more about raspberry pi	What is a raspberry pi?	3	F0418	What is a raspberry pi?	Q00365	are you interested in raspberry pi projects	i am looking for information that helps me understand what a raspberry pi is
# 201	I would like to know more about raspberry pi	What is a raspberry pi?	3	F0418	What is a raspberry pi?	Q02981	when was raspberry pi created	what is raspberry pi
# 201	I would like to know more about raspberry pi	What is a raspberry pi?	3	F0418	What is a raspberry pi?	Q03312	would you like to buy raspberry pi computer	no i want to know what raspberry pi is

import os
import sys
import json
import random
import argparse
import numpy as np
from collections import defaultdict
import pandas as pd

from parlai.core.build_data import download_multiprocess, built
from parlai.core.params import ParlaiParser
from parlai.utils.io import PathManager

FOLD = "validation"
FOLD_OUT = "valid"
# FOLD = "train"
# FOLD_OUT = "train"
# FOLD = "test"
# FOLD_OUT = "test"

