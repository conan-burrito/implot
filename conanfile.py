from conans import tools, ConanFile, CMake

import os


class Recipe(ConanFile):
    name = 'implot'
    description = 'Advanced 2D Plotting for Dear ImGui'
    homepage = 'https://github.com/epezent/implot'
    license = 'MIT'
    url = 'https://github.com/conan-burrito/implot'

    settings = 'os', 'arch', 'compiler', 'build_type'
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
        'with_demo': [True, False]
    }
    default_options = {'shared': False, 'fPIC': True, 'with_demo': True}

    generators = 'cmake'
    exports_sources = ['CMakeLists.txt', 'Config.cmake.in']
    requires = ['imgui/1.83@conan-burrito/stable']

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    @property
    def source_subfolder(self):
        return 'src'

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination='src', strip_root=True)

    def build(self):
        cmake = CMake(self)
        cmake.definitions['IMPLOT_VERSION'] = str(self.version)
        cmake.definitions['IMPLOT_SOVERSION'] = tools.Version(str(self.version)).major
        cmake.definitions['IMPLOT_DEMO'] = 'ON' if self.options.with_demo else 'OFF'

        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self.source_subfolder)

    def package_info(self):
        self.cpp_info.libs = ['implot']

        self.cpp_info.names['cmake_find_package'] = 'ImPlot'
        self.cpp_info.names['cmake_find_package_multi'] = 'ImPlot'
