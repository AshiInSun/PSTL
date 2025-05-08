# PSTL

**Projet STL - Experimentation between Alias algorithm implemented by unuran and a new one.**

In the repositery, you will find "dau" file. These are the files from the unuran library that implements the Alias Algorithm. Note that it is highly recommended to download the all library, because these files uses methods and structures implemented in the unuran library. You can find the source files of the library here :
https://github.com/scipy/unuran.git
BUT I highly recommend to download the source files here : https://statmath.wu.ac.at/software/unuran/download.html
"Step 2, Download UNURAN (version 1.11.0)" because you'll find some configuration files that are missing in the github.
The file which implements the alias algorithm can be find in the directory src/methods.

You also can find the documentation of unuran here : https://statmath.wu.ac.at/software/unuran/
and the documentation of the Alias Algorithm here : https://statmath.wu.ac.at/software/unuran/doc/unuran.html#DAU in the section "5.8.2 DAU – (Discrete) Alias-Urn method".
Other doc/sources that could be useful :
https://docs.scipy.org/doc/scipy/tutorial/stats/sampling_dau.html
https://experts.illinois.edu/en/publications/an-analysis-of-the-alias-method-for-discrete-random-variate-gener
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.sampling.DiscreteAliasUrn.html

---

## Running the Scripts

This repository provides several Python scripts to test and compare the two Alias algorithms.

---

### 1. `test_alias_integer.py`

Test the custom integer-based Alias method.

#### Usage:

```bash
python test_alias_integer.py [options]
```

#### Options:

- `--mode` : Choose between `manuel` (predefined tests) or `aleatoire` (random tests). Default: `aleatoire`, following options only work in `aleatoire` mode.
- `--tests` : Number of random distributions to perform the tests with. Default: 100
- `--samples` : Number of samples to generate per test. Default: 1000
- `--tol` : Maximum tolerated deviation between expected and observed frequency. Default: 0.1
- `--verbose` : Force output even if the test passes

#### Example:

```bash
python test_alias_integer.py --tests 50 --samples 1000 --tol 0.05 --verbose
```

---

### 2. `test_alias_unuran.py`

Test the Alias implementation provided by the UNURAN library. Same structure and options as above.

#### Usage:

```bash
python test_alias_unuran.py [options]
```

#### Example:

```bash
python test_alias_unuran.py --mode manuel
```

---

### 3. `run_chi2_comparison.py`

Run a statistical chi-squared comparison on both algorithms using a given input distribution. Results are stored as a CSV file in the `output/` directory.

#### Usage:

```bash
python run_chi2_comparison.py <input_distribution.txt>
```

- The input file should contain a list of integer weights (one integer per line).
- The script saves chi² results and p-values to CSV.

#### Example:

```bash
python run_chi2_comparison.py ../../TestSamples/test5.txt
```

---

### 4. `plot_chi2_results.py`

Read the CSV files produced by `run_chi2_comparison.py` and generate a comparative bar chart.

#### Usage:

```bash
python plot_chi2_results.py
```

- Reads all CSV files in the `output/` folder
- Plots a bar chart comparing both algorithms per test case

---

## Authors

- [Rodrigo VILA](https://github.com/rvila94) <r94vila@gmail.com>
- [Timothée MORANDEAU](https://github.com/AshiInSun) <timorandeau@gmail.com>

Supervised by Mehdi NAIMA and Antoine Genitri.
