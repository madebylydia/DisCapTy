import discapty

code = "My code"
generator = discapty.WheezyGenerator()

captcha_object = generator.generate(code)
captcha = discapty.Captcha(code, captcha_object)

# Checking the code
is_correct: bool = captcha.check(user_input)
