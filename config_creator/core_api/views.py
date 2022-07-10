from core.models import Field
from django import views
from rest_framework import renderers, response, request, status, views
from rest_framework.permissions import IsAuthenticated, AllowAny


class FieldView(views.APIView):

    renderer_classes = [renderers.JSONRenderer]
    permission_classes = [AllowAny]

    def delete(self, request: request, pk: int) -> response.Response:
        """
        > This function deletes a field from the database

        Args:
          request (request): request - this is the request object that is passed to the view.
          pk (int): The primary key of the field to be deleted.

        Returns:
          A response object with the data and status.
        """

        field = Field.objects.get(id=pk)
        if field:
            outp = {
                "message": f"Field '{field.name}' deleted.",
                "type": "success",
            }
            field.delete()
            return_status = status.HTTP_200_OK
        else:
            outp = {
                "message": f"Field with id '{pk}' does not exist.",
                "type": "error",
            }
            return_status = status.HTTP_404_NOT_FOUND

        return response.Response(data=outp, status=return_status)
