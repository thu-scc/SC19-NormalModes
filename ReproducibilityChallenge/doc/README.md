# Reproducibility Challenge

## Contents

ReproducibilityChallenge
|-- compile
|   |-- README.md
|   |-- compile.sh                                                                              // Scripts to compile the binary
|   |-- files                                                                                         // Files used to compile the binary
|   \`-- scc19_team13_ExperimentalEnvironment.txt                        // System information
|-- doc
|   |-- README.md
|   \`-- scc19_team13_normalmodes_reproducibility_report.pdf      // Final reproducibility report
|-- figures
|   |-- output                                                                                     // Figures used in the report
|   \`-- scripts                                                                                    // Scripts to generate figures
|-- input                                                                                           // Input data given by SCC committee
\`-- run
    |-- output                                                                                     // Results from the binary
    \`-- scripts                                                                                    // Scripts to run the binary

## Instructions

### Compile

1. Prepare intel compilers, intel mpi and intel mkl.
2. Edit the path for dependences.
3. run [compile.sh](<../compile/compile.sh>) in [compile](../compile) to get the binary.

See [readme](<../compile/README.md>) in `compile` for more information.

### Run & View

We use the same script to run the binary and create figures. The scripts are already in their required place. They can also be found in [run](<../run/scripts>) and [figures](<../figures/scripts>).

Use `python3 tools/cluster_run.py` in [demos](<../compile/files/NormalModes/demos/tools>) to run the script.

The script is actually a simple console. Please specify the hostnames of the cluster before run the console.

It consists the following parts:

1. **switch \<label\>** Switch to the dataset. To run the experiments, switch to `test`, to see the results, switch to `week` and `strong`.
2. **run \<label\>** Run the experiments. Specify the experiment name(`M1-1`, `M2-2`, `M3-1`, `M3-2`, `M3-4`, `M4-1`, `M5-2`, `M6-4`) and input the node list,  for example, `e1,e2,e3,e4` for an experiment using four nodes.
3. **parse \<filename\>** Parse the log and show the key results.
4. **check** Check the status of the dataset. The status may be `NOT STARTED`, `UNFINISHED` or `DONE`.
5. **plot** Create figures and charts of the dataset.
6. **download** Download the logs to the local computer. If the `logs` folder is existed, it will be move to a `Trash` folder.
7. **exit** Exit the console.


## Results





## todo

### compile
1. 把给的模型放到compile文件夹的model/moon里
2. 确定机器配置情况

### run

1. 更新脚本

### figures

1. 放结果，更新readme
2. 更新脚本
3. VTK

### doc

1. final report
2. results in readme