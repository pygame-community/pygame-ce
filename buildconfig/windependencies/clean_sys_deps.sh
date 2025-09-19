# Cleans environment for the install of win deps, deleting things that are not
# required, or things that will be replaced with something else

rm -rf $MINGW_PREFIX/lib/libz.*
rm -rf $MINGW_PREFIX/lib/liblzma.*
rm -rf $MINGW_PREFIX/lib/libzstd.*
