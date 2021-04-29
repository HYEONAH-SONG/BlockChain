from django.shortcuts import render
from .models import UploadFileModel
from .forms import TransactionForm
from django.http import JsonResponse
from django.http import HttpResponse
import sys
import math
import json
import re

cnt = 1
fileName_Num =1
num_list = [1]
info_list = []
whole_fun_list = []
func_cnt = 0
func_list =[]
dict_index = {'cost' : {'function': {'code_line_cost' : '', 'control_statement_cost' : '', 'data_process_cost' : ''}}}
code_line_cost = "code_line_cost"
control_statement_cost = "control_statement_cost"
data_process_cost = "data_process_cost"

# Create your views here.

# upload.html 출력
def upload(request):
    return render(request, 'upload.html')

# 파일 업로드하면 /media 폴더내에 파일 업로드
def upload_file(request): 
    uploadfile = UploadFileModel()
    uploadfile.func_file=request.FILES['func_file']
    print(uploadfile)
    uploadfile.save()

    # web을 통해 받은 file 열기
    f = open("media/input.txt", 'r')
    f2 = open("media/input.txt", 'r')    
    sen = f.read()
    lines = f2.readlines()
    f.close()
    global fileName_Num
    global cnt
    global num_list
    global info_list
    global whole_fun_list
    global func_cnt
    global func_list
    word = 'func '



    for index,line in enumerate(lines):
        if index < len(lines)-1:

            fileName = 'media/function'+ str(fileName_Num)+'.txt'

            fw = open(fileName,"a")
            fw.write(line)
            fw.close()

            if word in lines[index+1] and 'main' not in lines[index+1]:
                fileName_Num = fileName_Num +1
                num_list.append(fileName_Num)
                cnt = 0
            cnt +=1

    sen_list =re.split(r'[}:{]',sen) 

    for index, i in enumerate(sen_list):
        if word in i:
            b= re.split(r'[(:)]',i)
            if len(b)==5:
                func_list.append(b[2])
            else:
                m = b[0].split(' ')[1]
                if m != "main":
                    func_list.append(m)
    print(func_list)

    for i in num_list:
        fileName = 'media/function' + str(i) + '.txt'
        func_cnt = func_cnt+1
        fw = open(fileName, "r")
        print("function",i)
        fun_weight(fw)
        info_list.append(i)
        whole_fun_list.append(info_list)
        info_list =[]
        fw.close()

    print(whole_fun_list)
    transaction_sorted = sorted(whole_fun_list, key = lambda x:(x[3],x[2],x[1],x[0]))

    print(transaction_sorted)

     # 토탈 코스트 : transaction_sorted[i][3]
    # 코드 라인 : transaction_sorted[i][0]
    # 반복문 수 : transaction_sorted[i][1]
    # 데이터 처리 비용: transaction_sorted[i][2]
    # 트랜잭션 함수명 : transaction_sorted[i][4]


    # transaction_sorted[i][4]의 값을 가지고 func_list 참조

 # 인덱스 파일 생성
    dict_index = {'cost' : {'function': {'code_line_cost' : '', 'control_statement_cost' : '', 'data_process_cost' : ''}}}
    code_line_cost = "code_line_cost"
    control_statement_cost = "control_statement_cost"
    data_process_cost = "data_process_cost"


    for i in range (1, func_cnt+1):
        str_total_cost = str(transaction_sorted[i-1][3])
        str_code_line = str(transaction_sorted[i-1][0])
        str_iteration = str(transaction_sorted[i-1][1])
        str_data = str(transaction_sorted[i-1][2])
        transaction_sorted_index = transaction_sorted[i-1][4] -1 # 인덱스 참고하기 위해

        index_cost = {'function': {'code_line_cost' : '', 'control_statement_cost' : '', 'data_process_cost' : ''}} #cost 다를 때, 키 cost의 value값 초기화해주기 위해
        index_func = {'code_line_cost' : '', 'control_statement_cost' : '', 'data_process_cost' : ''} #cost같을 때, 키 func의 value값 초기화해주기 위해
        
      
        chg_str_total_cost = "cost" + str_total_cost 
        chg_str_func_name = func_list[transaction_sorted_index]

        if (i == 1):
            dict_index[chg_str_total_cost] = dict_index.pop('cost')
            dict_index[chg_str_total_cost][chg_str_func_name] = dict_index[chg_str_total_cost].pop('function')

            dict_index[chg_str_total_cost][chg_str_func_name][code_line_cost] =  str_code_line
            dict_index[chg_str_total_cost][chg_str_func_name][control_statement_cost] = str_iteration
            dict_index[chg_str_total_cost][chg_str_func_name][data_process_cost] = str_data


        
        else:
            previous_total_cost = transaction_sorted[i-2][3] #이전 cost와 비교하기 위해
            if transaction_sorted[i-1][3] ==  previous_total_cost : #이전 cost와 같을 때
                
                dict_index[chg_str_total_cost][chg_str_func_name] = index_func #새로운 func 키를 생성

                dict_index[chg_str_total_cost][chg_str_func_name][code_line_cost] =  str_code_line
                dict_index[chg_str_total_cost][chg_str_func_name][control_statement_cost] = str_iteration
                dict_index[chg_str_total_cost][chg_str_func_name][data_process_cost] = str_data

            else: #이전 cost와 다를 때
                dict_index[chg_str_total_cost] = index_cost
                dict_index[chg_str_total_cost][chg_str_func_name] = dict_index[chg_str_total_cost].pop('function')


                dict_index[chg_str_total_cost][chg_str_func_name][code_line_cost] =  str_code_line
                dict_index[chg_str_total_cost][chg_str_func_name][control_statement_cost] = str_iteration
                dict_index[chg_str_total_cost][chg_str_func_name][data_process_cost] = str_data
    

    json_index = json.dumps(dict_index, indent=4, sort_keys=False)  #cost를 기준으로 sorting된 function
    print(json_index)

    index_file_name = 'media/sorted_index_file'+'.json'
    f_index_file = open(index_file_name, "w")
    f_index_file.write(json_index)
    f_index_file.close()
    
    form = TransactionForm()
    return render(request, 'show2.html', {'form' : form})
    # return HttpResponse(json_index,content_type="application/json")
    # return render(request, 'show.html',{'code_line1': whole_fun_list[0][0], 'iteration1':whole_fun_list[0][1] , 'data_cost1': whole_fun_list[0][2], 'total_cost1': whole_fun_list[0][3],'code_line2': whole_fun_list[1][0], 'iteration2':whole_fun_list[1][1] , 'data_cost2': whole_fun_list[1][2], 'total_cost2':whole_fun_list[1][3] ,'code_line3':whole_fun_list[2][0] , 'iteration3': whole_fun_list[2][1], 'data_cost3': whole_fun_list[2][2], 'total_cost3':whole_fun_list[2][3],'first_fun':transaction_sorted[0][4], 'second_fun':transaction_sorted[1][4], 'third_fun':transaction_sorted[2][4], 'sorted_first_line':transaction_sorted[2][0],'sorted_first_iteration':transaction_sorted[2][1],'sorted_first_data':transaction_sorted[2][2], 'sorted_first_total':transaction_sorted[2][3],'sorted_second_line':transaction_sorted[1][0],'sorted_second_iteration':transaction_sorted[1][1],'sorted_second_data':transaction_sorted[1][2], 'sorted_second_total':transaction_sorted[1][3],'sorted_third_line':transaction_sorted[0][0],'sorted_third_iteration':transaction_sorted[0][1],'sorted_third_data':transaction_sorted[0][2], 'sorted_third_total':transaction_sorted[0][3]})


