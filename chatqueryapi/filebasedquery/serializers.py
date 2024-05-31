from rest_framework.serializers import Serializer, FileField
from rest_framework import serializers
from rest_framework.fields import empty
from openai import OpenAI

from .models import ApiUser

class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']


class ChatQuerySerializer(Serializer):
    query = serializers.CharField(max_length=200)
    file_id = serializers.CharField(max_length = 200)

    class Meta:
        fields = ['query', 'file_id']

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        # print(self.__dict__)
        # print(self.initial_data)
        self.query = self.initial_data["query"]
        self.file_id = self.initial_data["file_id"]
        # print(self.query, self.file_id)
    
    def get_openai_fileid(self, user:ApiUser):
        # print(self.file_id)
        self.openai_file = user.user_files.filter(file_name = self.file_id).first().openai_fileid
        return self.openai_file

    def make_query(self):
        client = OpenAI()

        assistant = client.beta.assistants.create(
            name="Test Assistant",
            instructions="You are an expert interviewer. Use you knowledge base to answer questions about audited resume.",
            model="gpt-4o",
            tools=[{"type": "file_search"}],
        )

        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "How can I improve this resume?",
                    # Attach the new file to the message.
                    "attachments": [
                        {
                            "file_id": self.openai_file,
                            "tools": [
                                {"type": "file_search"}
                            ]
                        }
                    ],
                }
            ]
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=assistant.id
        )

        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        return {
            "message" : message_content,
            "citations" : "\n".join(citations),
        }

    
