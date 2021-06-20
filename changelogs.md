Stable 1.0.0
============
**This release present breaking changes. You're advised to read this changelog to know what to do in order to update your code.**

A more complete rewrite of the main library has been done, plus DisCapTy one too.
They are not meant to make the code faster but more easy to read and understand, and developer friendly.

* ``PlainCaptcha`` has been renamed into ``TextCaptcha``
* Fully added typehinting to the base library and DisCapTy, making more easy to pass your own functions directly to the generator.
* ``discapty.Captcha.generate_embed`` now return a ``discord.Embed`` object only instead of a dict with the embed and the captcha.
* ``discapty.Captcha.verify_code`` will now check case. To revert that change, use the ``ignore_case`` argument.
* You can now customize the embed's image URL when generating embed.
* Width and height are defined when generating captcha, not when initializing class.

Beta 0.4
========
* Developers can now add other fields (Author, title, etc...) in the embed when using ``Captcha.generate_embed``.

Beta 0.3.2
==========
* Install requirements throught pip
* Fix a missing fonts file?

Beta 0.3
========
* Initial commit, nothing much to say.