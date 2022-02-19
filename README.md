# DELAUNAY: a dataset of abstract art for psychophysical and machine learning research

![Visualization of DELAUNAY dataset.](examples.JPG)

DELAUNAY (Dataset for Experiments on Learning with Abstract and non-figurative art for Neural networks and Artificial intelligence) is named after artists [Sonia](https://en.wikipedia.org/wiki/Sonia_Delaunay) and [Robert Delaunay](https://en.wikipedia.org/wiki/Robert_Delaunay). It is a dataset of images of abstract and non-figurative artworks from 53 different artists. It provides a middle ground between natural images typically used in machine learning research and unnatural, structureless patterns at the opposite side of the spectrum. We believe the unique properties of this dataset make it useful for both machine learning as well as psychophsyics research, for example to investigate the hypothesis that sample efficiency scales inversely with the statistical similarity of samples to natural images for humans but not for DNNs.

### Contents

The dataset comprises 11,503 images from 53 categories, i.e. artists (mean number of images per artist: 217.04; standard deviation: 58.55), along with the associated URLs. These samples are split between a training set of 9202 images and a test set of 2301 images. A random subset of samples illustrating their non-figurative (not representing a natural object) nature and high diversity is shown above.

Images can be downloaded from the website of the Department of Physiology of the University of Bern at the following links:
- [https://physiologie.unibe.ch/supplementals/delaunay_1.zip]( https://physiologie.unibe.ch/supplementals/delaunay_1.zip) : containing the 11,503 images (can be read using the [DataLoader](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader) PyTorch class);
- [https://physiologie.unibe.ch/supplementals/delaunay_test.zip]( https://physiologie.unibe.ch/supplementals/delaunay_test.zip) : training set containing 9202 images;
- [https://physiologie.unibe.ch/supplementals/delaunay_train.zip]( https://physiologie.unibe.ch/supplementals/delaunay_train.zip) : test set containing 2301 images;
- [https://physiologie.unibe.ch/supplementals/URLs.zip]( https://physiologie.unibe.ch/supplementals/URLs.zip) : .csv files containing the URLs of each image in the dataset.

### Citing this data set
Please cite the following paper:

[C. Gontier, J. Jordan, and M. A. Petrovici (2022). DELAUNAY: a dataset of abstract art for psychophysical and machine learning research. arXiv preprint.
](https://arxiv.org/abs/2201.12123)


