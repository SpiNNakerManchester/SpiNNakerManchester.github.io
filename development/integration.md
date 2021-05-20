---
title: Integration testing the SpiNNaker software
---
1. [Install requirements](#Requirements)
1. [Integration tests directory](#directory)
1. [Extendied unittest.TestCase](#BaseTestCase)
1. [Testing Scipts](#TestScripts)
1. [Testing example scripts Automatically](#BuildScripts)
1. [global_variables tool to get output](#global_variables)
1. [Reading provenance database](#provenance)

# <a name="Requirements">Requirements</a>

To run interrogation test locally you will need TestBase installed;
[check these instructions](devenv6.0.html).

To add the tests to the Jenkins build the Jenkins files in IntegrationTests may need updating.

The things that could need adding include:
1. Add a `git clone`
2. Add a `make` (especially when using custom C code)
3. Add a `setup.py` call
4. Add a `pip install requirements-test.txt`
5. Add a `stage('Run ..... Integration Tests')`
    - run `script_builder.py` if used
    - run tests

# <a name="directory">Integration tests directory</a>
Ensure one or more integration tests directory exists
1. Directly under the repository root
2. Directory name(s) must end with `_tests`

# <a name="BaseTestCase">BaseTestCase</a>

[BaseTestCase](https://github.com/SpiNNakerManchester/TestBase/blob/main/spinnaker_testbase/base_test_case.py)
is an  extension of `unittest.TestCase` to add extra functionality. Usage:

```python
from spinnaker_testbase import BaseTestCase

class MyTestClass(BaseTestCase):

    def the_script(self):
        _some_test_stuff

    def test_the_script(self):
        self.runsafe(self.the_scipt)
```

1. As [BaseTestCase](https://github.com/SpiNNakerManchester/TestBase/blob/main/spinnaker_testbase/base_test_case.py)
   extends `unittest.TestCase` all assert available there are included.
   You can also use the Python `assert` keyword.
2. The main method is `self.runsafe()`, which:
    - Runs the method given in the parameter
    - Will automatically `cd` into the directory the test is in
        - Therefore picking up any cfg file
        - Allowing for relative paths to supporting files
    - Will reset the simulator state in case a previous test left in unstable.
        - Sorry, it can not push the reset button on a 4 chip board for you.
    - Will try the method a few times if a network type error occurs.
        - The retry is recorded and Jenkins will fail at a later stage
3. Proves a few extra support methods including
    - `assert_logs_messages()`
    - `get_provenance_files()`
    - `get_system_iobuf_files()`
    - `get_app_iobuf_files()`
    - `get_placements()`
    - `report()`

# <a name="TestScripts">Testing example scripts</a>

[ScriptChecker](https://github.com/SpiNNakerManchester/TestBase/blob/main/spinnaker_testbase/script_checker.py)
provides a convenient tool for easily testing a python script.

```python
from spinnaker_testbase import ScriptChecker

class MyTestClass(ScriptChecker):

    def test_learning_simple(self):
        self.check_script("learning/simple.py")
```

- It will convert a relative script path to an absolute one.
    - The relative should be from the repository root
    - Currently only works if the test file is directly under an [Integration tests directory](#directory)
- It will automatically `cd` into the directory the script is in
    - Therefore picking up any cfg file
    - Allowing for relative paths to supporting files
- It will reset the simulator state in case a previous test left in unstable.
    - Sorry, it can not push the reset button on a 4 chip board for you.
- Will try the script a few times if a network type error occurs.
    - The retry is recorded and Jenkins will fail at a later stage
- Keeps a record of how long the script took to standard output and in `TestBase/reports/scripts_ran_successfully`

1. Success criteria
    - The script must have run without error
    - No checking of results is done unless the script contains assert statements
    - As the script is run in its directory any files output by the script will be relative to it
    - For an example that checks the log files [see HelloWorld](https://github.com/SpiNNakerManchester/SpiNNakerGraphFrontEnd/blob/master/gfe_integration_tests/test_hello_world.py)

1. Matplotlib
   - Scripts can safely include plotting to maplotlib
   - Must use the import format: `import matplotlib.pyplot ...`
   - `ScriptChecker` will mock out the show
   - `ScriptChecker` will raise `SkipTest` if the show is not called at least once

1. Data available from `globals_variables` even after the script finished

    `from spinn_front_end_common.utilities.globals_variables import ...`

    - `provenance_file_path()`: The path to the directory that holds all provenance files
    - `app_provenance_file_path()`: The path to the directory that holds all app provenance files
    - `system_provenance_file_path()`: The path to the directory that holds all system provenance files
    - `report_default_directory()`: The path to the directory that holds all the reports for run

# <a name="BuildScripts">Testing example scripts automatically</a>

1. Add a `script_builder.py`
    - Copy in a [script_builder.py](https://github.com/SpiNNakerManchester/PyNN8Examples/blob/master/integration_tests/script_builder.py)
    - Must be directly under the integration tests directory
    - `self.create_test_scripts` takes three parameters
        1. A List of directories to find test scripts in
            - The path should be relative to the repository root
        2. A dictionary of `too_long` files that take a long time to test
            - File name (without path)
            - Time it takes to run
        3. A dictionary of `exceptions` python files that should not run
            - File name (without path)
            - A reason they should not be run
    - `too_long` and `exceptions` may be empty
    - `too_long` files
       - Will add a comment with the time it takes to run
       - Will add a commented out SkipTest so the script can easily be skipped
       - Jenkins can be configured to uncomment the `SkipTest`(s)
       - Jenkins runs several tests in parallel so 4 scripts that each take 5 minutes should run faster than one 10 minute script
    - `exceptions`
        - Class and utility files with no main do not need to be listed as exception.  The test will on these will just be a can they be imported.
        - exceptions scripts will raise a `SkipTest` with the reason given
            - ideally a link to the issue why they don't run or a needs x device

1. To run the tests locally
    - run `script_builder.py`
    - pytest the created `test_scripts.py`

1. To run the tests on Jenkins.
    - `script_builder.py` is run every job so new scripts are automatically found
    - `test_scripts.py` if found in github is ignored/ reference only

# <a name="global_variables">`global_variables` tool to get output</a>
Many [global variables](https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon/blob/master/spinn_front_end_common/utilities/globals_variables.py)
are available even after a end is called or [ScriptChecker.check_script](https://github.com/SpiNNakerManchester/TestBase/blob/main/spinnaker_testbase/script_checker.py)
has returned.

These include:
- `get_generated_output`
- `provenance_file_path`
- `app_provenance_file_path`
- `system_provenance_file_path`
- `report_default_directory`
- `config`

These methods will work from when `setup` is called until the next `setup` or `reset`.
`config` is callable even before `setup` but then will not include any changes done to the configs by the setup call.

# <a name="provenance">Reading provenance database</a>
[ProvenanceReader](https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon/blob/master/spinn_front_end_common/interface/provenance/provenance_reader.py)
provides a tool for reading the provenance database.

The Reader provides a thin wrapper around the provenance database.
As long as the object is created between setup and end/reset the data is available.
(or at least as long as the file is not deleted by later runs)

While the class has methods `get_database_handle` and `run_query` which provide a very flexible way of accessing the data,
their use is not the recommended way of IntegrationTesting.

Ideally add an extra support function directly to [ProvenanceReader](https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon/blob/master/spinn_front_end_common/interface/provenance/provenance_reader.py)
so that it is
1. Easy to find for other tests / scripts to reuse
1. Easier to update if the SQL schema changes
