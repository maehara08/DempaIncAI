echo "dir $1"

# usage: ln -s /usr/local/Cellar/opencv/2.4.12_2/share/OpenCV/haarcascades haarcascades'
# sh run.sh ../images/images_mirin/ out_mirin

members=("risa")
#members=("pincky" "risa" "nemu")
inputpath="../images/images_"

for name in ${members[@]} ; 
do
    for file in `\find $inputpath$name -maxdepth 1 -type f`; do
  		cmd="python detect.py $file out_$name"
 		$cmd
	done
done


