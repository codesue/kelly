"""
The dataset loading script for the codesue/kelly dataset.
"""

import csv

import datasets

_CITATION = """\
@article{Kilgarriff2013,
doi = {10.1007/s10579-013-9251-2},
url = {https://doi.org/10.1007/s10579-013-9251-2},
year = {2013},
month = sep,
publisher = {Springer Science and Business Media {LLC}},
volume = {48},
number = {1},
pages = {121--163},
author = {Adam Kilgarriff and Frieda Charalabopoulou and Maria Gavrilidou and Janne Bondi Johannessen and Saussan Khalil and Sofie Johansson Kokkinakis and Robert Lew and Serge Sharoff and Ravikiran Vadlapudi and Elena Volodina},
title = {Corpus-based vocabulary lists for language learners for nine languages},
journal = {Language Resources and Evaluation}
}
"""

_DESCRIPTION = """\
The Swedish Kelly list is a freely available frequency-based vocabulary list \
that comprises general-purpose language of modern Swedish. The list was \
generated from a large web-acquired corpus (SweWAC) of 114 million words \
dating from the 2010s. It is adapted to the needs of language learners \
and contains 8,425 most frequent lemmas that cover 80% of SweWAC.
"""

_HOMEPAGE = "https://spraakbanken.gu.se/en/resources/kelly"

_LICENSE = "CC BY 4.0"

_URLS = {
    "csv": "sv.csv",
}


class Kelly(datasets.GeneratorBasedBuilder):
  """Kelly: Keywords for Language Learning for Young and adults alike"""

  VERSION = datasets.Version("1.0.0")

  def _info(self):
    features = datasets.Features(
      {
        "id": datasets.Value("string"),
        "raw_frequency": datasets.Value("float64"),
        "relative_frequency": datasets.Value("float64"),
        "cefr_level": datasets.Value("string"),
        "source": datasets.Value("string"),
        "marker": datasets.Value("string"),
        "lemma": datasets.Value("string"),
        "class": datasets.Value("string"),
        "examples": datasets.Value("string"),
      }
    )

    return datasets.DatasetInfo(
      description=_DESCRIPTION,
      features=features,
      homepage=_HOMEPAGE,
      license=_LICENSE,
      citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    data_path = dl_manager.download_and_extract(_URLS["csv"])
    return [
      datasets.SplitGenerator(
        name=datasets.Split.TRAIN,
        gen_kwargs={
          "filepath": data_path,
        },
      ),
    ]

  def _generate_examples(self, filepath):
    """Generate text2log dataset examples."""
    with open(filepath, encoding="utf-8") as csv_file:
      csv_reader = csv.reader(
        csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
      )
      next(csv_reader)
      for key, row in enumerate(csv_reader):
        a, b, c, d, e, f, g, h, i = row
        yield key, {
          "id": a,
          "raw_frequency": b or "-1",
          "relative_frequency": c or "-1",
          "cefr_level": d,
          "source": e,
          "marker": f,
          "lemma": g,
          "class": h,
          "examples": i,
        }
