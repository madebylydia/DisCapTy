.. _builtin_generators:

==================
Builtin generators
==================

Here is the following generators coming with DisCapTy:

TextGenerator
^^^^^^^^^^^^^

.. autoclass:: discapty.TextGenerator
   :noindex:


.. important::
   The following generators are image-based generators, meaning you'll receive images.
   If you use the color arguments, we make use of `pydantic.Color <https://pydantic-docs.helpmanual.io/usage/types/#color-type>`_. While you CAN pass a ``str`` object, you IDE might complain that you didn't pass a ``pydantic.Color`` object. This is fine, you can just ignore this error, your string will be processed without trouble. We tried our best


WheezyGenerator
^^^^^^^^^^^^^^^

.. autoclass:: discapty.WheezyGenerator
   :noindex:


ImageGenerator
^^^^^^^^^^^^^^

.. autoclass:: discapty.ImageGenerator
   :noindex:
