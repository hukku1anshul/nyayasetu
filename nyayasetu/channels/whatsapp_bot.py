"""
WhatsApp Conversational Lead Intake & Concierge Engine
Compatible with Meta WhatsApp Cloud API and Twilio Webhooks.
Provides a frictionless 2-minute citizen onboarding experience via WhatsApp.
"""

from typing import Dict, Any, Optional
import uuid
from datetime import datetime

from nyayasetu.integrations.rta_client import RTAUnclaimedRegisterEngine, RTADirectory
from nyayasetu.engines.iepf_recovery import IEPFTransmissionEngine, UnclaimedAssetFolio
from nyayasetu.engines.gazette_engine import GazetteEngine

class WhatsAppBotEngine:
    """
    State machine managing multi-turn conversational intake over WhatsApp.
    Users can complete end-to-end applications or check claim status via chat.
    """
    # In-memory session store (can be backed by Redis / Postgres)
    USER_SESSIONS: Dict[str, Dict[str, Any]] = {}

    WELCOME_MESSAGE = (
        "🙏 *Namaste! Welcome to NyayaSetu (Adhikar AI)*\n"
        "India's automated legal & bureaucracy concierge.\n\n"
        "How can we assist you today?\n"
        "1️⃣ *Change Name / Correct Passport in Gazette* (₹3,499 flat)\n"
        "2️⃣ *Recover Lost Shares / IEPF Unclaimed Wealth* (Pay only upon success)\n"
        "3️⃣ *MEA Apostille & Degree Legalization* (Insured Doorstep Vault)\n"
        "4️⃣ *Track Existing Case / Gazette Status*\n\n"
        "👉 _Reply with 1, 2, 3, or 4 to begin._"
    )

    @classmethod
    def handle_incoming_message(cls, sender_phone: str, message_text: str, media_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Processes an incoming WhatsApp message and returns the bot's response.
        """
        msg = message_text.strip()
        session = cls.USER_SESSIONS.get(sender_phone, {"state": "IDLE", "data": {}})

        state = session.get("state", "IDLE")

        # Global restart or help
        if msg.lower() in ["hi", "hello", "restart", "start", "menu"]:
            cls.USER_SESSIONS[sender_phone] = {"state": "MENU", "data": {}}
            return {"reply": cls.WELCOME_MESSAGE, "session_state": "MENU"}

        # ----------------- STATE: MENU -----------------
        if state in ["IDLE", "MENU"]:
            if msg == "1":
                cls.USER_SESSIONS[sender_phone] = {"state": "GAZETTE_OLD_NAME", "data": {"service": "GAZETTE"}}
                return {
                    "reply": (
                        "📰 *Central Gazette Name Change Wizard*\n\n"
                        "Please enter your *Current Full Name* (exactly as it appears on your Aadhaar or 10th marksheet):"
                    ),
                    "session_state": "GAZETTE_OLD_NAME"
                }

            elif msg == "2":
                cls.USER_SESSIONS[sender_phone] = {"state": "WEALTH_HOLDER_NAME", "data": {"service": "UNCLAIMED_WEALTH"}}
                return {
                    "reply": (
                        "💎 *Unclaimed Wealth & IEPF Recovery Concierge*\n\n"
                        "Please enter the *Full Name of the Shareholder / Deceased Parent* to search across RTA & IEPF registers:"
                    ),
                    "session_state": "WEALTH_HOLDER_NAME"
                }

            elif msg == "3":
                return {
                    "reply": (
                        "✈️ *MEA Apostille & Cross-Border Vault*\n\n"
                        "We provide insured doorstep pickup for degrees & birth certificates.\n"
                        "To book an insured vault courier, please visit our instant booking portal: "
                        "https://nyayasetu.in/vault-book or type your destination country (e.g., 'UAE', 'USA')."
                    ),
                    "session_state": "MENU"
                }

            elif msg == "4":
                cls.USER_SESSIONS[sender_phone] = {"state": "TRACK_CASE", "data": {}}
                return {
                    "reply": "🔍 Please enter your *Application Docket ID* or *Name* to check live status:",
                    "session_state": "TRACK_CASE"
                }

            else:
                return {
                    "reply": "⚠️ Invalid option. Please reply with *1*, *2*, *3*, or *4*.\n\n" + cls.WELCOME_MESSAGE,
                    "session_state": "MENU"
                }

        # ----------------- GAZETTE FLOW -----------------
        elif state == "GAZETTE_OLD_NAME":
            session["data"]["old_name"] = msg
            session["state"] = "GAZETTE_NEW_NAME"
            cls.USER_SESSIONS[sender_phone] = session
            return {
                "reply": f"Got it: _{msg}_\n\nNow, please enter your *New Desired Full Name*:",
                "session_state": "GAZETTE_NEW_NAME"
            }

        elif state == "GAZETTE_NEW_NAME":
            session["data"]["new_name"] = msg
            session["state"] = "GAZETTE_FATHER_NAME"
            cls.USER_SESSIONS[sender_phone] = session
            return {
                "reply": "Please enter your *Father's Name* (or Spouse's Name):",
                "session_state": "GAZETTE_FATHER_NAME"
            }

        elif state == "GAZETTE_FATHER_NAME":
            session["data"]["father_name"] = msg
            session["state"] = "GAZETTE_CONFIRM"
            cls.USER_SESSIONS[sender_phone] = session

            dossier = GazetteEngine.draft_name_change_affidavit(
                old_name=session["data"]["old_name"],
                new_name=session["data"]["new_name"],
                father_or_spouse_name=msg,
                residential_address="To be fetched via Aadhaar OTP",
                reason="Official record correction"
            )

            docket_id = f"NS-GAZ-{uuid.uuid4().hex[:6].upper()}"
            session["data"]["docket_id"] = docket_id

            return {
                "reply": (
                    f"✅ *Application Docket Created: #{docket_id}*\n\n"
                    f"• *Current Name:* {session['data']['old_name']}\n"
                    f"• *New Name:* {session['data']['new_name']}\n"
                    f"• *Father's Name:* {msg}\n"
                    f"• *Package:* NeSL e-Stamping + 2 Newspapers + Central Gazette CD\n"
                    f"• *Total Fee:* ₹3,499 (All inclusive)\n\n"
                    "👉 _Reply *CONFIRM* to receive your 1-click Aadhaar OTP sign link, or *RESTART* to edit._"
                ),
                "session_state": "GAZETTE_CONFIRM",
                "docket_id": docket_id
            }

        elif state == "GAZETTE_CONFIRM":
            if "confirm" in msg.lower() or "yes" in msg.lower():
                docket = session["data"].get("docket_id", "NS-GAZ-001")
                cls.USER_SESSIONS[sender_phone] = {"state": "IDLE", "data": {}}
                return {
                    "reply": (
                        f"🎉 *Thank you! Case #{docket} is now actively queued.*\n\n"
                        "📲 We have sent an Aadhaar e-Sign authorization link to your phone: "
                        f"https://nyayasetu.in/sign/{docket}\n\n"
                        "Once signed, our team will syndicate the newspaper notices and file the dossier with the Central Gazette Press. "
                        "You will receive live tracking updates right here on WhatsApp!"
                    ),
                    "session_state": "COMPLETED"
                }

        # ----------------- UNCLAIMED WEALTH FLOW -----------------
        elif state == "WEALTH_HOLDER_NAME":
            session["data"]["holder_name"] = msg
            session["state"] = "WEALTH_COMPANY"
            cls.USER_SESSIONS[sender_phone] = session

            # Run preliminary instant search across public RTA registers
            records = RTAUnclaimedRegisterEngine.search_unclaimed_records(msg)

            if records:
                rec = records[0]
                session["data"]["matched_record"] = rec
                reply_text = (
                    f"🚨 *FOUND MATCH IN STATUTORY REGISTERS!*\n\n"
                    f"• *Investor:* {rec['investor_name']}\n"
                    f"• *Company:* {rec['company']} ({rec['rta']})\n"
                    f"• *Folio No:* {rec['folio_number']}\n"
                    f"• *Unclaimed Shares:* {rec['unclaimed_shares']} units\n"
                    f"• *Est. Current Value:* ₹{rec['total_portfolio_value_inr']:,.2f}\n\n"
                    f"Are you a legal heir of *{rec['investor_name']}*? (Reply *YES* to calculate recovery payout)"
                )
            else:
                reply_text = (
                    f"Searching registers for *{msg}*...\n\n"
                    "Which company did they own shares in? (e.g. *Tata Steel*, *Reliance*, *Infosys*, *ITC*, or reply *UNKNOWN*):"
                )

            return {"reply": reply_text, "session_state": "WEALTH_COMPANY"}

        elif state == "WEALTH_COMPANY":
            if "yes" in msg.lower() and "matched_record" in session["data"]:
                rec = session["data"]["matched_record"]
                calc = IEPFTransmissionEngine.calculate_contingency_fee(rec["total_portfolio_value_inr"])
                docket_id = f"NS-IEPF-{uuid.uuid4().hex[:6].upper()}"

                cls.USER_SESSIONS[sender_phone] = {"state": "IDLE", "data": {}}
                return {
                    "reply": (
                        f"📊 *Recovery Plan for Case #{docket_id}:*\n\n"
                        f"• *Total Recoverable Asset:* ₹{calc['gross_asset_value']:,.2f}\n"
                        f"• *Our Success Fee ({calc['contingency_rate_pct']}%):* ₹{calc['platform_success_fee']:,.2f} *(Payable ONLY upon credit to your demat)*\n"
                        f"• *Net Payout to Your Family:* *₹{calc['net_payout_to_client']:,.2f}*\n\n"
                        "📄 *What NyayaSetu handles:*\n"
                        "1. Automated Form ISR-1, ISR-2 Banker Sheets\n"
                        "2. Form-A Affidavit & Form-B Indemnity on NeSL e-Stamp\n"
                        "3. Complete RTA Liaison & Form IEPF-5 filing\n\n"
                        "An empanelled senior case manager has been assigned. You can upload photos of old certificates or death certificates anytime to this chat!"
                    ),
                    "session_state": "COMPLETED",
                    "docket_id": docket_id
                }
            else:
                return {
                    "reply": "Thank you! Our research desk will scan historical MCA physical archives and message you back within 2 hours.",
                    "session_state": "IDLE"
                }

        # Fallback
        return {"reply": cls.WELCOME_MESSAGE, "session_state": "MENU"}
