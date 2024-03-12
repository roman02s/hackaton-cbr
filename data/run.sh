#!/bin/bash

max_number=400
for i in $(seq 0 $max_number)
do
    echo "Page ${i}"
    result=$(curl "https://cbr.ru/Crosscut/LawActs/Page/94917?Date.Time=Custom&Date.DateFrom=01%2F01%2F1990%2000%3A00%3A00&Date.DateTo=03%2F01%2F2024%2000%3A00%3A00&Page=${i}")
    urls=$(echo $result | grep -o 'href="[^"]*' | sed 's/href="//')
    for url in ${urls}
    do
        full_url="https://cbr.ru${url}"
        file_name="$(basename ${full_url}).pdf"
        
        # Проверка на существование файла
        if [ ! -f "$file_name" ]; then
            echo "Downloading ${full_url}"
            wget -O "$file_name" "${full_url}"
        else
            echo "File ${file_name} already exists, skipping."
        fi
    done
    
done
