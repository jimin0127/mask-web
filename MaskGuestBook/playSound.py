import pygame

class playsound:
    def __init__(self):
        self.freq = 16000  # sampling rate, 44100(CD), 16000(Naver TTS), 24000(google TTS)
        self.bitsize = -16  # signed 16 bit. support 8,-8,16,-16
        self.channels = 1  # 1 is mono, 2 is stereo
        self.buffer = 2048  # number of samples (experiment to get right sound)


    def play_detect_mask(self):
        pygame.mixer.init(self.freq, self.bitsize, self.channels, self.buffer)
        self.detect_mask_sound = pygame.mixer.Sound("MaskGuestBook/sounds/detect_mask.wav")
        self.detect_mask_sound.play()

    def play_camera(self):
        pygame.mixer.init(self.freq, self.bitsize, self.channels, self.buffer)
        self.camera_sound = pygame.mixer.Sound("MaskGuestBook/sounds/찰칵소리.wav")
        self.camera_sound.play()

    def play_pose(self):
        pygame.mixer.init(self.freq, self.bitsize, self.channels, self.buffer)
        self.pose_sound = pygame.mixer.Sound("MaskGuestBook/sounds/pose.wav")
        self.pose_sound.play()

    def play_countdown(self):
        pygame.mixer.init(self.freq, self.bitsize, self.channels, self.buffer)
        self.countdown_sound = pygame.mixer.Sound("MaskGuestBook/sounds/countdown.wav")
        self.countdown_sound.play()

    def play_wear_mask(self):
        pygame.mixer.init(self.freq, self.bitsize, self.channels, self.buffer)
        self.wear_mask_sound = pygame.mixer.Sound("MaskGuestBook/sounds/plz_wear_mask.wav")
        self.wear_mask_sound.play()