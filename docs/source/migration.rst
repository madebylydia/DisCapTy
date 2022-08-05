.. _migration:

===============
Migration Guide
===============

From 2.0.x to 2.1.0
===================

DisCapTy 2.1.0 has been released around the beginning august to resolve one major problem of DisCapTy 2.0.x: Type hinting in :py:class:`discapty.generators.Generator`, :py:class:`discapty.Captcha`, :py:class:`discapty.Challenge` and :py:class:`discapty.CaptchaQueue`.
These classes, when returning a captcha object, would give the :py:data:`typing.Any`, which is vague - it actually doesn't tell the developer what type could the captcha object be.

To resolve this issue, generics classes were implemented into needed classes and will now take the type hint from generators to mirror them into methods who return captcha objects.

While this shouldn't require any code changes, if you directly typed your variable, here's how to migrate:

.. code-block:: python
   :caption: Custom generator

   from discapty import Generator

   # Before
   class MyGenerator(Generator):
       def generate(self, text: str) -> str:
           return complexify_text(text)

   # After
   class MyGenerator(Generator[str]):  # Indicate here what ".generate" type will return!
       def generate(self, text: str):  # Type can be disregarded/optional, but good to add too!
           return complexify_text(text)

.. code-block:: python
   :caption: discapty.Captcha, discapty.Challenge, discapty.CaptchaQueue stored in variable with implicit type hint (Python >3.10, else use Union)

   from discapty import Captcha, Challenge, CaptchaQueue, TextGenerator, WheezyGenerator
   import PIL.Image.Image

   # Before
   queue: CaptchaQueue = CaptchaQueue([TextGenerator(), WheezyGenerator()])  # Wait... What's the generator type?
   challenge: Challenge = queue.create_challenge()  # Wait... What's the generator type?
   captcha_class: Captcha = challenge.captcha  # Wait... What's the generator type?

   # After
   queue: CaptchaQueue[str | PIL.Image.Image] = CaptchaQueue([TextGenerator(), WheezyGenerator()])  # Generator's type is "str" or "PIL.Image.Image"!
   challenge: Challenge[str | PIL.Image.Image] = queue.create_challenge()  # Generator's type is "str" or "PIL.Image.Image"!
   captcha_class: Captcha[str | PIL.Image.Image] = challenge.captcha  # Generator's type is "str" or "PIL.Image.Image"!

   captcha_class.captcha_object  # We know this is either a str or a PIL.Image.Image!
   challenge.begin()  # We also know it is either a str or a PIL.Image.Image!

.. note::
   It is not necessary to indicate the variable's type hint, it is even suggested to not do that unless you know what you're doing/be sure of what you want to get.


From 1.0.x to 2.0
=================

DisCapTy has been created to be a supplementary tool for ``discord.py``, however, its owner had announced that this library would not be supported anymore. From here, many peoples has created forks of this library, which was making DisCapTy completely unusable for others library.
This thought has dragged me to think about what DisCapTy should be & become. As such, it has been decided that DisCapTy should NOT be related to ``discord.py`` anymore but as a standalone library with no restriction on where it could be used.

The most important points are:

#. Deprecating generating Captcha in the :py:obj:`discapty.Captcha` class, but rather in a :py:obj:`discapty.generators.Generator` subclass.
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

Added :py:class:`Challenge <discapty.Challenge>` class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :py:obj:`discapty.Challenge` class is the new preferred way to create Captcha now. You can read more about challenges here: :ref:`Introduction to Challenges <intro_challenge>` - :ref:`Creating a Challenge <create_challenge>`

To use :py:class:`discapty.Challenge` rather than the old :py:class:`discapty.Captcha`, you can do these changes:

.. literalinclude:: docs/source/code_sample/captcha_to_challenge/c_to_c.py
   :diff: docs/source/code_sample/captcha_to_challenge/c_to_c.old.py
