# CHI2 values for n degrees freedom
_chiSquared_table = {
        1:3.841,
        2:5.991,
        3:7.815,
        4:9.488,
        5:11.071,
        6:12.592,
        7:14.067,
        8:15.507,
        9:16.919,
        10:18.307
        }

class ChiSquaredException(Exception):
    pass

def chi_squared(actual, expected):
    answerKeys = set(list(actual.keys()) + list(expected.keys()))
    degreesFreedom = len(answerKeys)
    chiSquared = 0

    get_count = lambda k, d : d[k]['count'] if k in d else 0

    for k in answerKeys:
        E = get_count(k, expected)
        O = get_count(k, actual)
        if E == 0:
            print('Warning! Expected 0 counts of {}, but got {}'.format(k, O))
        else:
            chiSquared += (O - E) ** 2 / E
    return degreesFreedom, chiSquared

def chi_squared_test(actual, expected):
    df, chiSquared = chi_squared(actual, expected)

    if chiSquared >= _chiSquared_table[df]:
        print('Significant difference between expected and actual answer distributions: \n' +
            'Chi2 value: {} with {} degrees of freedom'.format(chiSquared, df))
        return False
    return True

def cross_formula_chi_squared(actualDict, expectedDict):
    for ka, actual in actualDict.items():
        for ke, expected in expectedDict.items():
            print('Comparing {} with {}'.format(ka, ke))
            chi_squared_test(actual, expected)

def cross_chi_squared(problemSets):
    for i, problemSetA in enumerate(problemSets):
        for problemSetB in problemSets[i + 1:]:
            for problemA in problemSetA:
                for problemB in problemSetB:
                    if (problemA.initial  == problemB.initial and 
                        problemA.modified == problemB.modified and
                        problemA.target   == problemB.target):
                        answersA = problemA.distributions
                        answersB = problemB.distributions
                        cross_formula_chi_squared(answersA, answersB)

def iso_chi_squared(actualDict, expectedDict):
    for key in expectedDict.keys():
        assert key in actualDict, 'The key {} was not tested'.format(key)
        actual   = actualDict[key]
        expected = expectedDict[key]
        chi_squared_test(actual, expected)
