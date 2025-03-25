
# Table of Contents

1.  [Code Organization](#orgb2a1825)
2.  [Data organization](#org7f71b08)
3.  [Selecting Proper Data](#orgaca5c67)
    1.  [Exceptional Cases](#orge72bf22)
    2.  [Additional information](#orgbcd42fa)
4.  [Estimation of $\widetilde{K_A}$](#org7b73e07)
5.  [Simulation](#org718c4de)

This documentation should serve as a reference manual for analyzing the data published in the paper (Fredrik Stridfeldt and Hanna Kylhammar and Prattakorn Metem and Vikash Pandey and Vipin Agrawal and Andr{\\'e} G{\\"o}rgens and Doste R Mamand and Oskar Gustafsson and Samir El Andaloussi and Dhrubaditya Mitra and Apurba Dev, 2024).


<a id="orgb2a1825"></a>

# Code Organization

The code is organized in the following manner:

    Code/
        ├─ Documentation/
        │                ├─ Documentation.md
        │                ├─ Documentation.pdf
        ├─ src/
        │     ├─ matlab/
        │     │        ├─code1.md
        │     │        ├─code2.md
        │     ├─ python/
        │     │        ├─code1.py
        │     │        ├─code2.py
        │     ├─ readme.txt
        ├─ .gitignore
        ├─ package.json
        ├─ README.md

The `matlab` folder contains all the matlab subroutines and the `python` folder contains the python codes.


<a id="org7f71b08"></a>

# Data organization

The data for the force-distance curve is expected to be arranged in the following manner.

    Data/
        ├─ SampleType1/
        │            ├─ SampleA/
        │            │         ├─ processed_curves-xx/
        │            │         │                     ├─ force-save-{series}.txt
        │            │         ├─ other-files
        │            ├─ SampleB/
        │            │         ├─ processed_curves-xx/
        ├─ SampleType2/
        │            ├─ SampleA/
        │            │         ├─ processed_curves-xx/
        │            │         │                     ├─ force-save-{series}.txt
        │            │         ├─ other-files
        │            ├─ SampleB/
        │            │         ├─ processed_curves-xx/
        │            │         │                     ├─ force-save-{series}.txt
        │            │         ├─ other-files

The `SampleType1` is the sample type e.g. `Wild-Type`. It can be given any name. An example data structure is the following:

    testdata
      └── WT
          ├── 221216ev6_08nN
          │   ├── after-0.3nN.txt
          │   ├── after-0.5nN.txt
          │   ├── before.txt
          │   └── processed_curves-12.13
          │       ├── force-save-2022.12.16-16.25.37.389.txt
          │       ├── force-save-2022.12.16-16.25.41.855.txt
          │       ├── force-save-2022.12.16-16.25.44.855.txt
          │       ....
          └── 221216ev8_08nN
              └── processed_curves-12.13
                  ├── force-save-2022.12.16-16.25.37.389.txt
                  ├── force-save-2022.12.16-16.25.41.855.txt
                  ....


<a id="orgaca5c67"></a>

# Selecting Proper Data

**This is the most important step.** Don't populate the data folder with unwanted datasets. **Copy only the data which are supposed to be analyzed.** This has to be done visually. Once the experiment on a particular sample is completed, use the jpk-software to convert the data into the csv format. 

To visualize all the force-distance curves recorded in the experiment use the code `visualize.py`. For execution run

    python visualize.py path/to/folder/containing/processed_curves-*/directory

The output window will show all the curves, where the first indentation will be deep-purple and the last yellow, as shown in the figure below

![img](./imgs/testvizualize.png)

Ensure all the criterion listed in the SI of (Fredrik Stridfeldt and Hanna Kylhammar and Prattakorn Metem and Vikash Pandey and Vipin Agrawal and Andr{\\'e} G{\\"o}rgens and Doste R Mamand and Oskar Gustafsson and Samir El Andaloussi and Dhrubaditya Mitra and Apurba Dev, 2024) is obeyed. For example the following experiment data is expected to be deleted

![img](imgs/reject1.png)


<a id="orge72bf22"></a>

## Exceptional Cases

It is possible that only few processed-curve could be erroneous \![see](fig-fewerror). This mainly happens during converting the data to csv using the jpk-software. Here these curves should be removed before copying the data into the expected directory. 

![img](./imgs/removebadguy.png)

To remove the erroneous curve run `visualize-and-delete.py`. The execution is same as before

    python visualize.py path/to/folder/containing/processed_curves-*/directory

The fdc will be plotted sequentially and the unwanted file can be removed by pressing [d]. See the terminal output Figure \![see](term<sub>info</sub>).

![img](imgs/sequencial-removing.png)

Write something on height vs RC


<a id="orgbcd42fa"></a>

## Additional information

All the post-processing data will be generated inside the folder where the `processed-curve*` is stored. In the same folder the metadata for the vesicle is also stored in the filename `vesicle_para.txt`. The content are

    height: 80.0 
    radius: 58.44 
    xmax: 20.0
    shift: 2.0

Height and radius are the height and radius of the membrane. xmax and shift will be explained in the section Simulation. 


<a id="org7b73e07"></a>

# Estimation of $\widetilde{K_A}$

To estimate $\widetilde{K_A}$, use the code `AverageFDCandKA.py`. For execution

    python AverageFDCandKA.py path/to/folder/containing/processed_curves-*/directory/

The output is `KA.txt` with all the KA estimated for individual fdc. The output is dumped
in the directory provided as an input while running the script.

The other output is `AverageFDC.txt` which will store the average FDC.


<a id="org718c4de"></a>

# Simulation

The details of simulation is given in the Supplementary information section 10.B of (Fredrik Stridfeldt and Hanna Kylhammar and Prattakorn Metem and Vikash Pandey and Vipin Agrawal and Andr{\\'e} G{\\"o}rgens and Doste R Mamand and Oskar Gustafsson and Samir El Andaloussi and Dhrubaditya Mitra and Apurba Dev, 2024).

Use the code `Optimize1dMembrane.py`. The output will be a fitted curve and the membrane as \![shown] (fig-fit)
![img](./imgs/Simulation.png)

Additional parameters required to fit are **shift** = The horizontal correction performed on average fdc and **xmax** = The upper bound for the fitting range. The curve will be fitted from [0+shift to xmax].

Fredrik Stridfeldt and Hanna Kylhammar and Prattakorn Metem and Vikash Pandey and Vipin Agrawal and Andr{\\'e} G{\\"o}rgens and Doste R Mamand and Oskar Gustafsson and Samir El Andaloussi and Dhrubaditya Mitra and Apurba Dev (2024). *Surface adhesion and membrane fluctuations influence the elastic modulus of extracellular vesicles*, bioRxiv.

