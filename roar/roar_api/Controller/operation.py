
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.shortcuts import render
from ..Models.active_models import Active_Category_Unit,Active_Information,Active_Show_Information
from django.template.response import TemplateResponse

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
        except Exception as e:
            print(e)
        template_dict = dict(
            uid = u_id,
            data_ld = data_dict
            
        )
        # 渲染模板并返回响应
        return TemplateResponse(request, 'operator.html', template_dict)
    def patch(self,request,*args,**kwargs):
        data_form = request.data
        
        try:
            pass
        except Exception as e:
            pass

        ret_json = dict(data={})
        return Response(ret_json)

    def deleted(self,request,*args,**kwargs):
        pass
# class Operation(TemplateView):
#     template_name = 'operator.html'
#     def get(self,request,*args,**kwargs):
#         uid = self.kwargs.get('UID')
#         print(uid)
#         template_dict = dict()
#         return render(request,self.template_name,template_dict)

#     def post(self,request,*args,**kwargs):
#         template_dict = dict()
#         return render(request,self.template_name,template_dict)