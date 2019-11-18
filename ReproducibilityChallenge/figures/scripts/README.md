# Usage
Use `python3 tools/cluster_run.py` in [demos](<../../compile/files/NormalModes/demos/tools>) to run the script. The scripts there are the same as those of here.

The script is actually a simple console. Please specify the hostnames of the cluster before run the console.

It consists the following parts:

1. **switch \<label\>** Switch to the dataset. To run the experiments, switch to `test`, to see the results, switch to `week` and `strong`.
2. **run \<label\>** Run the experiments. Specify the experiment name(`M1-1`, `M2-2`, `M3-1`, `M3-2`, `M3-4`, `M4-1`, `M5-2`, `M6-4`) and input the node list,  for example, `e1,e2,e3,e4` for an experiment using four nodes.
3. **parse \<filename\>** Parse the log and show the key results.
4. **check** Check the status of the dataset. The status may be `NOT STARTED`, `UNFINISHED` or `DONE`.
5. **plot** Create figures and charts of the dataset.
6. **download** Download the logs to the local computer. If the `logs` folder is existed, it will be move to a `Trash` folder.
7. **exit** Exit the console.

# More Information
The figures are drawn by matplotlib.

The vtk?