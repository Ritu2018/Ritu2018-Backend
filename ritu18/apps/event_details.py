CSE = 'CSE'
ECE = 'ECE'
EEE = 'EEE'
MECH = 'MEC'
CIVIL = 'CVL'
MCA = 'MCA'
BARCH = 'BAR'
TINKERHUB = 'TNK'
BOOTCAMP = 'BTC'
GENERAL = 'GEN'
FILIM_CLUB = 'FLM'

# EVENT TYPES

WORKSHOP = 'Workshop'
COMPETITION = 'Competition'

# FIELDS

NAME = 'name'
AMOUNT = 'amount'
TYPE = 'type'

event_details = {

    #WORKSHOPS
    CSE+'W01': {
        NAME:'Web Development Workshop',
        AMOUNT: '1',
        TYPE: WORKSHOP
        # 17 feb
    },
    CSE+'W02': {
        NAME:'Machine Learning Workshop',
        AMOUNT: '2',
        TYPE: WORKSHOP
    },
    CSE+'W03': {
        NAME:'Computer Vision Workshop',
        AMOUNT:'1',
        TYPE:WORKSHOP
    },

    ECE+'W01': {
        NAME: 'CCNA',
        AMOUNT: '400',
        TYPE:WORKSHOP,
        # 28 Feb
    },

    TINKERHUB+'W01': {
        NAME: 'Android',
        AMOUNT: '300',
        TYPE: WORKSHOP
        # 28 Feb
    },

    TINKERHUB+'W02': {
        NAME: 'Machine Learning',
        AMOUNT: '400',
        TYPE: WORKSHOP,
        # 1 Mar
    },

    MECH+'W01': {
        NAME: 'RC Aircraft Workshop',
        AMOUNT: '1200',
        TYPE: WORKSHOP,
        # 28 Feb 1 Mar
    },

    MECH+'W02': {
        NAME: 'Plathora',
        AMOUNT: '1000',
        TYPE: WORKSHOP,
        # 28 Feb
    },

    #EVENTS

}

