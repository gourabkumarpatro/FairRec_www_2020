# Two-Sided Fairness for Personalized Recommendations in Two-Sided Platforms
## Running FairRec
```python
python fairrec_algorithm.py google_local_fact.csv 10 0.5
```
There are three arguments here.<br>
* path to csv file with relevance scores (rows: customers, columns: producers)<br>
e.g., google_local_fact.csv
* size of recommendation or _k_<br>
* value of ```tex $\alpha$``` (our producer-side guarantee will be $\alpha$MMS)
## Relevance Scores
You can use the relevance scores estimated in your dataset in csv format (rows: customers, columns: producers) for your application scenario. Alternatively you can test with ours. The relevance scores calculated for the datasets (used in the paper) can be found in the following links in zipped csv format.
* [GL-CUSTOM](https://zenodo.org/record/3675113/files/GL-CUSTOM.csv.zip?download=1) : Custom relevance function on [Google Local ratings data](https://cseweb.ucsd.edu/~jmcauley/datasets.html#google_local).
* [GL-FACT](https://zenodo.org/record/3675113/files/GL-FACT.csv.zip?download=1) : Relevance scores from latent embedding based factorization on [Google Local ratings data](https://cseweb.ucsd.edu/~jmcauley/datasets.html#google_local).
* [LF](https://zenodo.org/record/3675113/files/LF.csv.zip?download=1) : Relevance scores from latent embedding based factorization on [Last.fm data](https://grouplens.org/datasets/hetrec-2011/).
## Citation Information
If you use this repository in your research, please cite the following paper.
* **_FairRec_: Two-Sided Fairness for Personalized Recommendations in Two-Sided Platforms.** <br>
Gourab K Patro, Arpita Biswas, Niloy Ganguly, Krishna P. Gummadi and Abhijnan Chakraborty.<br>
To appear in proceedings of The Web Conference (WWW), Taipei, Taiwan, April 2020. <br>

You can use the following bibtex.<br>
```tex
@inproceedings{patro_FairRec_WWW20,
author = {Patro, Gourab K and Biswas, Arpita and Ganguly, Niloy and Gummadi, Krishna P. and Chakraborty, Abhijnan},
title = {FairRec: Two-Sided Fairness for Personalized Recommendations in Two-Sided Platforms.},
year = {2020},
isbn = {978-1-4503-7023-3/20/04},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3366423.3380196},
doi = {10.1145/3366423.3380196},
booktitle = {The World Wide Web Conference},
pages = {},
numpages = {11},
location = {Taipei, Taiwan},
series = {WWW ’20}
}
```
