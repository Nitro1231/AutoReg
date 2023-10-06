from AutoReg import WebSoc

w = WebSoc.WebSoc()
opt = w.get_option_info()

w.set_option('YearTerm', opt['SelectedYearTerm'])
w.set_option('Submit', 'Display Text Results')

w.set_course_codes({34050, 34053, 34080, 34100, 34220, 34222, 34270, 38495, 33301})
w.save_file(w.get_websoc_request().decode('utf-8'), 'websoc_request.txt')
w.save_file(w.get_raw_xml_course_info().decode('utf-8'), 'raw_xml_course_info.xml')
w.save_json(w.get_raw_json_course_info(), 'raw_json_course_info.json')
w.save_json(w.get_course_info(), 'course_info.json')
w.save_json(w.get_option_info(), 'option_info.json')

list_all = list()

for d in opt['Dept']:
    w.set_option('Dept', d[0])
    print(d[0])
    list_all.append(w.get_course_info())

w.save_json({'list': list_all}, 'course_info_all.json')
