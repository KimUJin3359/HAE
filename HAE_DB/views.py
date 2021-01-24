from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery, Count
from django.db.models.functions import Coalesce
from django.db.models import Value
from PIL import Image
import datetime
import pandas
import shutil
import sys
sys.path.append("""C:\\Users\michi\HAE\yolov5\yolov5""")
sys.path.append('C:/Users/michi/HAE/yolov5/yolov5')

from yolov5.yolov5 import adaptor, detect




########################GET##############################

# user_feed 목록 시간 기준 오름차순 반환
@api_view(['GET'])
def user_feed_list(request):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    feeds = queryset = feed.objects.all().values('ID', 'des', 'start_time', 'end_time', 'created_at', 'image',
                                                 'user_ID', 'user_ID__name', 'user_ID__image') \
        .filter(user_ID=user_ID).order_by('-created_at')

    return Response(feeds)


# crew_feed 목록 시간 기준 오름차순 반환
@api_view(['GET'])
def crew_feed_list(request):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    f_crew_id = user.objects.values('crew_ID').filter(ID=user_ID)
    f_user_id = user.objects.values('ID').filter(crew_ID__in=f_crew_id)
    feeds = feed.objects.values('ID', 'des', 'start_time', 'end_time', 'created_at',
                                'image', 'user_ID', 'user_ID__name','user_ID__image')\
        .order_by('-created_at').filter(user_ID__in=f_user_id)

    if user.objects.get(ID=user_ID).crew_ID_id == 1:
        return Response(None)
    else:
        return Response(feeds)


# feed 댓글 반환
@api_view(['GET'])
def feed_comment_list(request, feed_ID):
    feed_comments = feed_comment.objects.values('ID', 'comment', 'created_at', 'feed_ID', 'user_ID', 'user_ID__name',
                                                'user_ID__image').order_by('-created_at').filter(feed_ID=feed_ID)

    return Response(feed_comments)


# gathering 댓글 반환
@api_view(['GET'])
def gathering_comment_list(request, gathering_ID):
    gathering_comments = gathering_comment.objects.values('ID', 'comment', 'created_at', 'gathering_ID',
                                                          'user_ID', 'user_ID__name', 'user_ID__image') \
        .order_by('-created_at').filter(gathering_ID=gathering_ID)

    return Response(gathering_comments)


# crew 목록 ID 기준 오름차순 반환
@api_view(['GET'])
def crew_list(request, name=None):
    if (name == None):
        qs = crew.objects.annotate(
            count=Coalesce(Subquery(user.objects.filter(crew_ID=OuterRef('pk')).values('crew_ID').annotate(count=Count('pk')).values('count')), Value(0))
        ).annotate(
            gathering_count=Coalesce(Subquery(gathering.objects.filter(crew_ID=OuterRef('pk')).values('crew_ID').annotate(gathering_count=Count('pk')).values('gathering_count')), Value(0))
        )

        data = list(qs.values())

        return Response(data)

    else:
        qs = crew.objects.filter(name__contains=name).annotate(
            count=Coalesce(Subquery(user.objects.filter(crew_ID=OuterRef('pk')).values('crew_ID').annotate(count=Count('pk')).values('count')), Value(0))
        ).annotate(
            gathering_count=Coalesce(Subquery(gathering.objects.filter(crew_ID=OuterRef('pk')).values('crew_ID').annotate(gathering_count=Count('pk')).values('gathering_count')), Value(0))
        )
        
        data = list(qs.values())

        return Response(data)


# crew 정보 반환
@api_view(['GET'])
def crew_info(request):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)
    crew_ID = user.objects.get(ID=user_ID).crew_ID_id

    qs = crew.objects.filter(ID=crew_ID).annotate(
        mem_count=Coalesce(Subquery(user.objects.filter(crew_ID=OuterRef('pk')).values('crew_ID').annotate(mem_count=Count('pk')).values('mem_count')), Value(0))
    ).annotate(
        gathering_count=Coalesce(Subquery(gathering.objects.filter(crew_ID=OuterRef('pk')).values('crew_ID').annotate(gathering_count=Count('pk')).values('gathering_count')), Value(0))
    ).values('ID', 'name', 'des', 'image', 'mem_count', 'gathering_count')
    data = list(qs.values())

    if(crew_ID==1):
        return Response(None)
    else:
        return Response(data)

@api_view(['GET'])
def check_crew_header(request):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    try:
        crew_header.objects.get(user_ID=user_ID)

        return Response({'result' : 'success'})

    except crew_header.DoesNotExist:

        return Response({'result' : 'fail'})

