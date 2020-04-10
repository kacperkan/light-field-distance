
Light Field Distance metric
===========================

Original repo: `link <https://github.com/Sunwinds/ShapeDescriptor>`_

Note
----

The code was converted to be able to use LFD metric (distance between two 
descriptors) that will compare visual appearance between ground truth mesh and 
retrieved mesh.

This fork
---------

The original repository was adapted partially to run on Linux. Only ``LightField`` 
was changed so it can be used through docker without any dependency. Underneath,
the container uses OSMesa for headless rendering. 

Requirements
------------


* docker
* ``pip install docker``

Installation
------------

.. code-block:: bash

   pip install light-field-distance

or 

.. code-block::

   python setup.py install

No need to explicitly install anything.

Usage
-----

.. code-block:: python

   from lfd import get_light_field_distance

   # rest of code
   path_to_shape_1: str = ...
   path_to_shape_2: str = ...

   lfd_value: float = get_light_field_distance(path_to_shape_1, path_to_shape_2)

The script will calculate light field distances 
`[1] <http://www.cs.jhu.edu/~misha/Papers/Chen03.pdf>`_ between two shapes. 
Example usage:

.. code-block:: python

   from lfd import get_light_field_distance

   # rest of code
   path_to_shape_1 = "examples/cup1.obj"
   path_to_shape_2 = "examples/airplane.obj"

   lfd_value: float = get_light_field_distance(path_to_shape_1, path_to_shape_2)
   print(lfd_value)

The lower the metric's value, the more similar shapes are in terms of the visual
appearance

How does it work
----------------

The ``lfd.py`` is a proxy for the container that install all the dependency necessary
to run a C code. The code performs calculation of Zernike moments and other
coefficients that are necessary to calculate the distance (\ ``3DAlignment`` program).
Then, these coefficients are saved and run by the ``Distance`` program that calculated the
Light Field Distance. It prints out the result and the stdout from the printing
is handled by the python script.

If an image for the C code is not found, it builds one. The operation is performed
once and it takes a while to finish it. After that, the script runs the necessary 
computations transparently.

Contribution
------------

For anyone interested in having a contribution, these are things to be done. 
Due to the time constraints, I'm not able to do these on my own:


* [ ] adapt code to handle passing vertices and edges directlt
* [ ] retrieve calculating coefficients from renders to be returned by a method
* [ ] bind C code with pybind11 to allow direct computation from the python code
    without any Docker dependency

How am I sure that it works as supposed?
----------------------------------------

I checked descriptor artifacts from the original implementation and compared with results in the docker through md5sum
