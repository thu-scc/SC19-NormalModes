cd files

# compile parmetis
cd parmetis-4.0.3
make config; make
cd ..

# compile pEVSL
cd pEVSL
make
cd ..

# compile NormalModes
cd NormalModes/src
make
cd ..