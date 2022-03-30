#!/bin/bash

rm -rf output/
mkdir -p output
go build -o output/ application.go

