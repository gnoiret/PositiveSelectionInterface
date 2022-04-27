# Master 1 Bioinformatics Internship
## Université Claude Bernard Lyon 1

Improvement of an interface for positive selection

# Introduction

This interface was developed to visualize data pertaining to positive selection in genes.
However, it can be used for a broader range of purposes. As long as the data
contains a Newick-formatted tree file, a FASTA alignment file and a results file
organised in columns (with site numbers as the first one), the Python script used to generate
the .XML file used by the interface will work.

# Usage

## Uploading your files

On the homepage, upload your three files on the required fields:

- Newick-formatted tree
- FASTA alignment
- statistical results

![Image formulaire](image.png)

### Other fields

If your data requires specific parameters, you are free to change several options: 

- which column to use for the results
- which value should be given to sites that do not have one in the results file

Once you are done, just click the *Display* button and the visualization will be available.

![Image formulaire](image.png)

## Visualization page

The layout is as follows:

- tree on the left
- results graph and alignment on the right

![Image données](image.png)

Parameters include:

- which sequence type to display (proteic / nucleic)
- upper and lower thresholds
    - if you only want one threshold to display, you may "merge" them by increasing the lower threshold or decreasing the upper threshold

(etc.)
