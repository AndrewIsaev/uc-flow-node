from enum import Enum


class Action(str, Enum):
    authorization = "authorization"
    api = "api"


class Resource(str, Enum):
    customer = 'customer'


class Operation(str, Enum):
    get_customers = "get_customers"


class CustomerIsStudy(int, Enum):
    lead = 0
    client = 1


class CustomerGender(str, Enum):
    male = "male"
    female = "female"


class CustomerLegalType(int, Enum):
    physical_person = 1
    legal_person = 2


class CustomerRemoved(int, Enum):
    archived = 2
    active_and_archived = 1
    active = 0


class Parameters(str, Enum):
    customer_id = 'id'
    customer_is_study = 'is_study'
    customer_study_status_id = 'study_status_id'
    customer_name = 'name'
    customer_gender = 'gender'
    customer_age_from = 'age_from'
    customer_age_to = 'age_to'
    customer_phone = 'phone'
    customer_legal_type = 'legal_type'
    customer_legal_name = 'legal_name'
    customer_company_id = 'company_id'
    customer_lesson_count_from = 'lesson_count_from'
    customer_lesson_count_to = 'lesson_count_to'
    customer_balance_contract_from = 'balance_contract_from'
    customer_balance_contract_to = 'balance_contract_to'
    customer_balance_bonus_from = 'balance_bonus_from'
    customer_balance_bonus_to = 'balance_bonus_to'
    customer_removed = 'removed'
    customer_removed_from = 'removed_from'
    customer_removed_to = 'removed_to'
    customer_level_id = 'level_id'
    customer_assigned_id = 'assigned_id'
    customer_employee_id = 'employee_id'
    customer_lead_source_id = 'lead_source_id'
    customer_color = 'color'
    customer_note = 'note'
    customer_date_from = 'date_from'
    customer_date_to = 'date_to'
    customer_next_lesson_date_from = 'next_lesson_date_from'
    customer_next_lesson_date_to = 'next_lesson_date_to'
    customer_tariff_till_from = 'tariff_till_from'
    customer_tariff_till_to = 'tariff_till_to'
    customer_customer_reject_id = 'customer_reject_id'
    customer_comment = 'comment'
    customer_dob_from = 'dob_from'
    customer_dob_to = 'dob_to'
    customer_withGroups = 'withGroups:true'
    customer_page = 'page'
