#!/bin/bash

set -o errexit
set -o nounset

DAY=$1

cp "aopy/b/day0.py" "aopy/b/day$DAY.py"
sed -i "" "s/0/$DAY/g" "aopy/b/day$DAY.py"

cp "tests/b/test_day0.py" "tests/b/test_day$DAY.py"
sed -i "" "s/0/$DAY/g" "tests/b/test_day$DAY.py"

touch "examples/b/day$DAY.txt"
touch "inputs/b/day$DAY.txt"
