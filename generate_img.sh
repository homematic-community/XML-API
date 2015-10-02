#!/bin/sh
mkdir -p tmp/xmlapi
cp -a xmlapi/* tmp/xmlapi
cp update_script tmp/
cp xml-api tmp/
cd tmp
tar -czvf ../xmlapi_addon_1.11.tar.gz *
cd ..
rm -rf tmp
