from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, TemplateView
from .test_function import load_test
from .models import LogModel
import logging
logger = logging.getLogger(__name__)



# Create your views here.
'''
 browser_type = models.ForeignKey(BrowserModel)
    started_time = models.CharField(max_length=30)
    elapsed_time = models.CharField(max_length=10)
    total_run_num = models.PositiveIntegerField()
    pass_case_num = models.PositiveIntegerField()
    failed_case_num = models.PositiveIntegerField()
    detail_log = models.TextField(blank=True)

'''

def save_test_to_model(log):
   # browser = BrowserModel(log['browser'])
   # print (BrowserModel.objects.all())

    if log:
        LogModel.objects.create(
            browser_type=log['browser'],
            started_time=log['start'], elapsed_time=log['elapsed'],
            total_run_num=log['total'], pass_case_num=log['pass'], failed_case_num=log['failure'],
            detail_log =log['log']
        ).save()

def activate_test(request):
    print('activate_test')


    logger.error(request.POST)

    if '_run' in request.POST:
        result = ''
        test_type = request.POST['browsertype']
        logger.error(test_type)
        result = load_test(test_type)
        result['browser'] = test_type
        #logger.error(result)

        save_test_to_model(result)


    queryset = LogModel.objects.all()

    context_object_name = 'loglist'
    template_name = 'homepage.html'
    if request.method == 'POST':
        return redirect('homepage')
    else:
        return render(request, template_name,
                      {context_object_name: queryset,}
                      )