def fun_weight(code):
    # initialized variables
    total,weight = 0, 0
    count_line = 0
    if_count,for_count, while_count,switch_count= 0,0,0,0
    G,P,M,U =0,0,0,0

    code_list = list(enumerate(code))
    count_line = code_list[-1][0]+1
    print('코드의 라인 수 :', count_line)
    word1,word2,word3,word4 = 'if','for','while','switch'
    data1,data2, data3, data4 = 'GetState','PutState','Marshal','Unmarshal'

    # count variable cost
    for i in code_list:
        if word1 in i[1]:
            if_count+=1
        elif word2 in i[1]:
            for_count+=1
        elif word3 in i[1]:
            while_count+=1
        elif word4 in i[1]:
            switch_count+=1
        elif data1 in i[1]:
            G+=1
        elif data2 in i[1]:
            P+=1
        elif data3 in i[1]:
            M+=1
        elif data4 in i[1]:
            U+=1

    code_line_cost = math.ceil(count_line/50)
    iteration_cost = if_count + for_count + switch_count + while_count
    data_cost = G+P+M+U
    total = code_line_cost + iteration_cost + data_cost
    # weight = code_line_cost + iteration_cost*2 + data_cost*3
    
    # output printing
    print('if문의 수 :', if_count)
    print('for문의 수 :', for_count)
    print('while문의 수 :', while_count)
    print('switch문의 수 :', switch_count)
    print('GetState:', G)
    print('PutState:', P)
    print('Marshal:', M)
    print('Unmarshal:', U)
    print('Total Execution Cost :',total)
    print('—————————————————————————')

    info_list.append(code_line_cost)
    info_list.append(iteration_cost)
    info_list.append(data_cost)
    info_list.append(total)

    return total

def sorting_func(request):

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            trans1 = form.cleaned_data['Transaction1']
            trans2 = form.cleaned_data['Transaction2']
            trans3 = form.cleaned_data['Transaction3']
         
        print(trans1, trans2, trans3)

    

    f = open("media/sorted_index_file.json", 'r')
    index = f.read()

    print(index)

    dic_index = json.loads(index)
    
    trans1_list = []
    trans2_list = []
    trans3_list = []

    ans = []

    for i in dic_index:
        index_key = list(dic_index[i].keys())  # cost안에 있는 function name

        if trans1 in index_key:
            ans.append(dic_index[i][trans1][code_line_cost])
            trans1_list.append(dic_index[i][trans1][code_line_cost])
            ans.append(dic_index[i][trans1][control_statement_cost])
            trans1_list.append(dic_index[i][trans1][control_statement_cost])
            ans.append(dic_index[i][trans1][data_process_cost])
            trans1_list.append(dic_index[i][trans1][data_process_cost])
            ans.append(i)
            trans1_list.append(i)
            ans.append(trans1)
            trans1_list.append(trans1)
           

        if trans2 in index_key:
            ans.append(dic_index[i][trans2][code_line_cost]) 
            ans.append(dic_index[i][trans2][control_statement_cost])
            ans.append(dic_index[i][trans2][data_process_cost])
            ans.append(i)
            ans.append(trans2)
            trans2_list.append(dic_index[i][trans2][code_line_cost])
            trans2_list.append(dic_index[i][trans2][control_statement_cost])
            trans2_list.append(dic_index[i][trans2][data_process_cost])
            trans2_list.append(i)
            trans2_list.append(trans2)


        if trans3 in index_key:
            ans.append(dic_index[i][trans3][code_line_cost]) 
            ans.append(dic_index[i][trans3][control_statement_cost])
            ans.append(dic_index[i][trans3][data_process_cost])
            ans.append(i)
            ans.append(trans3)
            trans3_list.append(dic_index[i][trans3][code_line_cost])
            trans3_list.append(dic_index[i][trans3][control_statement_cost])
            trans3_list.append(dic_index[i][trans3][data_process_cost])
            trans3_list.append(i)
            trans3_list.append(trans3)
            


    


    print(ans)

    form = TransactionForm()

    return render(request, 'show.html',{'code_line1': trans1_list[0],'iteration1':trans1_list[1], 'data_cost1': trans1_list[2], 'total_cost1': trans1_list[3], 'func_name1': trans1_list[4],'code_line2': trans2_list[0],'iteration2':trans2_list[1], 'data_cost2': trans2_list[2], 'total_cost2': trans2_list[3], 'func_name2': trans2_list[4],'code_line3': trans3_list[0],'iteration3':trans3_list[1], 'data_cost3': trans3_list[2] ,'total_cost3': trans3_list[3], 'func_name3': trans3_list[4],  'first_fun':ans[4], 'second_fun':ans[9], 'third_fun':ans[14], 'sorted_first_line':ans[10],'sorted_first_iteration':ans[11],'sorted_first_data':ans[12], 'sorted_first_total':ans[13],'sorted_second_line':ans[5],'sorted_second_iteration':ans[6],'sorted_second_data':ans[7], 'sorted_second_total':ans[8],'sorted_third_line':ans[0],'sorted_third_iteration':ans[1],'sorted_third_data':ans[2], 'sorted_third_total':ans[3]})