====================================
Welcome to DisCapTy's documentation!
====================================

.. image:: _static/logo.png
   :class: only-dark

.. image:: _static/logo-dark.png
   :class: only-light

DisCaPty is a Python module to generate Captcha images & challenges without struggling your mind on how to make your own.

**Features:**

* Highly customizable Captcha generation / Hackable
* Developer & user friendly
* Extendable with your own/third-party generators

Example
-------

.. code-block:: python

   from discapty import Challenge, ImageGenerator, TooManyRetriesError

   challenge = Challenge(ImageGenerator(width=500, height=250, fonts=["./my-fonts.ttf"]), allowed_retries=5)
   captcha = challenge.begin()
   send_captcha_to_user(captcha)

   user_input = get_user_input()

   try:
       is_valid = challenge.check(user_input)
       if is_valid:
           print("You're correct!")
       else:
           print("You're incorrect, try again!")
           # And here, do something to get user's input & check again.
   except TooManyRetriesError:
       print("You've made too many errors!")

Pages
-----

.. toctree::
    :titlesonly:

    source/introduction
    source/api
    source/migration
