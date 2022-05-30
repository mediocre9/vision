class AppInfo:
    def __init__(self):
        self.APP_NAME = 'Vision'
        self.APP_ICON = 'ico/webcam.png'
        self.GEOMETRY = '400x300'
        self.CONSOLE_TITLE = 'title Vision Network Log'
        self.FORE_THEME = 'white'
        self.BACK_THEME = (91, 161, 227)
        self.CASCADE = 'cascades//haarcascade_fullbody.xml'
        self.IP_WEBCAM = 'https://play.google.com/store/search?q=ip%20webcam&c=apps'
        self.CONFIG_FILE = 'config/config.ini'
        self.HELP = 'Download \'IP Webcam\' from PlayStore and install it on your phone to use this ' \
                    'software.\n\n' \
                    'Instructions:\n' \
                    '1). First connect to the internet on both devices.\n' \
                    '2). Start the IP Webcam server.\n' \
                    f'3). Note the \'IP Webcam\' IP Address, and insert that IP address into \'{self.APP_NAME}\' IP ' \
                    'text field.\n' \
                    '4). Click on the capture button! '
        self.AUTHOR = 'mediocre9'
        self.EMAIL = 'mirzafahadzia9@gmail.com'
        self.GITHUB = 'https://github.com/mediocre9'
        self.SKYLINE_VR = 'https://skyline.github.com/mediocre9/2022'
        self.ABOUT = f'A real time computer vision software, programmed by {self.AUTHOR}. If you have found any bug ' \
                     f'or problem, contact us at {self.EMAIL}.'
