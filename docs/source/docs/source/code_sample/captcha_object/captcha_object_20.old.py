import discapty

captcha = discapty.Captcha("whezzy")
captcha_object = captcha.generate_captcha()

# Checking the code
is_correct = captcha.verify_code(user_input)
