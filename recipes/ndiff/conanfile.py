from conans import ConanFile, CMake, tools

import multiprocessing
import os
import shutil


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
    options = {}
    default_options = {}
    generators = "make"

    def source(self):
        source_folder = "ndiff-2.00"
        filename = source_folder + ".tar.gz"
        tools.ftp_download("ftp.math.utah.edu", "/pub/misc/" + filename)
        shutil.rmtree(source_folder, ignore_errors=True)
        tools.untargz(filename)

    def build(self):
        with tools.chdir("ndiff-2.00"):
            package_dir = "package"
            if self.should_configure:
                self.run("./configure --prefix={}".format(
                    os.path.abspath(package_dir)))
            if self.should_build:
                self.run("make all -j {}".format(multiprocessing.cpu_count()))
            if self.should_test:
                self.run("make check")

    def package(self):
        source_folder = "ndiff-2.00"
        package_dir = os.path.join(source_folder, "package")
        # The install command doesn't create these two folders
        os.makedirs(os.path.join(package_dir, "bin"), exist_ok=True)
        os.makedirs(os.path.join(package_dir, "man", "man1"), exist_ok=True)
        with tools.chdir(source_folder):
            self.run("make install")
        self.copy("*", src=package_dir)