# gathering start time 기준 오름차순 반환
@api_view(['GET'])
def gathering_list(request):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    crew_id = user.objects.get(ID=user_ID)
    gatherings = gathering.objects.order_by('-created_at').filter(crew_ID=crew_id.crew_ID_id, date__gte=datetime.datetime.now()).annotate(
        count=Coalesce(Subquery(gathering_participant.objects.filter(gathering_ID=OuterRef('pk')).values('gathering_ID').annotate(count=Count('pk')).values('count')),Value(0))
    ).annotate(
        participate=Coalesce(Subquery(gathering_participant.objects.filter(gathering_ID=OuterRef('pk'), user_ID=user_ID).values('gathering_ID').annotate(participate=Count('pk')).values('participate')), Value(0))
    )
    data = list(gatherings.values())

    if crew_id.crew_ID_id == 1:
        return Response(None)
    else:
        return Response(data)


# gathering 참여자 목록 반환
@api_view(['GET'])
def gathering_participant_list(request, gathering_ID):
    participant_lists = gathering_participant.objects.values('user_ID').filter(gathering_ID=gathering_ID)
    user_lists = user.objects.order_by('name').filter(ID__in=participant_lists)
    serializer = UserSerializer(user_lists, many=True)

    return Response(serializer.data)


# 위도, 경도 파악해서 거리안에 속하는 기구들 반환
@api_view(['GET'])
def equipment_list(request, X_loc, Y_loc, distance, category=-1):
    allow = float(distance) * 0.001  # 2,5,10
    # 1km에 0.01 100m에 0.001

    if (category == -1):
        equipments = equipment.objects.filter(location_X__gte=float(X_loc) - allow,
                                              location_X__lte=float(X_loc) + allow,
                                              location_Y__gte=float(Y_loc) - allow,
                                              location_Y__lte=float(Y_loc) + allow)
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data)

    else:
        equipments = equipment.objects.filter(category=category,
                                              location_X__gte=float(X_loc) - allow,
                                              location_X__lte=float(X_loc) + allow,
                                              location_Y__gte=float(Y_loc) - allow,
                                              location_Y__lte=float(Y_loc) + allow)
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data)


# 유저 정보 반환
@api_view(['GET'])
def user_profile(request):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    profile = user.objects.get(ID=user_ID)
    serializer = UserSerializer(profile)

    return Response(serializer.data)


# 비밀번호 일치 확인
@api_view(['GET'])
def user_login(request, ID, password):
    try:
        login_User = account.objects.get(user_ID=ID)
        if (password == login_User.password):
            payload = {
                'user_ID': login_User.ID_id
            }
            jwt_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm)

            return Response({'token' : jwt_token.decode('utf-8')})

        else:
            return Response({'result' : 'password error'})

    except account.DoesNotExist:
        return Response({'result' : 'not exist id'})


####################################PUT########################
# 유저 정보 변경
@api_view(['PUT'])
def user_put(request):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    name = request.POST['name']
    if (request.FILES.get('image', False)):
        image = request.FILES['image']
    else:
        image = None

    result = user.update_profile(ID=user_ID, name=name, image=image)

    if(result):
        return Response({'result': 'success'})
    else:
        return Response({'result': 'fail'})

