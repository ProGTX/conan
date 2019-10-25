from conans import ConanFile, CMake, tools

import multiprocessing
import os
import shutil


class MultitimeConan(ConanFile):
    name = "multitime"
    version = "1.4"
    license = "MIT"
    author = "Peter Žužek peterzuzek@gmail.com"
    url = "https://github.com/ProGTX/conan"
    description = ("Time command execution over multiple executions. " +
                   "See http://tratt.net/laurie/src/multitime/.")
    topics = ("multitime", "time", "benchmark")
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
        source_folder = "multitime"
        git = tools.Git(source_folder)
        shutil.rmtree(source_folder, ignore_errors=True)
        git.clone(
            "https://github.com/ltratt/multitime.git", branch="multitime-1.4")

    def build(self):
        with tools.chdir("multitime"):
            if self.should_configure:
                self.run("autoconf")
                self.run("autoheader")
                self.run("./configure")
            if self.should_build:
                self.run("make all -j {}".format(multiprocessing.cpu_count()))

    def package(self):
        source_folder = "multitime"
        package_dir = "package"
        with tools.chdir(source_folder):
            self.run("make install DESTDIR={}".format(package_dir))
        package_dir = os.path.join(source_folder, package_dir, "usr", "local")
        self.copy("*", src=package_dir)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
