#!/bin/bash

echo 'NOMINAL'
python -u makeStep2condor.py nominal

#sleep 5

#echo "JECUP"
#python -u makeStep2condor.py JECup

#sleep 5

#echo "JECDOWN"
#python -u makeStep2condor.py JECdown

#sleep 5

#echo "JERUP"
#python -u makeStep2condor.py JERup

#sleep 5

#echo "JERDOWN"
#python -u makeStep2condor.py JERdown

echo "SUBMIT DONE"
