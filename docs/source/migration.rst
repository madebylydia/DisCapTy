.. _migration:

===============
Migration Guide
===============

From 1.0.x to 2.0
=================

DisCapTy has been created to be a supplementary tools for ``discord.py``, however, its owner had announced that this library would not be supported anymore. From here, many peoples has created forks of this library, which was making DisCapTy completely unusable for others library.
This thought has dragged me to think about what DisCapTy should be & become. As such, it has been decided that DisCapTy should NOT be related to ``discord.py`` anymore but as a standalone library with no restriction on where it could be used.

The most important points are:

#. Deprecating generating Captcha in the :py:obj:`discapty.Captcha` class, but rather in a :py:obj:`discapty.Generator` subclass.
#. Featuring :py:obj:`discapty.Challenge` & :py:obj:`discapty.CaptchaQueue`.
#. Added more specific errors to the library.
#. A documentation has been created.

Rewrite of Captcha class
^^^^^^^^^^^^^^^^^^^^^^^^

The :py:obj:`discapty.Captcha` object does not longer generates the Captcha object anymore, what does is a generator.
There is no exact alternative to generates the Captcha object in the same place as the Captcha class, since now the Captcha class only **include** the Captcha object and its code.
However, you can do this:

.. admonition:: Regarding diff block
   :class: note

   The "-" represent the old version, the "+" represent the actual, new version.

.. literalinclude:: docs/source/code_sample/captcha_object/captcha_object_20.py
   :diff: docs/source/code_sample/captcha_object/captcha_object_20.old.py

Removal of ``.setup`` function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Along with the rewrite of the Captcha class, the ``.setup`` function has been removed, instead, parameters can be provided to a generator when initializing a generator class.

.. literalinclude:: docs/source/code_sample/generator_init/gen_init_20.py
   :diff: docs/source/code_sample/generator_init/gen_init_20.old.py

Added ``Challenge`` class
^^^^^^^^^^^^^^^^^^^^^^^^^

The :py:obj:`discapty.Challenge` class is the new preferred way to create Captcha now. You can read more about challenges here: :ref:`Introduction to Challenges <intro_challenge>`

To use ``Challenge`` rather than the old ``Captcha``, you can do these changes:

.. literalinclude:: docs/source/code_sample/captcha_to_challenge/c_to_c.py
   :diff: docs/source/code_sample/captcha_to_challenge/c_to_c.old.py
