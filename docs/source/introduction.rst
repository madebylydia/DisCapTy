.. _usage:

============
Introduction
============

This is a simplified guide to show everyone how to use the DisCapTy library.
This guide is meant for everyone, however if you're an experienced developer, you might be interested to read the :ref:`DisCapTy API` directly.

To read this guide
------------------

Before you read this guide, we need to explain some terms we will use here.
The word we will define here will be reference in uppercase and italic through this guide, for example, the word `CAPTCHA`, defined below, will be used in the guide as "`CAPTCHA`".

#. ``GENERATOR``: A `GENERATOR` is a class that can be initialized with required/optional arguments (Or none at all), and that will generate a `CAPTCHA OBJECT` based on any given input. The result can be of any form.
#. ``RAW CODE``/``CODE``: The `RAW CODE` or `CODE`  is the code that you'll provide to DisCapTy, it is a clear code, and it is the expected input of your user.
#. ``CAPTCHA OBJECT``: The `CAPTCHA OBJECT` is the result of a `GENERATOR`, it can be anything (Text, audio, image, etc...) and it is what the user will face during it's `CHALLENGE`.
#. ``CHALLENGE``: A `CHALLENGE` is a temporary question-answer made for one single user. A `CHALLENGE` can have different states:

   * ``PENDING``: The `CHALLENGE` is waiting to begin.
   * ``WAITING``: The `CHALLENGE` has begun, he is now waiting for user's input.
   * ``COMPLETED``: The `CHALLENGE` has been completed with success.
   * ``FAILED``: The `CHALLENGE` has been failed by the user. (Generally by giving too many wrong answers)
   * ``FAILURE``: The `CHALLENGE` has unexpectedly failed (Such as cancelled)

   It is generally thrown away after being completed, or failed.

#. ``CAPTCHA CLASS``: Refers to the :py:obj:`discapty.Captcha` class.
#. ``CHALLENGE CLASS``: Refers to the :py:obj:`discapty.Challenge` class.

Objects of DisCapTy
-------------------

Assuming you're reading this guide because this is the first time you're interacting with DisCapTy, you may need to understand what objects will DisCapTy serves you.
This is important because if your codebase doesn't understand what you are using, you might find yourself into a mess that is not a captcha. 🤔

:py:obj:`discapty.Captcha`
^^^^^^^^^^^^^^^^^^^^^^^^^^
A `CAPTCHA CLASS` contain the `RAW CODE` and it's `CAPTCHA OBJECT` in the same place.
It is where you can check for user's input directly using the ``.check`` function.

.. attention::
   This class does not generates the `CAPTCHA OBJECT` itself, a `GENERATOR` do.
   The `CAPTCHA CLASS` just wrap the `RAW CODE` and the `CAPTCHA OBJECT` together.

.. _intro_challenge:

:py:obj:`discapty.Challenge`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The `CHALLENGE CLASS` is the DisCapTy's implementation of a `CHALLENGE`.
With the `CHALLENGE CLASS`, you are able to generate the captcha, verify's user input, set a defined limit of retries, use a custom `CODE`, etc...

The `CHALLENGE CLASS` has different states, as stated in `CHALLENGE`. If the challenge state's is either ``FAILED``, ``FAILURE`` or ``COMPLETED``, it cannot be edited.
While properties are writable, you're advised to not touch them manually.

You can access the states in :py:obj:`discapty.States`

Subclasses of :py:obj:`discapty.Generator`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Any subclasses of :py:obj:`discapty.Generator` are considered to be `GENERATORS`. They can be used in :py:obj:`Challenges <discapty.Challenge>`, or directly, like this:

.. code-block:: python

   # TextGenerator is a subclass of Generator
   from discapty import TextGenerator

   captcha_object = TextGenerator().generate('My Code')

   send_to_user(captcha_object)

A generator can have default arguments arguments. You can change them directly when initializing the class:

.. code-block:: python

   # An image based Captcha object generator
   from discapty import WheezyGenerator

   captcha_object = WheezyGenerator(width=500, height=200, noise_level=3).generate('My code')  # Returns a PIL.Image.Image object

   send_image_to_user(captcha_object)

Certain generators will requires you to give certain arguments. In the case of DisCapTy's builtin generators, they all have optional arguments.

.. _create_challenge:

Creating a Challenge
--------------------

Now that you know what you'll interact with, it's time for you to create your first `CHALLENGE CLASS`.

To create a `CHALLENGE`, you just have to initialize the `CHALLENGE CLASS` with an initialized generator you want to use.

.. code-block:: python

   from discapty import Challenge, TextGenerator

   challenge = Challenge(TextGenerator())
   captcha_object = challenge.begin()  # You'll obtain your CAPTCHA_OBJECT HERE

From here you can send your `CAPTCHA OBJECT` to your user, and you can validate the user's input like this:

.. code-block:: python

   user_input = get_user_input()

   is_valid_input = challenge.check(user_input)

This is a basic example, and it is a `bad` one, because the ``.check`` function can raise :py:exc:`TooManyRetriesError <discapty.errors.TooManyRetriesError>` if ``.check`` has been used more than the ``allowed_retries`` attributes allows it.
The ``allowed_retries`` attribute can be edited when creating the `CHALLENGE CLASS`.

If you do like a more complete example, check the following:

.. code-block:: python

   from discapty import Challenge, TextGenerator, TooManyRetriesError

   challenge = Challenge(TextGenerator(), allowed_retries=3)

   first_captcha = challenge.begin()
   send_to_user(first_captcha)

   # challenge.is_completed returns `True` when the Challenge's state is either completed or failed.
   while not challenge.is_completed:
       user_input = get_user_input()

       try:
           is_right = challenge.check(user_input)
           # If it is right, the challenge will be completed.
       except TooManyRetriesError:
           # From here, challenge will be completed.
           is_right = False

       # The loop will continue until a right answer has been completed or if there is too many retries.

   if is_right:
       do_something_for_completing_the_captcha()
   else:
       do_something_for_failing_the_captcha()

This code is already more suitable for your needs.

Creating a Captcha queue
------------------------

The DisCapTy's Captcha queue permit the developers to store many `CHALLENGE CLASS` in one place, it takes cares of managing all of them.
Putting in place the Captcha queue is fairly easy. The Captcha queue will always give an ID to a challenge, if you don't pass one, an `UUID <ps://docs.python.org/3/library/uuid.html#uuid.uuid4>`_ will be generated for you.

To use the queue, as always you just need to initialize it with one or more initialized generator(s):

.. code-block:: python

   from discapty import CaptchaQueue, WheezyGenerator, TextGenerator

   # With one generator
   my_queue = CaptchaQueue(TextGenerator())

   # With multiple generators
   my_queue = CaptchaQueue([TextGenerator(), WheezyGenerator()])

if you use multiple generators, this mean that one generator will be picked randomly when creating a `CHALLENGE CLASS`.

.. warning::

   This may create inconsistency when generating `CAPTCHA OBJECTS` where you'll need to check in your code what kind of `CAPTCHA OBJECT` you receive, for example, you may send an image differently from a string.

After then, you can create a challenge by calling ``.create_challenge``:

.. code-block:: python

   from discapty import CaptchaQueue, TextGenerator

   queue = CaptchaQueue(TextGenerator())

   challenge = queue.create_challenge()  # You'll obtain a challenge here

   send_captcha_to_user(challenge.captcha)

   challenge_id = challenge.id
   # To obtain your challenge through it's ID
   challenge = queue.get_challenge(challenge_id)

   # To delete/cancel your challenge
   queue.delete_challenge(challenge_id)
