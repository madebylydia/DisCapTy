.. _builtin_generators:

==================
Builtin generators
==================

Here is the following generators coming with DisCapTy:

TextGenerator
^^^^^^^^^^^^^

.. autoclass:: discapty.TextGenerator


.. important::
   The following generators are image-based generators, meaning you'll receive images.
   If you use the color arguments, we make use of `pydantic.Color <https://pydantic-docs.helpmanual.io/usage/types/#color-type>`_. While you CAN pass a ``str`` object, you IDE might complain that you didn't pass a ``pydantic.Color`` object. This is fine, you can just ignore this error, your string will be processed without trouble.


WheezyGenerator
^^^^^^^^^^^^^^^

.. autoclass:: discapty.WheezyGenerator


ImageGenerator
^^^^^^^^^^^^^^

.. autoclass:: discapty.ImageGenerator
