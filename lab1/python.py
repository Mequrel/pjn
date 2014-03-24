import re
import sys
import string

from collections import Counter

punctuation_regex = re.compile("[" + re.escape(string.punctuation) + "]")

def extract_words(line):
  no_punctuation = re.sub(punctuation_regex, "\n", line)
  lowered = no_punctuation.lower()
  return lowered.split()

def main():
  counter = Counter()

  with open(sys.argv[1]) as f:
    for line in f:
      words_in_line = extract_words(line)
      counter.update(words_in_line)

  for word, count in counter.most_common():
    print("{} {}".format(count, word))

if __name__ == '__main__':
  main()


    