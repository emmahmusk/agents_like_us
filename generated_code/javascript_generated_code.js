const sendAndVerifyOTP = async (phoneNumber, channel = 'sms') => {
  if (!phoneNumber || typeof phoneNumber !== 'string' || !phoneNumber.startsWith('+')) {
    throw new Error('Invalid phone number.  Must be in E.164 format (e.g., +15551234567).');
  }
  if (!['sms', 'whatsapp'].includes(channel)) {
    throw new Error('Invalid channel. Must be "sms" or "whatsapp".');
  }
  const twilio = require('twilio');
  const client = new twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);
  try {
    const verification = await client.verify.services(process.env.TWILIO_SERVICE_SID)
      .verifications
      .create({
        to: phoneNumber,
        channel,
      });
    return verification.sid;
  } catch (error) {
    if (error.response && error.response.body) {
      throw new Error(`Twilio error: ${error.response.body.message}`);
    }
    throw new Error(`Error sending OTP: ${error.message}`);
  }
};
const verifyOTP = async (verificationSid, code) => {
  if (!verificationSid || typeof verificationSid !== 'string') {
    throw new Error('Invalid verification SID.');
  }
  if (!code || typeof code !== 'string') {
    throw new Error('Invalid verification code.');
  }
  const twilio = require('twilio');
  const client = new twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);
  try {
    const verificationCheck = await client.verify
      .services(process.env.TWILIO_SERVICE_SID)
      .verificationChecks
      .create({
        to: code,
        code,
      });
    return verificationCheck.status === 'approved';
  } catch (error) {
    throw new Error(`Error verifying OTP: ${error.message}`);
  }
};
module.exports = { sendAndVerifyOTP, verifyOTP };