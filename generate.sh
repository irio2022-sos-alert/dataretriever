#!/bin/bash

cd alertconfirmer
python -m grpc_tools.protoc -I../protos --python_out=. \
 --pyi_out=. --grpc_python_out=. ../protos/alert.proto
cd ..

cd alertmanager
python -m grpc_tools.protoc -I../protos --python_out=. \
 --pyi_out=. --grpc_python_out=. ../protos/alert.proto
cd ..

cd alertsender
python -m grpc_tools.protoc -I../protos --python_out=. \
 --pyi_out=. --grpc_python_out=. ../protos/alert.proto
cd ..
