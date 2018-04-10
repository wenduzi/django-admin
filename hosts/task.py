class Task(object):
    def __init__(self, request):
        self.request = request
        self.task_type = self.request.POST.get('task_type')

    def handle(self):
        if self.task_type:
            if hasattr(self, self.task_type):
                func = getattr(self, self.task_type)
                return func()
            else:
                return TypeError

    def multi_cmd(self):
        print(self.request.POST.get('task_type'))
        print(self.request.POST.get('cmd_text'))
        print(self.request.POST.getlist('selected_host[]'))
        print('doing something')
