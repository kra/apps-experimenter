# Requirements

- Have Credential List 'experimenter' with credential 'experimenter'
- Have SIP Domain 'futel-experimenter' with SIP registartion enabled, voice authentication and SIP registration for 'experimenter' Credential List
- Have a Twilio phone number

# Test

Register SIP client to sip:experimenter@futel-experimenter.sip.twilio.com.

- FROM_PSTN_NUMBER: <Twilio test PSTN number>

    twilio api:core:calls:create --from="<FROM_PSTN_NUMBER>" --to="sip:experimenter@futel-experimenter.sip.twilio.com" --url="https://ws.app-dev.phu73l.net/index.xml" --method=GET

