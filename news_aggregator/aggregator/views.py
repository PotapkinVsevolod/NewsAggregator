from django.http import HttpResponse, JsonResponse
from django.views import View

from aggregator.models import News


ORDER_CHOICE = ('id', '-id', 'title', '-title', 'link', '-link', 'created_at', '-created_at')


class PostsView(View):
    def get(self, request):

        order = self.request.GET.get('order', 'id')
        if order not in ORDER_CHOICE:
            return HttpResponse(f'Ошибка, order может принимать следующие значения - {ORDER_CHOICE}')

        offset = self.request.GET.get('offset', 0)
        if not offset.isdigit() or int(offset) not in range(News.objects.count()):
            return HttpResponse(f'Ошибка, offset должен принимать положительные целочисленные '
                          f'значения, не более чем {News.objects.count() - 5}')
        else:
            offset = int(offset)

        limit = self.request.GET.get('limit', 5)
        if not limit.isdigit() or int(limit) not in range(1, News.objects.count() - offset):
            return HttpResponse(f'Ошибка, limit может принимать положительные целочисленные '
                                f'значения, не более чем {News.objects.count() - offset}')
        else:
            limit = int(limit)

        items_query = News.objects.order_by(order)[offset:][:limit].values('id', 'title', 'link', 'created_at')
        return JsonResponse(list(items_query), safe=False)
