#!/bin/sh
mkdir -p tmp/xmlapi
cp -a xmlapi/* tmp/xmlapi
cp update_script tmp/
cp xml-api tmp/
cp VERSION tmp/
cd tmp
tar --owner=root --group=root --exclude=.DS_Store -czvf ../xmlapi_addon-$(cat ../VERSION).tar.gz *
cd ..
rm -rf tmp
