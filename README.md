# Master 1 Bioinformatics Internship
## Université Claude Bernard Lyon 1

Improvement of an interface for positive selection

# Introduction

This interface was developed to visualize data pertaining to positive selection in genes.
However, it can be used for a broader range of purposes. As long as the data
contains a Newick-formatted tree file, a FASTA alignment file and a results file
organised in columns (with site numbers as the first one), the Python script used to generate
the XML file used by the interface will work.

# Usage

## Uploading your files

On the homepage, upload your three files on the required fields:

- Newick-formatted tree
- FASTA alignment
- Statistical results

![Image formulaire](image.png)

### Other fields

If your data requires specific parameters, you are free to change several options:

- A toggle to choose whether your sequences should be treated as nucleotidic (and translated 
into proteins) or not

- A toggle for the logarithmic transformation of branch lengths (can be useful 
to create space in the tree if some branches are really short)

- Which column to use for the results (site mode)

Once you are done, just click the *Display* button and the visualization will be available.

![Image formulaire](image.png)

## Visualization page

The layout is as follows:

- Tree on the left
- Results histogram and alignment on the right

![Image données](image.png)

Parameters include:

- Which sequence type to display (amino acids / nucleotides)

- Upper and lower thresholds
    - All computations are currently based on the upper threshold

- In branch-site mode, boundaries used to compute branch colors
    - "Automatic boundaries" updates them when the alignment is scrolled
    - "Reset boundaries" replaces the current values to account for the whole sequence
