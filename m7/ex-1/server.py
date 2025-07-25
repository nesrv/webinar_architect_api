from concurrent import futures
import grpc
import todo_pb2
import todo_pb2_grpc

class TodoService(todo_pb2_grpc.TodoServiceServicer):
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def AddTask(self, request, context):
        task = todo_pb2.TaskResponse(
            id=self.next_id,
            title=request.title,
            description=request.description,
            completed=False
        )
        self.tasks.append(task)
        self.next_id += 1
        return task

    def GetTasks(self, request, context):
        for task in self.tasks:
            yield task  # Отправка задач через поток

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Сервер запущен на порту 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()