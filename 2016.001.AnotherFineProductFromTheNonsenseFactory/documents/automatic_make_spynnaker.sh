cd spinnaker_tools
source setup
make clean
make || exit $?
cd ..
cd spinn_common
make clean
make || exit $?
make install
cd ..
cd SpiNNMan/c_models/reinjector/
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
source setup
cd sPyNNakerExternalDevicesPlugin/neural_modelling/
make clean
make || exit $?
cd ../../sPyNNakerExtraModelsPlugin/neural_modelling
make clean
make || exit $?
