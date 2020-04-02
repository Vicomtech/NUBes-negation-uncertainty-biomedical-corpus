########################################################################################################################
# Copyright (c) 2020 Vicomtech (https://www.vicomtech.org)
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
#    - Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#      disclaimer.
#
#    - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#      following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
########################################################################################################################
"""Evaluate NCRF++ predictions against a reference file

Gold standard and prediction files must have NCRF++ format (see examples at https://github.com/jiesutd/NCRFpp). The
results are reported in terms of per-class and per-token precision, recall and F1.

Three evaluation scenarios are offered:
   1. "bin" or "binary": binary classification (i.e., "IN" or "OUT")
   2. "class" or "type": category classification
   3. "full": category and BIO-tag classification
"""
import os
import argparse
import pandas as pd

from enum import Enum
from typing import List
from io import TextIOWrapper

from sklearn.metrics import precision_recall_fscore_support


class Task(Enum):
    """Evaluation scenarios
    """
    binary = 'bin'
    type = 'class'
    full = 'full'

    def __str__(self):
        return self.value


def get_labels(file: List[str], task: Task) -> List[str]:
    """Obtain a list of labels from a file in NCRF++ format

    :param file: the lines of a file in NCRF++ format
    :param task: the evaluation scenario
    :return: the list of labels in the input file (one label per token)
    """
    labels = []
    for line in file:
        line = line.strip()
        if line not in ('', '# 1.0000'):
            label = line.split(' ')[-1]
            if task == Task.binary:
                label = label != 'O'
            elif task == Task.full:
                pass
            else:
                label = label[2:] if len(label) > 2 else label
            labels.append(label)
    return labels


def main(true_file: TextIOWrapper, prediction_files: List[TextIOWrapper], task: Task):
    """Evaluate predictions against a reference file in the given evaluation scenario

    :param true_file: the reference file
    :param prediction_files: a list of predictions files to be evaluated
    :param task: the evaluation scenario
    """
    y_true = get_labels(true_file.readlines(), task)
    labels = list(set(y_true) - {'O', False})
    results = []
    for prediction_file in prediction_files:
        y_pred = get_labels(prediction_file.readlines(), task)
        if len(y_true) == len(y_pred):
            ps, rs, f1s, _ = precision_recall_fscore_support(y_true, y_pred, labels=labels, average=None)
            results.append(list(num for p, r, f in zip(ps, rs, f1s) for num in (p, r, f)))
        else:
            results.append([float('NaN')] * len(labels) * 3)
    index = [prediction_file.name for prediction_file in prediction_files]
    columns = pd.MultiIndex.from_product([labels, ['P', 'R', 'F1']])
    df = pd.DataFrame(results, index=index, columns=columns)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)


if __name__ == '__main__':

    task_help = 'evaluation mode (see above; default: "cat")'
    default_true_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'test.bio')
    true_help = 'path to gold standard file (default: ' + default_true_path + ')'
    pred_help = 'path to predictions file (accepts multiple paths)'

    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__)
    ap.add_argument('--task', type=Task, choices=list(Task), default=Task.type, help=task_help)
    ap.add_argument('--true', metavar='T', type=argparse.FileType('r'), default=default_true_path, help=true_help)
    ap.add_argument('pred', nargs='+', type=argparse.FileType('r'), help=pred_help)
    args = ap.parse_args()

    main(args.true, args.pred, args.task)
