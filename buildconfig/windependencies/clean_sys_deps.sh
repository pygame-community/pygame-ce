# Cleans environment for the install of win deps, deleting things that are not
# required, or things that will be replaced with something else

rm $MINGW_PREFIX/lib/libz.dll.a
rm $MINGW_PREFIX/lib/liblzma.dll.a
rm $MINGW_PREFIX/lib/libzstd.dll.a
