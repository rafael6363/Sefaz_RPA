from anticaptchaofficial.imagecaptcha import *
def anticaptcha():
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key("f28c1eadf668c9646d4b564e71678bc5")
    

    # Specify softId to earn 10% commission with your app.
    # Get your softId here: https://anti-captcha.com/clients/tools/devcenter
    solver.set_soft_id(0)

    captcha_text = solver.solve_and_return_solution(fr'C:\Sefaz_RPA\img\captcha.jpg')
    if captcha_text != 0:
        print("o captcha foi resolvido corretamente")

    return captcha_text
