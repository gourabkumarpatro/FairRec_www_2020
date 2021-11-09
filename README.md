# Towards Fair Recommendation in Two-Sided Platforms
## Running FairRec or FairRecPlus
```python
python FairRec.py google_local_fact.csv 10 0.5
python FairRecPlus.py google_local_fact.csv 10 0.5
```
There are three arguments here.<br>
* path to csv file with relevance scores (rows: customers, columns: producers) like _google_local_fact.csv_ above. <br>
* size of recommendation or _k_ like _10_ above. <br>
* value of α (our producer-side guarantee will be α×MMS. The value of α can be in between 0 and 1) like _0.5_ above.

It saves the recommendations in zipped pickle file (dictionary format { customer : list_of_recommended_products }).
  
## Relevance Scores
You can use the relevance scores estimated in your dataset in csv format (rows: customers, columns: producers) for your application scenario. Alternatively you can test with ours. The relevance scores calculated for the datasets (used in the paper) can be found in the following links in zipped csv format.
* [GL-CUSTOM](https://zenodo.org/record/3675113/files/GL-CUSTOM.csv.zip?download=1) : Custom relevance function on [Google Local ratings data](https://cseweb.ucsd.edu/~jmcauley/datasets.html#google_local).
* [GL-FACT](https://zenodo.org/record/3675113/files/GL-FACT.csv.zip?download=1) : Relevance scores from latent embedding based factorization on [Google Local ratings data](https://cseweb.ucsd.edu/~jmcauley/datasets.html#google_local).
* [LF](https://zenodo.org/record/3675113/files/LF.csv.zip?download=1) : Relevance scores from latent embedding based factorization on [Last.fm data](https://grouplens.org/datasets/hetrec-2011/).
## Citation Information
If you use this repository in your research, please cite the following paper.
* [**_FairRec_: Two-Sided Fairness for Personalized Recommendations in Two-Sided Platforms.**](https://arxiv.org/abs/2002.10764) <br>
Gourab K Patro, Arpita Biswas, Niloy Ganguly, Krishna P. Gummadi and Abhijnan Chakraborty.<br>
In proceedings of The Web Conference (WWW), Taipei, Taiwan, April 2020. <br>

You can use the following bibtex.<br>
```tex
@inproceedings{10.1145/3366423.3380196,
author = {Patro, Gourab K and Biswas, Arpita and Ganguly, Niloy and Gummadi, Krishna P. and Chakraborty, Abhijnan},
title = {FairRec: Two-Sided Fairness for Personalized Recommendations in Two-Sided Platforms},
year = {2020},
isbn = {9781450370233},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3366423.3380196},
doi = {10.1145/3366423.3380196},
booktitle = {Proceedings of The Web Conference 2020},
pages = {1194–1204},
numpages = {11},
keywords = {Fair Allocation, Fair Recommendation, Maximin Share, Two-Sided Markets, Envy-Freeness},
location = {Taipei, Taiwan},
series = {WWW ’20}
}
```
