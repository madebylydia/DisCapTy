from discapty import Challenge, WheezyGenerator

challenge = Challenge(WheezyGenerator(width=200, height=100))

captcha_object = challenge.begin()

# Checking the code
is_correct = challenge.check(user_input)
