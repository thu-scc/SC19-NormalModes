import os
def run(cmd):
    os.system("clush -w e1,e2 {}".format(cmd))

def get_env():
    print("------------------------------HARDWARE------------------------------------------")
    print("[Server]")
    run('sudo dmidecode -t system | grep -A2 "System Information"')
    print("[Processor]")
    run("lscpu | grep -E 'Model name|Socket'")
    print("[Memory]")
    run('sudo dmidecode -t memory | grep -v -E "No|Unknown|Detail"| grep -E "Size|Type|Clock Speed|Error"')
    print("[Network]")
    run('''sudo ifconfig | grep flags | grep -v "lo" |  cut -d ":" -f 1,2 | awk '{print("echo "$1$2"&& sudo ethtool "$2 "| grep -i speed")}' | sh   ''')
    print("[Accelerator]")
    run("nvidia-smi -L")
    print("\n----------------------------SOFTWARE------------------------------------------")
    print("[OS]")
    run("lsb_release -d")
    print("[Linux Kernel]")
    run("uname -v")
    print("[Compilers & Libraries from Spack]")
    os.system("/usr/bin/modulecmd sh 'list'")
    print("[Libraries Compiled by Ourselves]")
    print("parmetis(Width modified):")
    os.system("cd $HOME/SC19 && ls -d -l */ | grep parmetis | awk '{print($9)}'")
    print("pEVSL:")
    os.system("cd $HOME/SC19/pEVSL && git log -n 1 | head -n 1") 
    print("\n----------------------------EXPERIMENT----------------------------------------")
    print("[Dataset]")
    print("TODO")
    print("[NormalModes]")
    os.system("cd $HOME/SC19/NormalModes && git log -n 1 | head -n 1")

   
    


if __name__ == "__main__":
    get_env()
