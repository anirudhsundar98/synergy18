#!/bin/bash
move(){
	# echo $1
	mv ~/Downloads/$1 templates/static/images
	cp templates/static/images/$1 prod/static/images
}

move $1