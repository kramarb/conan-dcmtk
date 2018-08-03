#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake
from conans.tools import download, unzip
import os
import shutil
import configparser

class DCMTKConan(ConanFile):

    name = "DCMTK"
    version = "3.6.3"
    description = "Conan package for DCMTK library"
    url = "https://github.com/kramarb/conan-dcmtk"
    homepage = "https://dicom.offis.de/dcmtk.php.en"
    license = "https://support.dcmtk.org/docs/file_copyright.html"
    author = "Miha Orazem miha.orazem@gmail.com"
    settings = "os", "arch", "compiler", "build_type"
    exports = ["CMakeLists.txt"] 
    dcmtk_modules = [ "ofstd", "oflog", "dcmdata", "dcmimgle", "dcmimage", "dcmjpeg", "dcmjpls", "dcmtls", "dcmnet", "dcmsr", "dcmsign", "dcmwlm", "dcmqrdb", "dcmpstat", "dcmrt", "dcmiod", "dcmfg", "dcmseg", "dcmtract", "dcmpmap"]
    options = dict({
        "shared": [True, False],
        "fPIC": [True, False],
        "wide_io" : [True, False],
        "overwrite_win32_flags" : [True, False] # if shared=False and overwrite_win32_flags=True it will build the libs with static runtime (MT/MTd)
    }, **{ module : [True, False] for module in dcmtk_modules})
    default_options = ("shared=True", "fPIC=True", "wide_io=False", "overwrite_win32_flags=True") + tuple(module + "=True" for module in dcmtk_modules)
    short_paths = True
    build_policy = "missing"

    def build_requirements(self):
        pass

    def configure(self):
        if os == "Windows":
            del self.options.fPIC

    def source(self):
        folder_name = "dcmtk%s" % self.version.replace(".", "")
        archive_name =  "DCMTK-%s.tar.gz" % self.version
        download("https://github.com/DCMTK/dcmtk/archive/%s" % archive_name, archive_name)
        unzip(archive_name)
        extraced_folder = "dcmtk-DCMTK-%s" % self.version
        shutil.move(extraced_folder, "src")


    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_APPS"] = "OFF"
        if self.options.shared:
            cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
        else:
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
            cmake.definitions["DCMTK_OVERWRITE_WIN32_FLAGS"] = "ON" if self.options.overwrite_win32_flags else "OFF"

        if self.options.wide_io:
            cmake.definitions["DCMTK_WIDE_CHAR_FILE_IO_FUNCTIONS"] = "ON"

        if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
            cmake.definitions["CMAKE_DEBUG_POSTFIX"] = "_d"
        if self.settings.compiler != "Visual Studio":
            if self.options.fPIC:
                cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        
        enabled_modules = [module for module in self.dcmtk_modules if getattr(self.options, module) == True]
        cmake.definitions["DCMTK_MODULES"] = ';'.join(enabled_modules)
        cmake.configure(build_dir="build")
        cmake.build(target="install")

    def package(self):
        self.copy("*", src="install")

    def package_info(self):
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
