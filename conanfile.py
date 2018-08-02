#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
from distutils.spawn import find_executable

from conans import ConanFile, CMake
from conans.tools import ftp_download, unzip, os_info, SystemPackageTool

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
    exports_sources = ["CMakeLists.txt", "ucm.cmake"]
    settings = "os", "arch", "compiler", "build_type"

    options = dict({
        "shared": [True, False],
        "fPIC": [True, False],
        })
    default_options = ("shared=True", "fPIC=True")
    short_paths = True
    build_policy = "missing"

    def build_requirements(self):
        pass

    def configure(self):
        pass


    def requirements(self):
        pass

    def source(self):
        folder_name = "dcmtk%s" % self.version.replace(".", "")
        archive_name =  "dcmtk-%s.tar.gz" % self.version
        server_name = "dicom.offis.de"
        file_name = "pub/dicom/offis/software/dcmtk/%s/%s" % (folder_name, archive_name)
        ftp_download(server_name, file_name)
        unzip(archive_name)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_APPS"] = "OFF"
        if self.options.shared:
            cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
        else:
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"

        if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
            cmake.definitions["CMAKE_DEBUG_POSTFIX"] = "_d"
        if self.settings.compiler != "Visual Studio":
            if self.options.fPIC:
                cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"

        cmake.configure()
        cmake.build(target="install")

    def package(self):
        pass

    def package_info(self):
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
