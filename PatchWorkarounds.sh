rootPath=$(realpath "${PICOPAD_BASE_PATH}../../..")
THE_SDK_PATH="$rootPath/picopad-playground/picopad-sdk/"
cd $THE_SDK_PATH
sed -i s,set\(PICO,set\(X-PICO,g picopad-gb/CMakeLists.txt
mkdir -p "$rootPath/picopad-playground/picopad-sdk/assets/"

# make GBC builder
cp -a ./picopad-gb/ ./picopad-gbc/
sed -i "s,PEANUT_FULL_GBC_SUPPORT 0,PEANUT_FULL_GBC_SUPPORT 1," ./picopad-gbc/src/main.cpp
