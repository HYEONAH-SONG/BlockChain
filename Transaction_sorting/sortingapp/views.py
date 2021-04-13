from django.shortcuts import render
# from .forms import UploadFileForm
from .models import UploadFileModel
import sys
import math


cnt = 1
fileName_Num =1
num_list = [1]
info_list = []
whole_fun_list = []

# Create your views here.

# upload.html 출력
def upload(request):
    return render(request, 'upload.html')


# 파일 업로드하면 /media 폴더내에 파일 업로드
def upload_file(request): 
    print("comein")
    uploadfile = UploadFileModel()
    uploadfile.func_file=request.FILES['func_file']
    print(uploadfile)
    uploadfile.save()

    # web을 통해 받으 file 열기
    f = open("media/input.txt", 'r')
    lines = f.readlines()
    f.close()

    global fileName_Num
    global cnt
    global num_list
    global info_list
    global whole_fun_list


    word = 'func '
    for index,line in enumerate(lines):
        if index < len(lines)-1:

            fileName = 'function'+ str(fileName_Num)+'.txt'

            fw = open(fileName,"a")
            fw.write(line)
            fw.close()

            if word in lines[index+1] :
                fileName_Num = fileName_Num +1
                num_list.append(fileName_Num)
                cnt = 0
            cnt +=1

    for i in num_list:
        fileName = 'function' + str(i) + '.txt'
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
    


    return render(request, 'show.html',{'code_line1': whole_fun_list[0][0], 'iteration1':whole_fun_list[0][1] , 'data_cost1': whole_fun_list[0][2], 'total_cost1': whole_fun_list[0][3],'code_line2': whole_fun_list[1][0], 'iteration2':whole_fun_list[1][1] , 'data_cost2': whole_fun_list[1][2], 'total_cost2':whole_fun_list[1][3] ,'code_line3':whole_fun_list[2][0] , 'iteration3': whole_fun_list[2][1], 'data_cost3': whole_fun_list[2][2], 'total_cost3':whole_fun_list[2][3],'first_fun':transaction_sorted[0][4], 'second_fun':transaction_sorted[1][4], 'third_fun':transaction_sorted[2][4],'third_line':transaction_sorted[2][0],'third_interation':transaction_sorted[2][1],'third_data':transaction_sorted[2][2], 'third_total':transaction_sorted[2][3],'seconde_line':transaction_sorted[1][0],'third_interation':transaction_sorted[1][1],'third_data':transaction_sorted[1][2], 'second_total':transaction_sorted[1][3],'first_line':transaction_sorted[0][0],'first_interation':transaction_sorted[0][1],'first_data':transaction_sorted[0][2], 'first_total':transaction_sorted[0][3]})




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
    print('--------------------------------------------------')

    info_list.append(code_line_cost)
    info_list.append(iteration_cost)
    info_list.append(data_cost)
    info_list.append(total)

    return total




