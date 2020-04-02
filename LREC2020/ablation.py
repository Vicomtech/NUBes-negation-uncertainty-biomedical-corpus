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
"""Generate data files for the ablation study

The data splits distributed with this code —"data/train.bmes", "data/dev.bmes" and "data/test.bmes"— contain the
complete set of features used in the experiments reported in the NUBes paper. This script generates the files to
perform the ablation study described in the paper.
"""
import os
import argparse

import pandas as pd

from csv import QUOTE_NONE
from multiprocessing import cpu_count, Pool


def ablate(df: pd.DataFrame, filter_rx: str, output_path: str):
    """Filter out the group of features that match the regular expression and write the result

    :param df: the DataFrame object containing the original features
    :param filter_rx: the regular expression of features that should be filtered out
    :param output_path: the path to write the results to
    :return:
    """
    ablated_df = df.drop(list(df.filter(regex=filter_rx)), axis=1)
    ablated_df.to_csv(output_path, sep=' ', quoting=QUOTE_NONE, header=None, index=None)
    print(output_path)


def main(input_dir: str, output_dir: str, process_num: int):
    """Generate data files for the ablation study

    :param input_dir: to directory containing the dataset
    :param output_dir: path to output directory
    :param process_num: number of parallel processes
    """

    # these are the groups of features discussed in the paper
    feature_groups = {
        'form': r'aff|ispunct|isalpha|isnum',
        'morphsyn': r'lemma|pos|dep|right|left',
        'brown': r'brown',
        'metadata': r'spec|sect',
        'window': r'win'
    }
    all_feats_rx = r'|'.join(feature_groups.values())

    # get column names from one of the files
    # warning: this script depends entirely on the features being ordered and on all tokens containing all the features
    #          (which they should for NCRF++)
    with open(os.path.join(input_dir, 'dev.bio')) as rf:
        first_line = rf.readline()
    _, *feats, _ = first_line.split(' ')
    columns = ['token', *[feat.split(']')[0][1:] for feat in feats], 'label']

    tasks = []

    for split in ('train', 'dev', 'test'):
        # read original files (full set of features)
        full_path = os.path.join(input_dir, split + '.bio')
        print('Reading from', full_path, '...', end=' ', flush=True)
        df = pd.read_csv(full_path, sep=' ', quoting=QUOTE_NONE, header=None, skip_blank_lines=False, engine='python')
        df.columns = columns
        print('Done')
        # ablate feature group
        for feats_group_name, feats_group_rx in feature_groups.items():
            ablation_path = os.path.join(output_dir, split + '.abl-' + feats_group_name + '.bio')
            tasks.append((df, r'(^|\b)(' + feats_group_rx + r')($|\b)', ablation_path))
        # ablate all features (keep tokens only)
        tokens_path = os.path.join(output_dir, split + '.token.bio')
        tasks.append((df, r'(^|\b)(' + all_feats_rx + r')($|\b)', tokens_path))

    print('Launching', process_num, 'processes...')
    with Pool(processes=process_num) as pool:
        pool.starmap(ablate, tasks)
    print('Done')


if __name__ == '__main__':

    default_data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
    input_help = 'path to directory containing the dataset (default: ' + default_data_path + ')'
    output_help = 'path to output directory (default: ' + default_data_path + ')'
    process_n = cpu_count() // 2
    processes_help = 'number of parallel processes (default: ' + str(process_n) + ')'

    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__)
    ap.add_argument('-i', '--input', metavar='I', help=input_help, default=default_data_path)
    ap.add_argument('-o', '--output', metavar='O', help=output_help, default=default_data_path)
    ap.add_argument('-p', '--processes', metavar='P', type=int, help=processes_help, default=process_n)
    args = ap.parse_args()

    main(args.input, args.output, args.processes)
