Stable 1.0.2
============
This is a hotfix release, fixing typehinting & adding a much easier way to choose the Captcha's code length.

* Typehinting for ``Author`` and ``Footer`` have been fixed.
* You can now choose the Captcha's code length using ``code_length`` attribute when initializing your Captcha class.

Stable 1.0.1
============

**This release present breaking changes. You're advised to read this changelog to know what to do in order to update
your code.**

A more complete rewrite of the main library has been done, plus DisCapTy one too.
They are not meant to make the code faster but more easy to read and understand, and developer friendly.

* ``PlainCaptcha`` has been renamed into ``TextCaptcha`` and his type has been renamed from ``plain`` to ``text``.
* Fully added typehinting to the base library and DisCapTy, making more easy to pass your own functions directly to the generator.
* ``discapty.Captcha.generate_embed`` now return a ``discord.Embed`` object only instead of a dict with the embed and the captcha.
* ``discapty.Captcha.verify_code`` will now check case. To revert that change, use the ``ignore_case`` argument.
* The original error ``discapty.SameCodeError`` has been renamed to ``discapty.CopyPasteError`` for more transparency.
* Every functions doesn't use async/await anymore. You need to remove all awaitable calls.
* You can now customize the embed's image URL when generating embed.
* ``discapty.Captcha.setup`` is now used to set advanced settings for captcha.

Beta 0.4
========
* Developers can now add other fields (Author, title, etc...) in the embed when using ``Captcha.generate_embed``.

Beta 0.3.2
==========
* Install requirements throughout pip
* Fix a missing fonts file?

Beta 0.3
========
* Initial commit, nothing much to say.