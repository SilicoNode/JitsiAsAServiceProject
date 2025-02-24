import time
import uuid
from authlib.jose import jwt

class JaaSJwtBuilder:
    EXP_TIME_DELAY_SEC = 7200
    NBF_TIME_DELAY_SEC = 10

    def __init__(self):
        self.header = { 'alg': 'RS256' }
        self.userClaims = {}
        self.featureClaims = {}
        self.payloadClaims = {}

    def withDefaults(self):
        return self.withExpTime(int(time.time() + self.EXP_TIME_DELAY_SEC)) \
            .withNbfTime(int(time.time() - self.NBF_TIME_DELAY_SEC)) \
            .withLiveStreamingEnabled(True) \
            .withRecordingEnabled(True) \
            .withOutboundCallEnabled(True) \
            .withSipOutboundCallEnabled(True) \
            .withTranscriptionEnabled(True) \
            .withModerator(True) \
            .withRoomName('*') \
            .withUserId(str(uuid.uuid4()))

    def withApiKey(self, apiKey):
        self.header['kid'] = apiKey
        return self

    def withUserAvatar(self, avatarUrl):
        self.userClaims['avatar'] = avatarUrl
        return self

    def withModerator(self, isModerator):
        self.userClaims['moderator'] = 'true' if isModerator else 'false'
        return self

    def withUserName(self, userName):
        self.userClaims['name'] = userName
        return self

    def withUserEmail(self, userEmail):
        self.userClaims['email'] = userEmail
        return self

    def withLiveStreamingEnabled(self, isEnabled):
        self.featureClaims['livestreaming'] = 'true' if isEnabled else 'false'
        return self

    def withRecordingEnabled(self, isEnabled):
        self.featureClaims['recording'] = 'true' if isEnabled else 'false'
        return self

    def withTranscriptionEnabled(self, isEnabled):
        self.featureClaims['transcription'] = 'true' if isEnabled else 'false'
        return self

    def withSipOutboundCallEnabled(self, isEnabled):
        self.featureClaims['sip-outbound-call'] = 'true' if isEnabled else 'false'
        return self

    def withOutboundCallEnabled(self, isEnabled):
        self.featureClaims['outbound-call'] = 'true' if isEnabled else 'false'
        return self

    def withExpTime(self, expTime):
        self.payloadClaims['exp'] = expTime
        return self

    def withNbfTime(self, nbfTime):
        self.payloadClaims['nbf'] = nbfTime  # FIXED: Corrected 'nbfTime' to 'nbf'
        return self

    def withRoomName(self, roomName):
        self.payloadClaims['room'] = roomName
        return self

    def withAppID(self, AppId):
        self.payloadClaims['sub'] = AppId
        return self

    def withUserId(self, userId):
        self.userClaims['id'] = userId
        return self

    def signWith(self, private_key):
        context = {'user': self.userClaims, 'features': self.featureClaims}
        self.payloadClaims['context'] = context
        self.payloadClaims['iss'] = 'chat'
        self.payloadClaims['aud'] = 'jitsi'
        return jwt.encode(self.header, self.payloadClaims, private_key)
