import file_p
from toolkit import errorProcess

# file_p.getExifOrientation()

a=errorProcess(debug=True)
for i in range(0,3):
    a.add_show(i,'',FileExistsError)
print('===')
a.show_all_type()
exit(a.error_code())
#print(np.array([1,1])*5)