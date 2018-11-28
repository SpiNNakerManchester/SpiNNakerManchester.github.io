cd spinnaker_tools
source setup
make clean
make || exit $?
cd ../spinn_common
make clean
make || exit $?
make install
cd ../SpiNNMan/c_models/reinjector/
make || exit $?
cd ../../../SpiNNFrontEndCommon/c_common/
cd front_end_common_lib/
make install-clean
cd ..
make clean
make || exit $?
make install
cd ../../SpiNNakerGraphFrontEnd/examples/
make clean
make || exit $?
