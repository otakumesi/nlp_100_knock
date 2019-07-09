echo '10:'
wc ./hightemp.txt

echo '11:'
cat ./hightemp.txt | tr '\t' ' ' | expand

echo '12:'
cut -f 1 ./hightemp.txt > ./col1.txt
cut -f 2 ./hightemp.txt > ./col2.txt
cat ./col1.txt
cat ./col2.txt

echo '13:'
paste ./col1.txt ./col2.txt

echo '14:'
head -n 7 ./hightemp.txt

echo '15:'
tail -n 7 ./hightemp.txt

echo '16:'
split -l 10 ./hightemp.txt splitted-

echo '17:'
sort col1.txt | uniq

echo '18:'
cat ./hightemp.txt | tr '\t' ' ' | sort -k 3 -t ' '

echo '19:'
cut -f 1 ./hightemp.txt | sort | uniq -c | sort -r -k 1 -t ' '
