echo "BASH"
time ./bash.sh potop-utf8.txt > result-bash.txt
cat bash.sh | wc -c
echo "PYTHON"
time python ./python.py potop-utf8.txt > result-python.txt
cat python.py | wc -c
echo "SCALA-PARSERS"
time scala WordCount potop-utf8.txt > result-scala-parsers.txt
cat scala-simple.scala | wc -c
echo "SCALA"
time scala WordCountEasy potop-utf8.txt > result-scala.txt
cat scala.scala | wc -c
echo "JAVA"
time java WordCounter potop-utf8.txt > result-java.txt
cat WordCounter.java | wc -c
echo "JS"
time node WordCounter.js potop-utf8.txt > result-js.txt
cat WordCounter.js | wc -c