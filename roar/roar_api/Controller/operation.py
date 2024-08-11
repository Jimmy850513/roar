
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.shortcuts import render
from ..Models.active_models import Active_Category_Unit,Active_Information,Active_Show_Information
from django.template.response import TemplateResponse
from django.utils.timezone import make_aware
from datetime import datetime
from rest_framework import status
class Index(TemplateView):
    template_name = 'index.html'
    def get(self,request,*args,**kwargs):
        username = request.session.get('username')
        login_status = request.session.get('login_status',False)
        active_info = Active_Information.objects.filter(is_deleted=0).values()
        active_info_list = list(active_info)
        
        template_dict = dict(
            login_status=login_status,
            data_ld = active_info_list
        )
        return render(request,self.template_name,template_dict)


class Operation(APIView):
    def get(self, request, *args, **kwargs):
        u_id = self.kwargs.get('UID')
        username = request.session.get('username')
        login_status = request.session.get('login_status',False)
        print(u_id)  # 打印 UID 或进行其他处理
        try:
            active_show_info = list(Active_Show_Information.objects.filter(active_info_id=u_id).values())
            active_category_unit = list(Active_Category_Unit.objects.filter(active_id=u_id).values())
            active_info = Active_Information.objects.filter(id=u_id).values('id','title','start_date','end_date','active_description',
                                                                            'active_promo_image')
            data_dict = dict()
            show_data = list()
            for data in active_show_info:
                data['show_start_time'] = data['show_start_time'].strftime('%Y-%m-%d %H:%M:%S')
                data['show_end_time'] = data['show_end_time'].strftime('%Y-%m-%d %H:%M:%S')
                if data['on_sale']:
                    data['on_sale'] = '是'
                else:
                    data['on_sale'] = '否'

            for data in active_info:
                data_dict[data['id']] = {
                    'title':data['title'],
                    'start_date':data['start_date'].strftime('%Y-%m-%d'),
                    'end_date':data['end_date'].strftime('%Y-%m-%d'),
                    'active_description':data['active_description'],
                    'active_promo_image':data['active_promo_image'],
                    'show_unit':'',
                    'master_unit':'',
                    'sub_unit':'',
                    'support_unit':'',
                    'other_unit':'',
                    'show_data':active_show_info
                }
            for data in active_category_unit:
                if data['active_id'] in data_dict:
                    data_dict[data['active_id']]['show_unit'] += data['show_unit'] if data['show_unit'] else "暫無演出單位"
                    data_dict[data['active_id']]['master_unit'] += data['master_unit'] if data['master_unit'] else "暫無主辦單位"
                    data_dict[data['active_id']]['sub_unit'] += data['sub_unit'] if data['sub_unit'] else "暫無協辦單位"
                    data_dict[data['active_id']]['support_unit'] += data['support_unit'] if data['support_unit'] else "暫無贊助單位"
                    data_dict[data['active_id']]['other_unit'] += data['other_unit'] if data['other_unit'] else "暫無其他單位"
            msg = '資料匹配'
            status_code = status.HTTP_200_OK
        except Exception as e:
            print(e)
            msg = '找不到資料'
            status_code = status.HTTP_404_NOT_FOUND
        print(data_dict)
        template_dict = dict(
            uid = u_id,
            data_ld = data_dict,
            username=username,
            login_status=login_status,
            msg=msg,
            status_code=status_code
        )
        return TemplateResponse(request, 'operator.html', template_dict)
    
    def patch(self,request,*args,**kwargs):
        u_id = self.kwargs.get('UID')
        username = request.session.get('username')
        login_status = request.session.get('login_status',False)
        data_form = request.data
        op = data_form.get("fmTextOP2")
        print(data_form)
        if op == 'update_show':
            try:
                """
                {
                'show_start_time': '2024-08-10 00:00:00', 
                'show_end_time': '2024-08-10 00:00:00'
                'show_location': '台北捷運音樂進站', 
                'show_location_addr': '臺北市中山站 4 號出口心中山舞臺、東區地下街第 2 廣場、
                大安森林公園站陽光大廳、松山站穹頂廣場、新店站廣場', 
                'on_sale': '是', 
                'price': '一張票200', 
                'fmTextOP2': 'update_show'}
                """
                show_id = data_form.get('show_id')
                show_start_time = data_form.get('show_start_time')
                show_end_time = data_form.get('show_end_time')
                # show_start_time = make_aware(datetime.strptime(show_start_time_str,'%Y-%m-%d %H:%M:%S'))
                # show_end_time = make_aware(datetime.strptime(show_end_time_str,'%Y-%m-%d %H:%M:%S'))
                show_location = data_form['show_location']
                show_location_addr = data_form['show_location_addr']
                on_sale = 1 if data_form['on_sale'] == '是' else 0
                price = data_form['price']
                data_ld = Active_Show_Information.objects.filter(id=show_id).update(
                    show_start_time=show_start_time,
                    show_end_time=show_end_time,
                    show_location=show_location,
                    show_location_addr=show_location_addr,
                    on_sale=on_sale,
                    price=price
                    )
                if data_ld!=0:
                    msg = '表演資訊更新成功'
                    status_msg = "OK"
                    status_code = status.HTTP_200_OK
                else:
                    msg = '找不到匹配的資料'
                    status_msg = "ERROR"
                    status_code = status.HTTP_404_NOT_FOUND
            except Exception as e:
                msg='表演資訊更新失敗'
                status_msg = "ERROR"
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                print(e)
        elif op == 'update_active':
            try:
                title = data_form.get('title')
                start_date = data_form.get('start_date')
                active_description = data_form.get('active_description')
                end_date = data_form.get('end_date')
                show_unit = data_form['show_unit'] if data_form['show_unit'] != '暫無演出單位' else ''
                master_unit = data_form['master_unit'] if data_form['master_unit'] !="暫無主辦單位" else ''
                sub_unit = data_form['sub_unit'] if data_form['sub_unit']!='暫無協辦單位' else ''
                support_unit = data_form['support_unit'] if data_form['support_unit'] !='暫無贊助單位' else ''
                other_unit = data_form['other_unit'] if data_form['other_unit']!='暫無其他單位' else ''

                data_ld = Active_Information.objects.filter(id=u_id).update(title=title,
                                                                            start_date=start_date,
                                                                            end_date=end_date,
                                                                            active_description=active_description
                                                                            )
                data_ld2 = Active_Category_Unit.objects.filter(active_id=u_id).update(show_unit=show_unit,
                                                                               master_unit=master_unit,
                                                                               sub_unit=sub_unit,
                                                                               support_unit=support_unit,
                                                                               other_unit=other_unit
                                                                               )
                if data_ld!=0 and data_ld2!=0:
                    msg = '活動資訊更新成功'
                    status_msg = "OK"
                    status_code = status.HTTP_200_OK
                else:
                    msg='未找到匹配的對象'
                    status_msg = "ERROR"
                    status_code = status.HTTP_404_NOT_FOUND
            except Exception as e:
                msg = f'活動資訊更新失敗,發生異常:{e}'
                status_msg = "ERROR"
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        ret_json = dict(data={'msg':msg,'status_msg':status_msg,'status_code':status_code})
        return Response(ret_json)

    def delete(self,request,*args,**kwargs):
        u_id = self.kwargs.get('UID')
        username = request.session.get('username')
        login_status = request.session.get('login_status',False)
        try:
            data_ld = Active_Information.objects.filter(id=u_id).update(is_deleted=1)
            data_ld2 = Active_Category_Unit.objects.filter(active_id=u_id).update(is_deleted=1)
            data_ld3 = Active_Show_Information.objects.filter(active_info_id=u_id).update(is_deleted=1)
            if data_ld!=0 and data_ld2!=0 and data_ld3!=0:
                msg='活動資料、表演資料刪除成功'
                status_msg = "OK"
                status_code = status.HTTP_200_OK
            else:
                msg='匹配不到資料'
                status_msg = "ERROR"
                status_code = status.HTTP_404_NOT_FOUND
        except Exception as e:
            msg = '刪除失敗,請重新操作'
            status_msg = "ERROR"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            print(e)
        ret_json = dict(data={'msg':msg,'status_msg':status_msg,'status_code':status_code})
        print(ret_json)
        return Response(ret_json)