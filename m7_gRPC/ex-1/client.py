import grpc
import todo_pb2
import todo_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = todo_pb2_grpc.TodoServiceStub(channel)

    # Добавляем задачу
    response = stub.AddTask(todo_pb2.TaskRequest(
        title="Изучить gRPC",
        description="Практическое занятие"
    ))
    print(f"Добавлена задача: {response.title} (ID: {response.id})")

    # Получаем задачи (поток)
    print("\nВсе задачи:")
    for task in stub.GetTasks(todo_pb2.GetTasksRequest()):
        print(f"- {task.title} (Выполнено: {task.completed})")

if __name__ == '__main__':
    run()