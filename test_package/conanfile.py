from conans import ConanFile, CMake, tools
import os


class Recipe(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            self.run(os.path.join("bin", "test"), run_environment=True)

        if self.settings.os == 'Emscripten':
            self.run("node %s" % os.path.join("bin", "test"), run_environment=True)
