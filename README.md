# DisCaPty
*The super hard-to-use module to make your super-hard-coded captcha image for Discord.py.*

DisCaPty is a Captcha's generator for generating captcha and embed for your servers.

## Installing

DisCaPty is available on PyPi!

````commandline
python -m pip install -U discapty
````
unless you want the git method
````commandline
python -m pip install -U git+https://github.com/Predeactor/discapty
````

## Creating your captcha

You can opt for 3 differnts types of captcha. There is "plain", "image" and "wheezy".
Plain is text, the text is "coded" to be sure the user cannot copy and paste the code, meaning he is obligated to rewrite it.

```python
import discapty

async def testme():
    my_captcha: discapty.Captcha = discapty.Captcha("plain")  # Creating my plain captcha without code, if so, a random code is generated.
    # At this point, the code is generated randomly and can already be 
    # verified, but if we want an output of a generated captcha text/image, 
    # use my_captcha.generate_captcha.
    await my_captcha.verify_code(str("SXCU"))
    # True
```

As long as you use "plain" type, you should receive string as the output of `discapy.Captcha.generate_captcha`, but when it comes to "image" and "wheezy", we receive BytesIO objects.

```python
import discapty

async def generate():
    my_captcha: discapty.Captcha = discapty.Captcha("wheezy")
    await my_captcha.generate_captcha(str("SXCU"))
    # <_io.BytesIO object at XxXXX>
```

If you just want to create an embed to send when challenging your member, there is a function for that.

```python
import discapty

async def sendcaptcha():
    my_captcha: discapty.Captcha = discapty.Captcha("image")
    my_embed: dict = await my_captcha.generate_embed(str("Red - Discord Bot"), title=str("Verification of my Discord server!"))
    await ctx.channel.send(embed=my_embed["embed"], file=my_embed["image"])
# We use a dict since we may send an image with our embed with the message to get included.
```

## Contact

You can join the Charlemagne/3 Discord server for any help: https://discord.gg/rD7TTrUcjw
