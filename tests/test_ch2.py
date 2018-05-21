#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils import dir_util
from os.path import isdir, splitext
from pytest import fixture #, approx, raises
import jeppson.ch2 as jch2

__author__ = "Bob Apthorpe"
__copyright__ = "Bob Apthorpe"
__license__ = "mit"


# we reuse a bit of pytest's own testing machinery, this should eventually come
# from a separatedly installable pytest-cli plugin. 
pytest_plugins = ["pytester"]
_APPNAME = 'jeppson_ch2'

@fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.

    Shamelessly purloined from https://stackoverflow.com/questions/29627341/pytest-where-to-store-expected-data
    and mangled until it worked right
    '''
    filename = request.module.__file__
    test_dir, _ = splitext(filename)

    if isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir

@fixture
def run(testdir):
    def do_run(*args):
        args = [_APPNAME] + list(args)
        return testdir._run(*args)
    return do_run

def test_ch2(datadir, run):
# Set up input, output, and reference data file paths
    bfn = [
        "ch2_test10",
        "ch2_test11",
        "ch2_test20",
        "ch2_test21",
        "ch2_test_all"
    ]

    for basefn in bfn:

        ifn = datadir.join("{:s}.inp".format(basefn))
#        ofn = datadir.join("{:s}.out".format(basefn))
        rfn = datadir.join("{:s}.ref.out".format(basefn))

# Run ch2.py and check for successful termination
        result = run('--legacy', '--no-modern', ifn)
        assert result.ret == 0

# Compare code output with reference output
#        with ofn.open("r") as ofh:
#            outcontent = ofh.read()
        outcontent = result.outlines

        with rfn.open("r") as rfh:
            refcontent = rfh.read().splitlines()

        nout = len(refcontent)
        assert len(outcontent) == nout

        if len(outcontent) == nout:
            for i, outln in enumerate(outcontent):
                assert outln == refcontent[i]

    return

# extract_case_input(iline, force_units=None):
# calculate_headloss(vol_flow, flow_area, lpipe, idiameter, eroughness,
# generate_results(kwinput):
# generate_legacy_output(idata, odata, units):
