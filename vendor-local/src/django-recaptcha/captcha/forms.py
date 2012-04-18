from captcha.fields import ReCaptchaField

from registration.forms import RegistrationForm


class RegistrationFormCaptcha(RegistrationForm):
    captcha = ReCaptchaField(attrs={'theme': 'white'})
