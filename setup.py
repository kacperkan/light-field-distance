from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="light-field-distance",
    version="0.0.1",
    author="Kacper Kania",
    license=u"BSD",
    packages=find_packages(
        exclude=["3DAlignment", "Executable", "LightField"]
    ),
    install_requires=["docker>=4.2.0"],
    long_description=readme,
    description=(
        "light-field-distance is a BSD-licensed package for "
        "calculating Light Field Distance from two Wavefront OBJ "
        "meshes using OpenGL and Docker underneath"
    ),
    classifiers=[
        u"Development Status :: 4 - Beta",
        u"Environment :: Console",
        u"Intended Audience :: Developers",
        u"Intended Audience :: Education",
        u"Intended Audience :: Science/Research",
        u"License :: OSI Approved :: BSD License",
        u"Operating System :: MacOS :: MacOS X",
        u"Operating System :: Microsoft :: Windows",
        u"Operating System :: POSIX",
        u"Programming Language :: C",
        u"Programming Language :: Python :: 3",
        u"Topic :: Multimedia :: Graphics :: 3D Rendering",
        u"Topic :: Scientific/Engineering",
        u"Topic :: Scientific/Engineering :: Information Analysis",
        u"Typing :: Typed",
    ],
)
