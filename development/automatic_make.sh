# This script assumes it is run from the directory holding all github projects in parellel
# sh SupportScripts/automatic_make.sh

cd spinnaker_tools
source $PWD/setup
make clean
make || exit $?
cd ..
cd spinn_common
make clean
make || exit $?
make install
cd ..
cd SpiNNMan/c_models/reinjector/
make clean
make || exit $?
cd ../../..
cd SpiNNFrontEndCommon/c_common/
cd front_end_common_lib/
make install-clean
cd ..
make clean
make || exit $?
make install
cd ../..
cd sPyNNaker/neural_modelling/
make clean
make || exit $?
source $PWD/setup
cd ../../SpiNNakerGraphFrontEnd/spinnaker_graph_front_end/examples/
make clean
make || exit $?
echo "completed"
