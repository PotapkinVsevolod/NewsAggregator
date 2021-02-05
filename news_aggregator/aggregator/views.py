from django.http import HttpResponse, JsonResponse
from django.views import View

from aggregator.models import News


ORDER_CHOICE = ('id', '-id', 'title', '-title', 'link', '-link', 'created_at', '-created_at')


class PostsView(View):
    def get(self, request):
        order = self.request.GET.get('order', 'id')
        if order not in ORDER_CHOICE:
            return HttpResponse(f'{order} not in ordering methods.\n')

        try:
            offset = int(self.request.GET.get('offset', 0))
        except Exception as err:
            return HttpResponse(f'{err}\n')

        if offset < 0:
            return HttpResponse('Offset can only take a positive value.\n')
        elif offset not in range(News.objects.count()):
            return HttpResponse(f'Value out of range. Maximum possible '
                                f'value is {News.objects.count() - 5}.\n')

        try:
            limit = int(self.request.GET.get('limit', 5))
        except Exception as err:
            return HttpResponse(f'{err}\n')

        if limit < 1:
            return HttpResponse('Limit can only take a positive value more than one.')
        elif limit not in range(News.objects.count()):
            return HttpResponse(f'Value out of range. Maximum possible '
                                f'value is {News.objects.count() - offset}.\n')

        news = News.objects.order_by(order)[offset:][:limit].values()

        return JsonResponse(list(news), safe=False)
