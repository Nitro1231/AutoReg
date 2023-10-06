from AutoReg import WebSoc
from collections import defaultdict, OrderedDict

classes = {
    'COMPSCI': {'163', '166', '169', '145', '147', '184A', '184C', '175', '178', '125', '134', '183'},
    'BIO SCI': {'93'}
}

years = ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016']


w = WebSoc.WebSoc()

option = w.get_option_info()

out = defaultdict(lambda: defaultdict(lambda: list()))

for dept, nums in classes.items():
    w.set_option('Dept', dept)
    w.set_course_numbers(nums)

    for term, disc in option['YearTerm']:
        for year in years:
            if 'Quarter' in disc and year in term:
                print(term, disc)
                w.set_option('YearTerm', term)

                for c in w.get_course_info():
                    name = c['course']['case'] + ' ' + c['course']['number'] + ' - ' + c['course']['title']
                    q = disc[6:]
                    if q not in out[name][year]:
                        out[name][year].append(q)

w.save_json(out, 'prev_offers.json')
