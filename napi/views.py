from celery import chain
from celery.result import AsyncResult
from rest_framework import viewsets, status, renderers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.utils.breadcrumbs import get_breadcrumbs
from napi.models import ProcessQueueAction
from napi.permissions import IsOwnerOrReadOnly,IsOwner
from napi.serializers import ProcessQueueActionSerializer, TaskSerializer
from napi.tasks import VerificationTask, ReadyForNumberTask, PreparationTask, PrintingTask, PersonalizationTask


class ProcessQueueActionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = ProcessQueueActionSerializer
    queryset = ProcessQueueAction.objects.all()
    lookup_field = 'tracking_id'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, url_path='taskstatus/(?P<task_id>[^/.]+)')
    def task_status(self, request, **kwargs):
        self.__setattr__('description', 'Returns individual celery task status')
        self.__setattr__('name', 'Task status')

        task_id = kwargs.get('task_id', None)
        task_response = self.get_task_result(task_id)

        return Response(task_response)

    @action(detail=True, renderer_classes=[renderers.TemplateHTMLRenderer])
    def display_results(self, request, *args, **kwargs):
        breadcrumbs = get_breadcrumbs(request.path, request)
        response = {'breadcrumblist': breadcrumbs, 'name': 'Process Queue Action Graph Display',
                    'description': 'Showing visual/HTML representation of API instance',
                    'tracking_id': kwargs.get('tracking_id')}
        return Response(response, template_name='tasklist.html')

    @action(detail=True, name='Task results')
    def fetch_results(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        tasks = serializer.data['tasks']
        seq = 0
        for task in tasks:
            task['result'] = self.get_task_result(task['task_id'])

        return Response(serializer.data)

    @action(detail=True, description='Initialize celery tasks', permission_classes=(IsOwner,), name='Initialize tasks')
    def initialize_tasks(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        tasks = serializer.data['tasks']
        if len(tasks) > 1:
            response = {'response': 'Tasks already initialized', 'tasks': []}
            for task in tasks:
                response['tasks'].append(dict(task))
            return Response(response)
        else:
            pq_chain = chain(
                VerificationTask().s(serializer.data),
                ReadyForNumberTask().s(),
                PreparationTask().s({'tracking_id': instance.tracking_id}),
                PrintingTask().s(),
                PersonalizationTask().s()
            )
            result = pq_chain()

            task_ids = self.get_task_list(result, pq_chain.tasks)
            task_serializer = TaskSerializer(data=task_ids, many=True)
            if task_serializer.is_valid():
                task_serializer.save(tracking_id=instance.tracking_id)

            response = {'response': 'Task initialized successfully', 'tasks': list(task_serializer.data)}
            return Response(response)

    def get_task_list(self, result, chain_tasks):
        task_ids = []
        tasks = []
        while result.parent:
            task_ids.append(result.id)
            result = result.parent
        task_ids.append(result.id)

        task_ids.reverse()

        for i in task_ids:
            task = {'name': chain_tasks[task_ids.index(i)].name, 'task_id': i}
            tasks.append(task)

        return tasks

    def get_task_result(self, task_id=None):
        res = AsyncResult(task_id)
        task_response = {"status": res.status, "task_id": res.id}

        if res.info is not None:
            if isinstance(res.info, Exception):
                task_response['error'] = res.info.args[0]
                task_response['exception'] = type(res.info).__name__
            else:
                task_response['info'] = res.info

        return task_response
