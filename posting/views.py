import json

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Count

from user.models    import User
from user.utils     import login_decorator, non_user_accept_decorator
from posting.models import (
        Posting,
        PostingSize,
        PostingHousing,
        PostingStyle,
        PostingSpace,
        PostingLike,
        PostingScrap
)

class PostingView(View):
    @non_user_accept_decorator
    def get(self, request):
        user          = request.user
        postings      = Posting.objects.prefetch_related('comment').select_related('user').all()
        order_request = request.GET.get('order', 'recent')
        postings      = postings.annotate(
                            like_num=Count('postinglike'),
                            comment_num=Count('comment'),
                            scrap_num=Count('postingscrap')
                            )
        
        order_prefixes = {
                'best'      : '-like_num',
                'popular'   : '-comment_num',
                'scrap'     : '-scrap_num',
                'recent'    : '-created_at',
                'old'       : 'created_at'
                }

        filter_prefixes = {
                'housing'    : 'housing_id__in',
                'space'      : 'space_id__in',
                'size'       : 'size_id__in',
                'style'      : 'style_id__in'
                }
        filter_set = {
                filter_prefixes.get(key) : value for (key, value) in dict(request.GET).items() 
                if filter_prefixes.get(key)
                }

        postings = postings.filter(**filter_set).order_by(order_prefixes[order_request])
        
        posting_list = [{
                'id'                        : posting.id,
                'card_user_image'           : posting.user.image_url,
                'card_user_name'            : posting.user.name,
                'card_user_introduction'    : posting.user.description,
                'card_image'                : posting.image_url,
                'card_content'              : posting.content,
                'like_status'               : posting.postinglike_set.filter(user=user).exists(),
                'scrap_status'              : posting.postingscrap_set.filter(user=user).exists(),
                'comment_num'               : posting.comment.filter(posting_id=posting.id).count(),
                'comment_user_image'        : posting.comment.all()[0].user.image_url if posting.comment.exists() else None,
                'comment_user_name'         : posting.comment.all()[0].user.name if posting.comment.exists() else None,
                'comment_content'           : posting.comment.all()[0].content if posting.comment.exists() else None,
                'like_num'                  : posting.postinglike_set.filter(posting_id=posting.id).count(),
                'scrap_num'                 : posting.postingscrap_set.filter(posting_id=posting.id).count(),
                'created_at'                : posting.created_at
                } for posting in postings
        ]
        return JsonResponse({'message' : posting_list}, status=200)

    @login_decorator
    def post(self, request):
        try:
            user       = request.user
            data       = json.loads(request.body)
            size_id    = data.get('size', None)
            housing_id = data.get('housing', None)
            style_id   = data.get('style', None)
            space_id   = data.get('space', None)
            image_url  = data.get('card_image', None)
            content    = data.get('card_content', None)

            if not (size_id and housing_id and style_id and space_id and image_url and content):
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            Posting.objects.create(
                    user_id    = user.id, 
                    image_url  = image_url, 
                    content    = content, 
                    size_id    = size_id, 
                    housing_id = housing_id, 
                    style_id   = style_id, 
                    space_id   = space_id
                    )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

class CategoryView(View):
    def get(self, request):
        sortings    = [
                {'id' : 1, 'name' : '역대인기순', 'Ename' : 'best'},
                {'id' : 2, 'name' : '댓글많은순', 'Ename' : 'popular'},
                {'id' : 3, 'name' : '스크랩많은순', 'Ename' : 'scrap'},
                {'id' : 4, 'name' : '최신순', 'Ename' : 'recent'},
                {'id' : 5, 'name' : '오래된순', 'Ename' : 'old'}
        ]
        
        category_condition = {
                'categories' : [
                    {
                        'id' : 1,
                        'categoryName'  : '정렬',
                        'categoryEName' : 'order',
                        'category'      : [name for name in list(sortings)]
                        },
                    {
                        'id' : 2,
                        'categoryName'  : '주거형태',
                        'categoryEName' : 'housing',
                        'category'      : [name for name in list(PostingHousing.objects.values().order_by('id'))]
                    },
                    {
                        'id' : 3,
                        'categoryName'  : '공간',
                        'categoryEName' : 'space',
                        'category'      : [name for name in list(PostingSpace.objects.values().order_by('id'))]
                    },
                    {
                        'id' : 4,
                        'categoryName'  : '평수',
                        'categoryEName' : 'size',
                        'category'      : [name for name in list(PostingSize.objects.values().order_by('id'))]
                    },
                    {
                        'id' : 5,
                        'categoryName'  : '스타일',
                        'categoryEName' : 'style',
                        'category'      : [name for name in list(PostingStyle.objects.values().order_by('id'))]
                    }]
                }
        return JsonResponse({'categories' : category_condition}, status=200)

class PostingLikeView(View):
    @login_decorator
    def post(self, request):
        try:
            user       = request.user
            data       = json.loads(request.body)
            posting_id = data.get('posting_id', None)

            if not posting_id:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)
            
            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({'message':'POSTING_DOES_NOT_EXIST'}, status=401)

            if PostingLike.objects.filter(user=user, posting_id=posting_id).exists():
                PostingLike.objects.filter(user=user, posting_id=posting_id).delete()
                return JsonResponse({'message':'SUCCESS'}, status=204)

            PostingLike.objects.create(user_id=user.id, posting_id=posting_id)
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except json.decoder.JSONDecodeError:
                    return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

class PostingScrapView(View):
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            posting_id = data.get('posting_id', None)

            if not posting_id:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)
            
            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({'message':'POSTING_DOES_NOT_EXIST'}, status=401)

            if PostingScrap.objects.filter(user=user, posting_id=posting_id).exists():
                PostingScrap.objects.filter(user=user, posting_id=posting_id).delete()
                return JsonResponse({'message':'SUCCESS'}, status=204)

            PostingScrap.objects.create(user_id=user.id, posting_id=posting_id)
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except json.decoder.JSONDecodeError:
                    return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

