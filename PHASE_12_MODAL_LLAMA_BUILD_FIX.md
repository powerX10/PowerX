# PowerX Phase 12 Modal llama.cpp build fix

Adds `pkg-config` to the Modal Debian image. The previous build reached llama-cpp-python compilation successfully but CMake stopped because `PKG_CONFIG_EXECUTABLE` was missing while configuring the OpenBLAS backend.
