from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    get_object_or_404,
    RetrieveDestroyAPIView
)

from apps.projects.models import Project, ProjectFile
from apps.projects.serializers.project_file_serializers import (
    CreateProjectFileSerializer,
    AllProjectFileSerializer,
    ProjectFileDetailSerializer
)
from apps.projects.utils.upload_file_helper import delete_file


class ProjectFileListGenericView(ListCreateAPIView):
    def get_queryset(self):
        project_name = self.request.query_params.get("project_name")
        if project_name:
            return ProjectFile.objects.filter(
                project__name=project_name
            )
        return ProjectFile.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return AllProjectFileSerializer
        return CreateProjectFileSerializer

    def get(self, request: Request, *args, **kwargs)-> Response:
        project_files = self.get_queryset()
        if not project_files.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )
        serializer = self.get_serializer(project_files, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request, *args, **kwargs) -> Response:
        file = request.FILES.get("file", None)
        project_id = request.data.get("project_id", None)
        request.data["file_name"] = file.name if file else None

        project = get_object_or_404(Project, pk=project_id)

        context = {
            "file": file,
            "project": project
        }

        serializer = self.get_serializer(data=request.data, context=context)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class ProjectFileDetailGenericView(RetrieveDestroyAPIView):

    serializer_class = ProjectFileDetailSerializer

    def get_object(self):
        return get_object_or_404(ProjectFile, pk=self.kwargs["file_id"])


    def get(self, request: Request, *args, **kwargs) -> Response:
        file = self.get_object()
        serializer = self.serializer_class(file)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request: Request, *args, **kwargs) -> Response:
        file = self.get_object()

        try:
            delete_file(file.file_path)
            file.delete()
            return Response(
                data={
                    'message': 'File was successfully deleted.'
                },
                status=status.HTTP_200_OK
            )
        except FileNotFoundError as err:

            return Response(
                data={
                    "message": str(err)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

