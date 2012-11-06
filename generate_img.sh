#!/bin/sh
mkdir -p tmp/xmlapi
cp -a xmlapi/* tmp/xmlapi
cp update_script tmp/
cd tmp
tar -czvf ../hq-xmlapi.img *
