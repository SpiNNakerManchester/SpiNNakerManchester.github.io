# This script assumes it is run from the directory holding all github projects in parallel
# bash SupportScripts/automatic_make.sh

do_make() {
    if [ -d "$1" ]; then
        # Control will enter here if DIRECTORY exists.
        # Run setup.bash if it exists
        if [ -f "$1/setup.bash" ]; then
            cd $1
            source setup.bash || exit $?
            cd -
        fi
        if [ -f "$1/setup" ]; then
            cd $1
            source setup || exit $?
            cd -
        fi
        # Clean
        make -C $1 clean || exit $?
        # Clean installation; ignore error if install-clean doesn't work
        # (probably because there is no install clean for most targets)
        make -C $1 install-clean || true
        # Make
        make -C $1 || exit $?
        # Install if needed
        if [ "$2" == "install" ]; then
            make -C $1 install || exit $?
        fi
    fi
}

do_make spinnaker_tools
do_make spinn_common install
do_make SpiNNFrontEndCommon/c_common/front_end_common_lib install
do_make SpiNNFrontEndCommon/c_common/ install
do_make sPyNNaker/neural_modelling/
do_make sPyNNaker8NewModelTemplate/c_models/
do_make SpiNNakerGraphFrontEnd/gfe_examples/
do_make SpiNNakerGraphFrontEnd/gfe_integration_tests/
do_make SpiNNGym/c_code