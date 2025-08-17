
# Table of Contents



1.  [Code Organization](#org2e47c69)
2.  [Data organization](#org369577e)
3.  [JPK-software (convert jpk to csv)](#org6ce746c)
4.  [Selecting Proper Data](#org8064afb)
    1.  [Exceptional Cases](#org10b36fe)
    2.  [Additional information](#orgfb0c237)
5.  [Estimation of $\widetilde{K_A}$](#orge49e192)
6.  [Violin Plot and Distribution](#org6922fac)
7.  [Simulation](#org57d796a)

This documentation should serve as a reference manual for analyzing the data published in the paper (??, ????).

<a id="org2e47c69"></a>

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

The \`matlab\` folder contains all the matlab subroutines and the \`python\` folder contains the python codes.

<a id="org369577e"></a>

The data for the force-distance curve is expected to be arranged in the following manner.

Data/
    ├─ SampleType1/
    │            ├─ SampleA/
    │            │         ├─ processed<sub>curves</sub>-xx/
    │            │         │                     ├─ force-save-{series}.txt
    │            │         ├─ other-files
    │            ├─ SampleB/
    │            │         ├─ processed<sub>curves</sub>-xx/
    ├─ SampleType2/
    │            ├─ SampleA/
    │            │         ├─ processed<sub>curves</sub>-xx/
    │            │         │                     ├─ force-save-{series}.txt
    │            │         ├─ other-files
    │            ├─ SampleB/
    │            │         ├─ processed<sub>curves</sub>-xx/
    │            │         │                     ├─ force-save-{series}.txt
    │            │         ├─ other-files

The \`SampleType1\` is the sample type e.g. \`Wild-Type\`. It can be given any name. An example data structure is the following:

testdata
  └── WT
      ├── 221216ev6<sub>08nN</sub>
      │   ├── after-0.3nN.txt
      │   ├── after-0.5nN.txt
      │   ├── before.txt
      │   └── processed<sub>curves</sub>-12.13
      │       ├── force-save-2022.12.16-16.25.37.389.txt
      │       ├── force-save-2022.12.16-16.25.41.855.txt
      │       ├── force-save-2022.12.16-16.25.44.855.txt
      │       &hellip;.
      └── 221216ev8<sub>08nN</sub>
          └── processed<sub>curves</sub>-12.13
              ├── force-save-2022.12.16-16.25.37.389.txt
              ├── force-save-2022.12.16-16.25.41.855.txt
              &hellip;.

<a id="org6ce746c"></a>

It is essential to convert the data which is in \`.jpk\` to human readable \`.csv\` form before performing any analysis. Although the software build for the analysis by the provider can be used to some of the analysis we perform, we do this for greater flexibility. The steps followed are as follows:

-   Open the software
-   Select open batch of spectroscopy data
-   Go to the folder and select load
-   Apply three operators (highlighted on top) viz: correct offset and tilt, fit slope and correct for zero, and correct for bending of tip. The symbols for the same are circled with red.
-   In the correct offset and tilt select the necessary operation on the right.
-   We generally discard the first data curve.
-   Apply the operation to all the curves
-   Once finished export the data. Use the naming convention as discussed above. See pictures below for more clarity.
    
    <table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">

<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-left">&nbsp;</td>
<td class="org-left">&nbsp;</td>
</tr>

<tr>
<td class="org-left"><img src="imgs/openjpk.png" alt="openjpk.png" /></td>
<td class="org-left"><img src="imgs/jpk1st.png" alt="jpk1st.png" /></td>
</tr>

<tr>
<td class="org-left"><img src="imgs/jpk6th.png" alt="jpk6th.png" /></td>
<td class="org-left"><img src="imgs/jpk7th.png" alt="jpk7th.png" /></td>
</tr>

<tr>
<td class="org-left">&nbsp;</td>
<td class="org-left">&nbsp;</td>
</tr>
</tbody>
</table>

<a id="org8064afb"></a>

****This is the most important step.**** Don't populate the data folder with unwanted datasets. ****Copy only the data which are supposed to be analyzed.**** This has to be done visually. Once the experiment on a particular sample is completed, use the jpk-software to convert the data into the csv format. 

To visualize all the force-distance curves recorded in the experiment use the code \`visualize.py\`. For execution run

python visualize.py path/to/folder/containing/processed<sub>curves</sub>-\*/directory

The output window will show all the curves, where the first indentation will be deep-purple and the last yellow, as shown in the figure below

\![img](./imgs/testvizualize.png)

Ensure all the criterion listed in the SI of (??, ) is obeyed. For example the following experiment data is expected to be deleted

\![img](imgs/reject1.png)

<a id="org10b36fe"></a>

\## Exceptional Cases

It is possible that only few processed-curve could be erroneous \\\![see](fig-fewerror). This mainly happens during converting the data to csv using the jpk-software. Here these curves should be removed before copying the data into the expected directory. 

\![img](./imgs/removebadguy.png)

To remove the erroneous curve run \`visualize-and-delete.py\`. The execution is same as before

python visualize.py path/to/folder/containing/processed<sub>curves</sub>-\*/directory

The fdc will be plotted sequentially and the unwanted file can be removed by pressing [d]. See the terminal output Figure \\\![see](term<sub>info</sub>).

\![img](imgs/sequencial-removing.png)

Write something on height vs RC

<a id="orgfb0c237"></a>

\## Additional information

All the post-processing data will be generated inside the folder where the \`processed-curve\*\` is stored. In the same folder the metadata for the vesicle is also stored in the filename \`vesicle<sub>para.txt</sub>\`. The content are

height: 80.0 
radius: 58.44 
xmax: 20.0
shift: 2.0

Height and radius are the height and radius of the membrane. xmax and shift will be explained in the section Simulation. 

<a id="orge49e192"></a>

To estimate $\widetilde{K_A}$, use the code \`AverageFDCandKA.py\`. For execution

python AverageFDCandKA.py path/to/folder/containing/processed<sub>curves</sub>-\*/directory/

The output is \`KA.txt\` with all the KA estimated for individual fdc. The output is dumped
in the directory provided as an input while running the script.

The other output is \`AverageFDC.txt\` which will store the average FDC.

<a id="org6922fac"></a>

We present the data using violin plots. After estimating the mean of all the physical quantity of interest we store them in .xlsx file. A representative is given inside Distribution folder. The code inside the folder (\`ViolinPlot.py KApdfWT.py\`) can be used to make representative figures as shown below. A sample JS divergence is also given in \`KApdfWT.py\`

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">

<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-left">&nbsp;</td>
<td class="org-left">&nbsp;</td>
</tr>

<tr>
<td class="org-left"><img src="./imgs/example<sub>voilin</sub><sub>plot.png</sub>" alt="example<sub>voilin</sub><sub>plot.png</sub>" /></td>
<td class="org-left"><img src="imgs/example<sub>KApdfWT.png</sub>" alt="example<sub>KApdfWT.png</sub>" /></td>
</tr>

<tr>
<td class="org-left">&nbsp;</td>
<td class="org-left">&nbsp;</td>
</tr>
</tbody>
</table>

****Note****: The code for the estimation of $\kappa$ is not provided now. 

<a id="org57d796a"></a>

The details of simulation is given in the Supplementary information section 10.B of (??, ).

Use the code \`Optimize1dMembrane.py\`. The output will be a fitted curve and the membrane as \\\![shown](fig-fit)
\![img](./imgs/Simulation.png)

Additional parameters required to fit are ****shift**** = The horizontal correction performed on average fdc and ****xmax**** = The upper bound for the fitting range. The curve will be fitted from [0+shift to xmax].

