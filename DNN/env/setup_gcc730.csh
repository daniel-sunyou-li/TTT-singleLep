
source /cvmfs/sft.cern.ch/lcg/releases/binutils/2.28-a983d/x86_64-centos7/setup.csh

set BASE=/cvmfs/sft.cern.ch/lcg/releases/gcc/7.3.0-cb1ee/x86_64-centos7

setenv PATH $BASE/bin:$PATH

if (${?MANPATH}) then
    setenv MANPATH $BASE/share/man:$MANPATH
else
    setenv MANPATH $BASE/share/man
endif

if ( -d "${BASE}/lib64" ) then
    setenv LD_LIBRARY_PATH "$BASE/lib64:${LD_LIBRARY_PATH}"
endif
if ( -d "${BASE}/lib" ) then
    # Add lib if exists
    setenv LD_LIBRARY_PATH "$BASE/lib:${LD_LIBRARY_PATH}"
endif

# Export package specific environmental variables

set gcc_home=/cvmfs/sft.cern.ch/lcg/releases/gcc/7.3.0-cb1ee/x86_64-centos7 

setenv FC `which gfortran`
setenv CC `which gcc`
setenv CXX `which g++`

setenv COMPILER_PATH ${gcc_home}

