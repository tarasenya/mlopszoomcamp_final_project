 #!/bin/bash
 current_date=`date +"%Y-%m-%d"`
 aws --endpoint-url=http://localhost:4566 s3 cp ../data/interim/heart_stroke_.csv s3://heart-stroke-data/heart_stroke_${current_date}.csv
