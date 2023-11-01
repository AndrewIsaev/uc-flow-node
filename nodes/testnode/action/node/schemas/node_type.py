from typing import List

from uc_flow_schemas import flow
from uc_flow_schemas.flow import Defaults, DisplayOptions
from uc_flow_schemas.flow import NodeType as BaseNodeType
from uc_flow_schemas.flow import OptionValue, Property
from nodes.testnode.action.node.schemas.enums import Parameters, CustomerGender, CustomerIsStudy, CustomerLegalType, \
    CustomerRemoved

from nodes.testnode.action.node.schemas.enums import Action, Operation, Resource


class NodeType(flow.NodeType):
    id: str = "ba8ff829-3bb9-460f-afd2-c04eff11fc64"
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = "test_name"
    displayName: str = "TestNode"
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = "test description"
    properties: List[Property] = [
        Property(
            displayName="Выберите действие",
            name="action",
            type=Property.Type.OPTIONS,
            noDataExpression=True,
            options=[
                OptionValue(
                    name="Авторизация",
                    value=Action.authorization,
                    description="Авторизация",
                ),
                OptionValue(
                    name="API",
                    value=Action.api,
                    description="API",
                ),
            ],
        ),
        Property(
            displayName="Адрес CRM",
            name="crm_host",
            type=Property.Type.URL,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.authorization,
                    ],
                },
            ),
        ),
        Property(
            displayName="ID филиала",
            name="office_id",
            type=Property.Type.NUMBER,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.authorization,
                    ],
                },
            ),
        ),
        Property(
            displayName="E-mail",
            name="email",
            type=Property.Type.EMAIL,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.authorization,
                    ],
                },
            ),
        ),
        Property(
            displayName="Ключ API (v2api)",
            name="api_key",
            type=Property.Type.STRING,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.authorization,
                    ],
                },
            ),
        ),
        Property(
            displayName="auth_data",
            name="auth_data",
            type=Property.Type.STRING,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.api,
                    ],
                },
            ),
        ),
        Property(
            displayName="Resource",
            name="resource",
            type=Property.Type.OPTIONS,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.api,
                    ],
                },
            ),
            options=[
                OptionValue(
                    name="Customers",
                    value=Resource.customer,
                    description="Customers",
                ),
            ],
        ),
        Property(
            displayName="Operation",
            name="operation",
            type=Property.Type.OPTIONS,
            noDataExpression=True,
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.api,
                    ],
                    "resource": [
                        Resource.customer
                    ]
                },
            ),
            options=[
                OptionValue(
                    name="Get customers",
                    value=Operation.get_customers,
                    description="Get customers",
                ),
            ],
        ),
        Property(
            displayName='Parameters',
            name='parameters',
            type=Property.Type.COLLECTION,
            default={},
            displayOptions=DisplayOptions(
                show={
                    "action": [
                        Action.api,
                    ],
                    "resource": [
                        Resource.customer
                    ],
                    "operation": [
                        Operation.get_customers
                    ]
                },
            ),
            options=[
                Property(
                    displayName='id',
                    name=Parameters.customer_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='Идентификатор клиента.',
                ),
                Property(
                    displayName='is_study',
                    name=Parameters.customer_is_study,
                    type=Property.Type.OPTIONS,
                    default='',
                    description='Cостояние клиента ( 0 - лид, 1 - клиент)',
                    options=[
                        OptionValue(
                            name='lead',
                            value=CustomerIsStudy.lead,
                            description='лид',
                        ),
                        OptionValue(
                            name='client',
                            value=CustomerIsStudy.client,
                            description='клиент',
                        ),
                    ]
                ),
                Property(
                    displayName='study_status_id',
                    name=Parameters.customer_study_status_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id статуса клиента',
                ),
                Property(
                    displayName='name',
                    name=Parameters.customer_name,
                    type=Property.Type.STRING,
                    default='',
                    description='имя клиента',
                ),
                Property(
                    displayName='gender',
                    name=Parameters.customer_gender,
                    type=Property.Type.OPTIONS,
                    default='',
                    description='пол клиента',
                    options=[
                        OptionValue(
                            name='male',
                            value=CustomerGender.male,
                            description='мужской',
                        ),
                        OptionValue(
                            name='female',
                            value=CustomerGender.female,
                            description='женский',
                        ),
                    ]
                ),
                Property(
                    displayName='age_from',
                    name=Parameters.customer_age_from,
                    type=Property.Type.NUMBER,
                    default='',
                    description='возраст клиента от',
                ),
                Property(
                    displayName='age_to',
                    name=Parameters.customer_age_to,
                    type=Property.Type.NUMBER,
                    default='',
                    description='возраст клиента до',
                ),
                Property(
                    displayName='phone',
                    name=Parameters.customer_phone,
                    type=Property.Type.STRING,
                    default='',
                    description='контакты клиента',
                ),
                Property(
                    displayName='legal_type',
                    name=Parameters.customer_legal_type,
                    type=Property.Type.OPTIONS,
                    default='',
                    description='тип заказчика(1-физ лицо, 2-юр.лицо)',
                    options=[
                        OptionValue(
                            name='physical_person',
                            value=CustomerLegalType.physical_person,
                            description='физ лицо',
                        ),
                        OptionValue(
                            name='legal_person',
                            value=CustomerLegalType.legal_person,
                            description='юр.лицо',
                        ),
                    ]
                ),
                Property(
                    displayName='legal_name',
                    name=Parameters.customer_legal_name,
                    type=Property.Type.STRING,
                    default='',
                    description='имя заказчика',
                ),
                Property(
                    displayName='company_id',
                    name=Parameters.customer_company_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id юр лица',
                ),
                Property(
                    displayName='lesson_count_from',
                    name=Parameters.customer_lesson_count_from,
                    type=Property.Type.NUMBER,
                    default='',
                    description='остаток уроков от',
                ),
                Property(
                    displayName='lesson_count_to',
                    name=Parameters.customer_lesson_count_to,
                    type=Property.Type.NUMBER,
                    default='',
                    description='остаток уроков до',
                ),
                Property(
                    displayName='balance_contract_from',
                    name=Parameters.customer_balance_contract_from,
                    type=Property.Type.NUMBER,
                    default='',
                    description='баланс договора от',
                ),
                Property(
                    displayName='balance_contract_to',
                    name=Parameters.customer_balance_contract_to,
                    type=Property.Type.NUMBER,
                    default='',
                    description='баланс договора до',
                ),
                Property(
                    displayName='balance_bonus_from',
                    name=Parameters.customer_balance_bonus_from,
                    type=Property.Type.NUMBER,
                    default='',
                    description='баланс бонусов от',
                ),
                Property(
                    displayName='balance_bonus_to',
                    name=Parameters.customer_balance_bonus_to,
                    type=Property.Type.NUMBER,
                    default='',
                    description='баланс бонусов до',
                ),
                Property(
                    displayName='removed',
                    name=Parameters.customer_removed,
                    type=Property.Type.OPTIONS,
                    default='',
                    description='флаг архивности (2 - только архивные, 1 - активные и архивные, 0 – только активные)',
                    options=[
                        OptionValue(
                            name='archived',
                            value=CustomerRemoved.archived,
                            description='только архивные',
                        ),
                        OptionValue(
                            name='active and archived',
                            value=CustomerRemoved.active_and_archived,
                            description='активные и архивные',
                        ),
                        OptionValue(
                            name='active',
                            value=CustomerRemoved.active,
                            description='только активные',
                        ),
                    ]
                ),
                Property(
                    displayName='removed_from',
                    name=Parameters.customer_removed_from,
                    type=Property.Type.DATE,
                    default='',
                    description='дата отправки в архив от, date',
                ),
                Property(
                    displayName='removed_to',
                    name=Parameters.customer_removed_to,
                    type=Property.Type.DATE,
                    default='',
                    description='дата отправки в архив до, date',
                ),
                Property(
                    displayName='level_id',
                    name=Parameters.customer_level_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id уровня знаний',
                ),
                Property(
                    displayName='assigned_id',
                    name=Parameters.customer_assigned_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id ответственного менеджера',
                ),
                Property(
                    displayName='employee_id',
                    name=Parameters.customer_employee_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id ответственного педагога',
                ),
                Property(
                    displayName='lead_source_id',
                    name=Parameters.customer_lead_source_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id источника',
                ),
                Property(
                    displayName='color',
                    name=Parameters.customer_color,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id цвета',
                ),
                Property(
                    displayName='note',
                    name=Parameters.customer_note,
                    type=Property.Type.STRING,
                    default='',
                    description='примечание, string',
                ),
                Property(
                    displayName='date_from',
                    name=Parameters.customer_date_from,
                    type=Property.Type.DATE,
                    default='',
                    description='дата добавления от, date',
                ),
                Property(
                    displayName='date_to',
                    name=Parameters.customer_date_to,
                    type=Property.Type.DATE,
                    default='',
                    description='дата добавления до, date',
                ),
                Property(
                    displayName='next_lesson_date_from',
                    name=Parameters.customer_next_lesson_date_from,
                    type=Property.Type.DATE,
                    default='',
                    description='дата след.посещения от',
                ),
                Property(
                    displayName='next_lesson_date_to',
                    name=Parameters.customer_next_lesson_date_to,
                    type=Property.Type.DATE,
                    default='',
                    description='дата след.посещения до',
                ),
                Property(
                    displayName='tariff_till_from',
                    name=Parameters.customer_tariff_till_from,
                    type=Property.Type.DATE,
                    default='',
                    description='дата действия абонемента от',
                ),
                Property(
                    displayName='tariff_till_to',
                    name=Parameters.customer_tariff_till_to,
                    type=Property.Type.DATE,
                    default='',
                    description='дата действия абонемента до',
                ),
                Property(
                    displayName='customer_reject_id',
                    name=Parameters.customer_customer_reject_id,
                    type=Property.Type.NUMBER,
                    default='',
                    description='id причины отказа',
                ),
                Property(
                    displayName='comment',
                    name=Parameters.customer_comment,
                    type=Property.Type.STRING,
                    default='',
                    description='комментарий',
                ),
                Property(
                    displayName='dob_from',
                    name=Parameters.customer_dob_from,
                    type=Property.Type.DATE,
                    default='',
                    description='дата рождения от',
                ),
                Property(
                    displayName='dob_to',
                    name=Parameters.customer_dob_to,
                    type=Property.Type.DATE,
                    default='',
                    description='дата рождения до',
                ),
                Property(
                    displayName='withGroups:true',
                    name=Parameters.customer_withGroups,
                    type=Property.Type.STRING,
                    default='',
                    description='активные группы клиента',
                ),
                Property(
                    displayName='page',
                    name=Parameters.customer_page,
                    type=Property.Type.NUMBER,
                    default='',
                    description='номер страницы',
                ),
            ]
        ),
    ]
