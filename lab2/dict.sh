wget http://sjp.pl/slownik/odmiany/sjp-odm-20140112.zip
unzip sjp-odm-20140112.zip
rm README.txt
rm sjp-odm-20140112.zip
mv odm.txt dictionary.win1250.txt
iconv -f windows-1250 -t UTF-8 dictionary.win1250.txt > dictionary.txt
rm dictionary.win1250.txt
