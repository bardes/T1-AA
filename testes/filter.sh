#!/bin/bash

sed -i -e "s/: /:/" -e "s/, /,/g" -e "s/\.$//" -e "/^$/d" $(find -name "*.in")
