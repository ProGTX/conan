from conans import ConanFile, CMake, tools

import multiprocessing


class NdiffConan(ConanFile):
    name = "ndiff"
    version = "2.0"
    license = "MIT"
    author = "Peter Žužek peterzuzek@gmail.com"
    url = "https://github.com/ProGTX/conan"
    description = (
        "Compare putatively similar files, ignoring small numeric differences. "
        + "See http://www.math.utah.edu/~beebe/software/ndiff/.")
    topics = ("ndiff", "diff")
    settings = (
        "os",
        "compiler",
        "build_type",
        "arch",
    )
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "make"

    def source(self):
        source_folder = "ndiff-2.00"
        filename = source_folder + ".tar.gz"
        tools.ftp_download("ftp.math.utah.edu", "/pub/misc/" + filename)
        tools.untargz(filename)

    def build(self):
        with tools.chdir("ndiff-2.00"):
            if self.should_configure:
                self.run("./configure")
            if self.should_build:
                # Only 3 source files
                self.run("make all -j 3")
            if self.should_test:
                self.run("make check")

    def package(self):
        source_folder = "ndiff-2.00"
        self.copy("ndiff", dst="bin", src=source_folder)
        self.copy("*.h", dst="include", src=source_folder)

    def package_info(self):
        self.cpp_info.libs = ["hello"]