# feed 업데이트
@api_view(['PUT'])
def user_feed_put(request, feed_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    des = request.POST['des']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']
    if (request.FILES.get('image', False)):
        image = request.FILES['image']
    else:
        image = None

    try:
        if (feed.objects.get(ID=feed_ID).user_ID_id == user_ID):
            feed.update(ID=feed_ID, des=des, start_time=start_time,
                        end_time=end_time, image=image)

            return Response({'result' : 'success'})

        else:
            return Response({'result' : 'not your feed'})

    except feed.DoesNotExist:
        return Response({'result' : 'not exist feed'})


# feed 댓글 업데이트
@api_view(['PUT'])
def feed_comment_put(request, feed_comment_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    comment = request.POST['comment']

    try:
        if (feed_comment.objects.get(ID=feed_comment_ID).user_ID_id == user_ID):
            feed_comment.update(feed_comment_ID, comment)

            return Response({'result' : 'success'})

        else:
            return Response({'result' : 'not your feed comment'})

    except feed.DoesNotExist:
        return Response({'result' : 'not exist feed comment'})


# crew 가입 시
@api_view(['PUT'])
def crew_update(request, crew_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    result = user.update_crew(user_ID=user_ID,
                              crew_ID=crew.objects.get(ID=crew_ID))

    if (result):
        return Response({'result' : 'success'})
    else:
        return Response({'result' : 'fail'})

# 모임 참가
@api_view(['PUT'])
def gathering_participate(request, gathering_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    result = gathering_participant.create(user_ID=user.objects.get(ID=user_ID),
                                          gathering_ID=gathering.objects.get(ID=gathering_ID))

    if (result):
        return Response({'result': 'success'})
    else:
        return Response({'result': 'fail'})


# 모임 댓글 수정
@api_view(['PUT'])
def gathering_comment_update(request, gathering_comment_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    comment = request.POST['comment']

    try:
        if (gathering_comment.objects.get(ID=gathering_comment_ID).user_ID_id == user_ID):
            gathering_comment.update(ID=gathering_comment_ID, comment=comment)

            return Response({'result': 'success'})

        else:
            return Response({'result': 'not your gathering comment'})

    except gathering_comment.DoesNotExist:
        return Response({'result': 'not exist gathering comment'})


###############################DELETE##########################

# feed 삭제
@api_view(['DELETE'])
def user_feed_delete(request, feed_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    try:
        if (feed.objects.get(ID=feed_ID).user_ID_id == user_ID):
            feed.remove(feed_ID)

            return Response({'result': 'success'})

        else:
            return Response({'result': 'not your feed'})

    except feed.DoesNotExist:
        return Response({'result': 'not exist feed'})

# crew 탈퇴 시
@api_view(['DELETE'])
def crew_leave(request):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    if(user.objects.get(ID=user_ID).crew_ID_id == 1):

        return Response({'result': 'you are not in crew'})

    try:
        crew_header.objects.get(user_ID=user_ID)

        return Response({'result': 'crew header cant leave'})

    except crew_header.DoesNotExist:
        user.update_crew(user_ID=user_ID, crew_ID=crew.objects.get(ID=1))

        return Response({'result': 'success'})


# feed 댓글 삭제
@api_view(['DELETE'])
def feed_comment_delete(request, feed_comment_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    try:
        if (feed_comment.objects.get(ID=feed_comment_ID).user_ID_id == user_ID):
            feed_comment.remove(feed_comment_ID)

            return Response({'result': 'success'})

        else:
            return Response({'result': 'not your feed comment'})

    except feed.DoesNotExist:
        return Response({'result': 'not exist feed comment'})


# 기구 삭제
@api_view(['DELETE'])
def equipment_delete(request, equipment_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    try:
        e = equipment.objects.get(ID=equipment_ID)

        if (e.user_ID_id == user_ID):
            equipment.remove(equipment_ID)

            return Response({'result': 'success'})

        else:
            return Response({'result': 'not your equipment'})

    except equipment.DoesNotExist:
        return Response({'result': 'not exist equipment'})


# crew 삭제 시
@api_view(['DELETE'])
def crew_delete(request):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    try:
        deleteCH = crew_header.objects.get(user_ID=user_ID)
        crew_ID = deleteCH.crew_ID_id
        deleteCH.delete()
        user.objects.get(ID=user_ID).update_crew_reset(crew_ID=crew.objects.get(ID=crew_ID))
        crew.objects.get(ID=crew_ID).delete()

        return Response({'result': 'success'})

    except crew_header.DoesNotExist:
        return Response({'result': 'not your crew'})


# 모임 삭제
@api_view(['DELETE'])
def gathering_delete(request, gathering_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    result = gathering.remove(user_ID=user.objects.get(ID=user_ID),
                              gathering_ID=gathering_ID)

    if(result == 1):
        return Response({'result': 'success'})

    elif(result == 0):
        return Response({'result' : 'not your gathering'})

    elif(result == -1):
        return Response({'result' : 'not exist gathering'})



# 모임 참가 취소
@api_view(['DELETE'])
def gathering_not_participate(request, gathering_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    result = gathering_participant.remove(user_ID=user.objects.get(ID=user_ID),
                                          gathering_ID=gathering.objects.get(ID=gathering_ID))

    return Response({'result' : result})


# 모임 댓글 삭제
@api_view(['DELETE'])
def gathering_comment_delete(request, gathering_comment_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    try:
        if (gathering_comment.objects.get(ID=gathering_comment_ID).user_ID_id == user_ID):
            gathering_comment.remove(ID=gathering_comment_ID)

            return Response({'result' : 'success'})

        else:
            return Response({'result' : 'not your gathering comment'})

    except gathering_comment.DoesNotExist:
        return Response({'result' : 'not exist gathering comment'})


######################POST########################

# 이미지 판단
@api_view(['POST'])
def equipment_judge(request):
    if (request.FILES.get('image', False)):
        image = request.FILES['image']

        judge.create(image)
        sys.argv = ['']
        result = adaptor.get_equipment_category()
        shutil.rmtree('C:/Users/michi/HAE/yolov5/yolov5/inference/media/test')

        return Response({'result' : result})

    else:

        return Response({'result' : 'fail'})




# 유저 ID, password 및 정보 삽입
@api_view(['POST'])
def user_post(request):  # crew 새로 만든 것 삭제하지 말기, 다시 바꿔주기!

    ID = request.POST['ID']
    password = request.POST['password']
    name = request.POST['name']
    crew_ID = 1
    if (request.FILES.get('image', False)):
        image = request.FILES['image']
    else:
        image = None

    try:
        account.objects.get(user_ID=ID)

        return Response({'result' : 'already exist id'})

    except account.DoesNotExist:
        new_User = user.create(name=name, crew_ID=crew.objects.get(ID=crew_ID), image=image)
        account.create(ID=user.objects.get(ID=new_User.ID), user_ID=ID, password=password)

        return Response({'result' : 'success'})


# crew 생성 시
@api_view(['POST'])
def crew_post(request):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    name = request.POST['name']
    des = request.POST['des']
    if (request.FILES.get('image', False)):
        image = request.FILES['image']
    else:
        image = None

    new_Crew = crew.create(name, des, image)
    crew_header.create(crew_ID=crew.objects.get(ID=new_Crew.ID), user_ID=user.objects.get(ID=user_ID))
    result = user.update_crew(user_ID=user_ID, crew_ID=crew.objects.get(ID=new_Crew.ID))

    if (result):
        return Response({'result' : 'success'})
    else:
        return Response({'result' : 'fail'})


# feed 댓글 삽입
@api_view(['POST'])
def feed_comment_post(request, feed_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    comment = request.POST['comment']
    created_at = datetime.datetime.now()

    result = feed_comment.create(comment=comment, created_at=created_at,
                                 feed_ID=feed.objects.get(ID=feed_ID),
                                 user_ID=user.objects.get(ID=user_ID))

    if (result):
        return Response({'result' : 'success'})
    else:
        return Response({'result' : 'fail'})


# feed 데이터 삽입
@api_view(['POST'])
def user_feed_post(request):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    des = request.POST['des']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']
    created_at = datetime.datetime.now()
    if (request.FILES.get('image', False)):
        image = request.FILES['image']
    else:
        image = None

    result = feed.create(des=des, start_time=start_time, end_time=end_time,
                         created_at=created_at, user_ID=user.objects.get(ID=user_ID), image=image)

    if (result):
        return Response({'result' : 'success'})
    else:
        return Response({'result' : 'fail'})


# 기구 삽입
@api_view(['POST'])
def equipment_post(request, X_loc, Y_loc, category):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    location_X = float(X_loc)
    location_Y = float(Y_loc)
    if (request.FILES.get('image', False)):
        image = request.FILES['image']
    else:
        image = None

    result = equipment.create(category=category, location_X=location_X, location_Y=location_Y,
                              user_ID=user.objects.get(ID=user_ID), image=image)

    if (result):
        return Response({'result' : 'success'})
    else:
        return Response({'result' : 'fail'})


# 모임 댓글 생성
@api_view(['POST'])
def gathering_comment_create(request, gathering_ID):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    comment = request.POST['comment']
    created_at = datetime.datetime.now()

    result = gathering_comment.create(comment=comment, created_at=created_at,
                                      gathering_ID=gathering.objects.get(ID=gathering_ID),
                                      user_ID=user.objects.get(ID=user_ID))

    if (result):
        return Response({'result' : 'success'})
    else:
        return Response({'result' : 'fail'})


# 모임 생성
@api_view(['POST'])
def gathering_post(request):
    token = request.headers.get('token')
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithm)
    user_ID_s = payload.get('user_ID')
    user_ID = int(user_ID_s)

    name = request.POST['name']
    date = request.POST['date']
    created_at = datetime.datetime.now()
    crew_ID = user.objects.get(ID=user_ID).crew_ID_id

    if (user.objects.get(ID=user_ID).crew_ID_id == 1):
        return Response({'result' : 'not in guild'})

    elif (crew_ID == user.objects.get(ID=user_ID).crew_ID_id):
        gathering.create(name=name, created_at=created_at, date=date,
                         crew_ID=crew.objects.get(ID=crew_ID),
                         user_ID=user.objects.get(ID=user_ID))

        return Response({'result' : 'success'})
    else:
        return Response({'result' : 'not your crew'})
