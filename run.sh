#! /bin/bash

mkdir raw_data
cd simulation_rust/
cargo build --release
cd ../raw_data/
../simulation_rust/target/release/randomness-sim
cd ../
mkdir Result 
python3 main.py
