import logging
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from .models import LogModel
from .test_function import load_test
logger = logging.getLogger(__name__)

def save_test_to_model(log):

    browser = log.get('browser', 'Default')
    start = log.get('start')
    elapsed = log.get('elapsed', 0)
    total = log.get('total', 0)
    success = log.get('pass', 0)
    failed = log.get('failure', 0)
    detail = log.get('detail', 'No more data')
    if log:
        LogModel.objects.create(
            browser_type=browser,
            started_time=start, elapsed_time=elapsed,
            total_run_num=total, pass_case_num=success, failed_case_num=failed,
            detail_log=detail
        ).save()

def activate_test(request):

    logger.debug('activate_test-request is %s' % request.POST)

    if '_run' in request.POST:
        test_type = request.POST['browsertype']
        result = load_test(test_type)

        logger.debug("test report is %s" % result)

        if len(result) > 0:
            result['browser'] = test_type

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


class DetailLog(DetailView):
    template_name = 'logdetail.html'
    model = LogModel

    def get_context_data(self, **kwargs):
        context = super(DetailLog, self).get_context_data(**kwargs)
        return context







