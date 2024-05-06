### build instructions
```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_19_patch2
cd CMSSW_10_6_19_patch2/src
cmsenv
git clone git@github.com:bchiarito/cmssw_CustomPFNanoTwoProng-v1.git .
scram b -j 10
```

### build instructions from scratch
```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_19_patch2
cd CMSSW_10_6_19_patch2/src
cmsenv
git cms-init  
git cms-rebase-topic andrzejnovak:614nosort
git clone https://github.com/cms-jet/PFNano.git PhysicsTools/PFNano
git cms-addpkg PhysicsTools/NanoAOD
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
mkdir temp
cd temp
git init
git remote add -f origin https://github.com/bchiarito/cmssw_CustomPFNanoTwoProng-v1.git
git config core.sparseCheckout true
echo "tweaks" >> .git/info/sparse-checkout
git pull origin master
cd ..
mkdir -p PhysicsTools/NanoAODTools/test
cp temp/tweaks/pfnano_hacks/addPFCands_cff.py PhysicsTools/PFNano/python
cp temp/tweaks/pfnano_hacks/pfnano_cff.py PhysicsTools/PFNano/python
cp temp/tweaks/pfnano_hacks/photons_cff.py PhysicsTools/NanoAOD/python
cp temp/tweaks/pfnano_hacks/genparticles_cff.py PhysicsTools/NanoAOD/python
cp temp/tweaks/pfnano_hacks/LHETablesProducer.cc PhysicsTools/NanoAOD/plugins
cp temp/tweaks/pfnano_cfgs/NANOAOD*_cfg.py PhysicsTools/PFNano/test/
cp temp/tweaks/pfnano_cfgs/Cert_* PhysicsTools/PFNano/test/
cp temp/tweaks/nanoaodtools_modules/* PhysicsTools/NanoAODTools/python/postprocessing/modules/
cp temp/tweaks/nanoaodtools_running/* PhysicsTools/NanoAODTools/test
rm -rf temp/
scram b -j 10
```
