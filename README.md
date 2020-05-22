
# NUBes: A Corpus of Negation and Uncertainty in Spanish Clinical Texts

This repository contains the NUBes corpus and other related material.

**WARNING:** Please note that the repository contains [Git LFS](https://git-lfs.github.com/) files. If you have any
problem cloning these files, please [get in touch](#contact) and we will provide alternative ways to obtain the data.

# Table of Contents

1. [NUBes and IULA+](#nubes-and-iula)
    * [Size and Composition](#size-and-composition)
    * [Data Protection](#data-protection)
    * [Related Publications](#related-publications)
1. [LREC2020](#lrec2020)
    * [Dataset](#dataset)
    * [Training](#training)
    * [Evaluation](#evaluation)
1. [Citation](#citation)
1. [License](#license)
1. [Contact](#contact)


## NUBes and IULA+

The NUBes corpus (from "Negation and Uncertainty annotations in Biomedical texts in Spanish") consists of sentences
obtained from anonymised health records and annotated with negation and uncertainty phenomena. As far as we know, it is
currently the largest publicly available corpus for negation in Spanish and the first that also incorporates the 
annotation of speculation cues, scopes, and events.

IULA+ is a new version of the IULA-SCRC corpus (accessible [here](http://eines.iula.upf.edu/brat/\#/NegationOnCR_IULA)).
More specifically, it consists of the same texts but annotated with NUBes' guidelines.

A couple of interesting remarks:
* The annotation guidelines can be consulted [here](./NUBes-guias-de-anotacion.pdf) (in Spanish).
* NUBes and IULA+ are distributed in [BRAT standoff format](https://brat.nlplab.org/standoff.html).
  
### Size and Composition

* NUBes is divided into 10 samples of approximately 3K sentences each.
* The first sample ([SAMPLE-001](./NUBes/SAMPLE-001)) has been annotated following a process involving 2 annotators and
  a referee, while the rest have been annotated by one person only. In this regard, the first sample can be said to be
  of higher quality.
* The sentences in each sample have been in turn grouped by the medical specialty and report sections to which they 
  belong. So, for instance, the file [`sample-001.traum.chico.txt`](./NUBes/SAMPLE-001/sample-001.traum.chico.txt)
  contains sentences of the specialty "traumatology" and the section "chief complaint".
   
You can consult the sizes of NUBes and IULA+ in the following table:
<table>
    <thead>
    <th></th>
    <th>NUBes</th>
    <th>IULA+</th>
    </thead>
    <tbody>
    <tr>
    <td colspan="3"><b>overall stats</b></td>
    </tr>
    <tr>
    <td>sentences</td>
    <td>29,682</td>
    <td>3,363</td>
    </tr>
    <tr>
    <td>tokens</td>
    <td>518,068</td>
    <td>38,208</td>
    </tr>
    <tr>
    <td>vocabulary size</td>
    <td>31,698</td>
    <td>8,651</td>
    </tr>
    <tr>
    <td colspan="3"><b>negation</b></td>
    </tr>
    <tr>
    <td>sentences affected</td>
    <td>7,567</td>
    <td>1,022<small><sup>*</sup></small></td>
    </tr>
    <tr>
    <td>average cues per affected sentence</td>
    <td>1.25 +/- 0.66</td>
    <td>1.20 +/- 0.59</td>
    </tr>
    <tr>
    <td>discontinuous cues</td>
    <td>0</td>
    <td>0</td>
    </tr>
    <tr>
    <td>average scope size in tokens</td>
    <td>4.01 +/- 3.59</td>
    <td>3.13 +/- 2.67</td>
    </tr>
    <tr>
    <td>discontinuous scopes</td>
    <td>219</td>
    <td>24</td>
    </tr>
    <tr>
    <td colspan="3"><b>uncertainty</b></td>
    </tr>
    <tr>
    <td>sentences affected</td>
    <td>2,219</td>
    <td>178<small><sup>*</sup></small></td>
    </tr>
    <tr>
    <td>average cues per affected sentence</td>
    <td>1.12 +/- 0.38</td>
    <td>1.12 +/- 0.38</td>
    </tr>
    <tr>
    <td>discontinuous cues</td>
    <td>95</td>
    <td>20</td>
    </tr>
    <tr>
    <td>average scope size in tokens</td>
    <td>5.27 +/- 4.97</td>
    <td>4.75 +/- 3.96</td>
    </tr>
    <tr>
    <td>discontinuous scopes</td>
    <td>123</td>
    <td>7</td>
    </tr>
    </tbody>
</table>

<small><sup>*</sup> These numbers do not match those in the paper's Table 1; the correct counts are shown here.</small>

### Data Protection

All sensitive information (e.g., people names, healthcare facilities, dates, and so on) in NUBes have been subsituted
with fake similar data. Furthermore, the sentences have been shuffled in order to hinder de-anonymization efforts as
much as possible. That is, subsequent sentences in the corpus provided most likely did not occur together in the
original health records. What is more, sentences that belong to the same health record are scattered across different
samples. 

### Related Publications

To know more about NUBes, read our article "NUBes: A Corpus of Negation and Uncertainty in Spanish Clinical Texts"
[[pdf](http://www.lrec-conf.org/proceedings/lrec2020/pdf/2020.lrec-1.708.pdf)].

To know more about IULA-SCRC, read the article "Annotation of negation in the IULA Spanish Clinical Record
Corpus" by Montserrat Marimon, Jorge Vivaldi and Núria Bel [[pdf](https://www.aclweb.org/anthology/W17-1807.pdf)].

Please see Section [Citation](#citation) to learn how to cite these works.

## LREC2020

This directory contains material and scripts related to the experiments section in the paper "NUBes: A Corpus of 
Negation and Uncertainty in Spanish Clinical Texts" (see above).

### Dataset

#### [`data/`](./LREC2020/data)

Here you will find the dataset splits —train, development and test— used in the experiments. Specifically, the files 
provided contain the full set of features described in the paper. Use the script [`ablation.py`](./LREC2020/ablation.py), 
explained below, to obtain the files to conduct the ablation study.

**WARNING:** Please note that this dataset is stored with [Git LFS](https://git-lfs.github.com/). If you have any
problem cloning these files, please [get in touch](#contact) and we will provide alternative ways to obtain the data.

#### [`ablation.py`](./LREC2020/ablation.py)

| Python version | Dependencies                         |
| -------------- | ------------------------------------ |
| \>= Python3.5  | [pandas](https://pandas.pydata.org/) |

This script generates the files necessary to perform the ablation study described in the paper.
For each data split, it will generate 6 new files, each with a different group of features left out.
For instance, from the file [`data/train.bio`](./LREC2020/data/train.bio), it will create:
* `data/train.abl-form.bio`
* `data/train.abl-morphsyn.bio`
* `data/train.abl-brown.bio`
* `data/train.abl-metadata.bio`
* `data/train.abl-window.bio`
* `data/train.token.bio`

The last file does not contain any feature apart from the tokens themselves.

Optionally, you may indicate input and output paths, as well as the number of parallel processes to be launched:

```text
usage: python3 ablation.py [-h] [-i I] [-o O] [-p P]

optional arguments:
  -h, --help           show this help message and exit
  -i I, --input I      path to directory containing the dataset (default: data)
  -o O, --output O     path to output directory (default: data)
  -p P, --processes P  number of parallel processes (default: cpu_count()//2)
```

The following command should work out of the box:
```shell script
python3 ablation.py
```

### Training

#### [`train.config`](./LREC2020/train.config) 

This is the NCRF++ configuration file we used for training the models described in the paper. This configuration file
specifies the neural network's architecture and hyperparamters. Read about how to install NCRF++ and how to train models
and use them for decoding at https://github.com/jiesutd/NCRFpp.

**NOTE**: you must change the I/O section in the file so that
1. it points to your dataset files (parameters `train_dir`, `dev_dir` and `test_dir`)
2. it writes the resulting models to the desired folder and with the desired name (parameter `model_dir`)

```text
### I/O ###
train_dir=/PATH/TO/train.bio
dev_dir=/PATH/TO/dev.bio
test_dir=/PATH/TO/test.bio
model_dir=/PATH/TO/<MODEL NAME>
```

### Evaluation

#### [`eval.py`](./LREC2020/eval.py)

| Python version | Dependencies                                                                                |
| -------------- | ------------------------------------------------------------------------------------------- |
| \>= Python3.5  | [sklearn](https://scikit-learn.org/stable/index.html), [pandas](https://pandas.pydata.org/) |

This is the script we used to obtain the results reported in the article.

It offers 3 evaluation scenarios:
   1. "bin" or "binary": binary classification (i.e., "IN" or "OUT")
   2. "class" or "type": category classification
   3. "full": category and BIO-tag classification
   
The results reported in the paper correspond to the category classification scenario.

The usage of the script is as follows:
```text
usage: python3 eval.py [-h] [--task {bin,class,full}] [--true T] pred [pred ...]

positional arguments:
  pred                  path to predictions file (accepts multiple paths)

optional arguments:
  -h, --help            show this help message and exit
  --task {bin,class,full}
                        evaluation mode (see above; default: "cat")
  --true T              path to gold standard file (default: data/test.bio)
```

Once you have trained your own model(s) and decoded the test set, you may evaluate the results simply by doing:

```shell script
python3 eval.py /PATH/TO/PREDICTION-1 /PATH/TO/PREDICTION-2 /PATH/TO/PREDICTION-3
```

If you do:

```shell script
python3 eval.py data/test.bio
```

you should obtain perfect results (because you will be evaluating the gold labels against themselves).

## Citation

If you use NUBes, IULA+ or any of the provided material in your publications, please cite us appropriately:

```bibtex
@inproceedings{lima2020nubes,
  author      = {Salvador Lima Lopez and Naiara Perez and Montse Cuadros and German Rigau},
  title       = "{NUBes: A Corpus of Negation and Uncertainty in Spanish Clinical Texts}",
  booktitle   = {Proceedings of The 12th Language Resources and Evaluation Conference (LREC2020)},
  month       = {May},
  year        = {2020},
  address     = {Marseille, France},
  publisher   = {European Language Resources Association},
  pages       = {5772--5781}
}

```

If you use IULA+, please cite also the paper describing the original corpus, IULA-SCRC:

```bibtex
@inproceedings{marimon2017annotation,
  author      = {Montserrat Marimon and Jorge Vivaldi and N{\'u}ria Bel Rafecas},
  title       = "{Annotation of negation in the IULA Spanish Clinical Record Corpus}",
  booktitle   = {Proceedings of the Workshop Computational Semantics Beyond Events and Roles (SemBEaR)},
  month       = {Apr},
  year        = {2017},
  address     = {Valencia, Spain},
  publisher   = {Association for Computational Linguistics},
  pages       = {43--52}
}
```

## License

The resources [NUBes](./NUBes), [IULA+](./IULA+), [NUBes experiment splits](./LREC2020/data) and [NUBes annotation
guidelines](./NUBes-guias-de-anotacion.pdf) are licensed under the Creative Commons Attribution-ShareAlike 3.0 Spain 
License. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/es/ or send a letter to 
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

The scripts [ablation.py](./LREC2020/ablation.py) and [eval.py](./LREC2020/eval.py) are copyright of Vicomtech --
(c) 2020 Vicomtech. Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following
  disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
  following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Contact

If you have any question or suggestion, do not hesitate to contact us at the following addresses:

* Naiara Perez: nperez@vicomtech.org
* Salvador Lima: slima@vicomtech.org
* Montse Cuadros: mcuadros@vicomtech.org
* German Rigau: german.rigau@ehu.eus
