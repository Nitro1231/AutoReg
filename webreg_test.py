import configparser
from AutoReg import *


config = configparser.ConfigParser()
config.read('user.key')
user_id, user_pw = config['user']['id'], config['user']['pw']
print('[UCI LOGIN INFO]', user_id, user_pw)


webreg = WebReg()
webreg.login(user_id, user_pw)
# webreg.enrollment_window()
# webreg.fee_status()
# webreg.study_list()
# webreg.wait_list()

webreg.requests_waitlist(Course(34070, Mode.ADD))
webreg.wait_list()
webreg.requests_waitlist(Course(34070, Mode.DROP))
webreg.wait_list()

# webreg.requests_course(Course(34070, Mode.ADD))
# webreg.study_list()
# webreg.requests_course(Course(34070, Mode.DROP))
# webreg.study_list()
webreg.logout()

# webreg.study_list()
# webreg.wait_list()

# print('=' * 20)
# webreg.study_list()
# webreg.wait_list()
# webreg.requests_waitlist(Course(34070, Mode.ADD))
# print('=' * 20)
# webreg.study_list()
# webreg.wait_list()
# print('=' * 20)
# webreg.requests_waitlist(Course(34070, Mode.DROP))
# webreg.study_list()
# webreg.wait_list()

# webreg.study_list()
# webreg.requests_course(Course(34040, Mode.DROP)) # CS 117
# webreg.study_list()

# webreg.logout()

# show study list:
#    Crse           Crse     Sec      Grd                      
#    Code  Dept    Num  Typ Num Unts Opt Days   Time          Bldg Room
#    34190 COMPSCI   147 LEC   A  4.0  GR        T   05:00-07:50pm SH   174       
#    34191 COMPSCI   147 LAB 1    0.0  GR         F  02:00-02:50   ICS2 162       
#    34200 COMPSCI   151 LEC   A  4.0  GR      T     06:30-09:20pm DBH  1200      
#    34201 COMPSCI   151 DIS   1  0.0  GR     M      02:00-02:50   ICS  180       
#    34340 COMPSCI   178 LEC A    4.0  GR     M W F  10:00-10:50   ELH  100       
#    34343 COMPSCI   178 DIS 3    0.0  GR         F  03:00-03:50   SH   174       
#    34370 COMPSCI  184A LEC A    4.0  GR     M W    08:00-09:20   SSL  140       
                                                                                
#           total units enrolled 16.0       0.0 p/np units 

# ADD/DROP
#  You have SUCCESSFULLY DROPPED                                                   
                


 
#    Crse           Crse     Sec      Grd                      
#    Code  Dept    Num  Typ Num Unts Opt Days   Time          Bldg Room
#    34040 COMPSCI   117 LEC   A  4.0  GR      T T   12:30-01:50   ICS  174 
