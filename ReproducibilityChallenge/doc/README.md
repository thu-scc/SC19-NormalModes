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

We use the same scripts for running the binary and creating figures. The scripts are already in their required place. They can also be found in [run](<../run/scripts>) and [figures](<../figures/scripts>).

The script is actually a simple console. Please config the experiments and specify the hostnames of the cluster before run the console.



## Results





## todo

### input

把主办方给的数据放进去

### compile
1. 把给的模型放到compile文件夹的model/moon里
2. 确定机器配置情况

### run

1. 更新脚本
2. 