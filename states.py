from aiogram.fsm.state import State, StatesGroup


class PurchaseStates(StatesGroup):
    waiting_for_receipt = State()


class SupportStates(StatesGroup):
    waiting_for_message = State()


class AdminStates(StatesGroup):
    waiting_for_card_number = State()
    waiting_for_card_holder = State()
    waiting_for_rules = State()
    waiting_for_config_text = State()
    waiting_for_reject_reason = State()
    waiting_for_approve_config = State()
    waiting_for_support_reply = State()
