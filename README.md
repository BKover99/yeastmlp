# yeastmlp
Python package for analysing MLP-formation

# On pypi
https://pypi.org/project/yeastmlp/

## Two modules:
### Adhesion
Allows the quantification of yeast surface adhesion to agar. Our high-throughput assays take advantage of the RoToR (Singer) instrument to pin out yeast in a 96-well arrangement of squares. After growth, each agar plate is imaged, washed, and imaged again. Comparison of cell density before and after wash in each square allows the quantification of adhesion.

### Flocculation
Allows the quantification of yeast flocculation. Our high-throughput assays take advantage of the RoToR (Singer) instrument to pin out yeast in a 96-well arrangement of squares. After growth, liquid culture plates are placed in a plate-reader that is capable of multiple measurements of optical density per well. The coefficient of variation (std/mean) in each well is our measurement for flocculation.

### Examples
To have a feel for how the software works, see the attached Jupyter Notebooks, which you can run in Google Colab.


### Goals

- [x] Releasing early version of repo, and the package on pypi - Jun 16, 2023
- [x] Finalising code - Aug 31, 2023
- [x] Upload pre-print - Dec 15, 2023  https://www.biorxiv.org/content/10.1101/2023.12.15.571870v1.article-info
- [ ] Publication of peer-reviewed research article
