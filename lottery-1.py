import pandas


def Read():
    lottery_all_df = pandas.read_csv('eurojackpot.csv', engine='pyarrow', sep=';', header=None, dtype_backend='pyarrow')
    lottery_all_df = lottery_all_df.loc[:, [3, 28, 29, 30, 31, 32, 33, 34]]  # drop out the useless columns
    field_a = lottery_all_df.loc[:, [28, 29, 30, 31, 32]]
    field_b = lottery_all_df.loc[:, [33, 34]]
    field_a.rename(columns={28: 'A_1', 29: 'A_2', 30: 'A_3', 31: 'A_4', 32: 'A_5'}, inplace=True)
    field_b.rename(columns={33: 'B_1', 34: 'B_2'}, inplace=True)
    return field_a, field_b


def Field_A(field_a):
    field_a['A_list'] = field_a.values.tolist()
    a_1_count = field_a['A_1'].value_counts()
    a_2_count = field_a['A_2'].value_counts()
    a_3_count = field_a['A_3'].value_counts()
    a_4_count = field_a['A_4'].value_counts()
    a_5_count = field_a['A_5'].value_counts()
    for_excel_A = pandas.concat([a_1_count, a_2_count, a_3_count, a_4_count, a_5_count], axis=1)
    for_excel_A.fillna(0, inplace=True)
    for_excel_A.reset_index(inplace=True)
    for_excel_A.columns = ['Lott_num_A', 'First', 'Second', 'Third', 'Fourth', 'Fifth']
    for_excel_A = for_excel_A.eval('Sum = First + Second + Third + Fourth + Fifth')
    for_excel_A['Percentage'] = (for_excel_A["Sum"] / sum(for_excel_A['Sum']) * 100).round(decimals=2)
    return for_excel_A


def Field_B(field_b):
    field_b['b_list'] = field_b.values.tolist()
    b_1_count = field_b['B_1'].value_counts()
    b_2_count = field_b['B_2'].value_counts()
    for_excel_B = pandas.concat([b_1_count, b_2_count], axis=1)
    for_excel_B.fillna(0, inplace=True)
    for_excel_B.reset_index(inplace=True)
    for_excel_B.columns = ['Lott_num_B', 'First', 'Second']
    for_excel_B = for_excel_B.eval('Sum = First + Second')
    for_excel_B['Percentage'] = (for_excel_B["Sum"] / sum(for_excel_B['Sum']) * 100).round(decimals=2)
    return for_excel_B


#pandas.options.display.float_format = '{:.2f} %'.format

field_a, field_b = Read()
into_excel_A = Field_A(field_a)
into_excel_B = Field_B(field_b)

into_excel_A.sort_values('Lott_num_A', inplace=True)
into_excel_B.sort_values('Lott_num_B', inplace=True)


# for_excel.rename(columns= {list(for_excel)[0] : f"{1}. num"}, inplace=True)
# it doesnt work on same names, but good if need to rename many columns

print(into_excel_A)
print(into_excel_B)



into_excel_A.to_excel('eurojack_count_A.xlsx', index=None)
into_excel_B.to_excel('eurojack_count_B.xlsx', index=None)
#for_excel.to_excel('eurojack_count_field_B.xlsx')