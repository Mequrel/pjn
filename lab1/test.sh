export TIMEFORMAT="%E"

echo "BASH"
time ./bash.sh potop-utf8.txt > result-bash.txt

echo "PYTHON"
time python python.py potop-utf8.txt > result-python.txt


