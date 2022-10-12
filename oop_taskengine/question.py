from oop_taskengine.forms import AddAnswerForm
from oop_taskengine.views import base_task_handle
from oop_taskengine.tasks import Task
from dtc.dtc_compiler import DTCCompiler

def prepare_dtc(file):
    with open(file + '.dtc', mode='r') as f:
        txt = f.read()

    dtcc = DTCCompiler()

    dtc = dtcc.compile(txt)
    dtc.execute()
    return dtc

class do_task(Task):
    def configure(self, dtc) -> None:
        self.description = dtc.field_table['text']
        self.dtc = dtc
    
    def render(self) -> str:
        return self.description

    def generate(self) -> None:
        return NotImplemented
    
    def test(self, answer: str) -> int:
        fields = {'answer': answer.strip()}
        return self.dtc.check(fields)

def task_render(request):
    dtc = prepare_dtc('C:\My\SCHOOL\Programming\SPC\dew\dtm\\test_tasks\question')
    task = do_task()
    task.configure(dtc=dtc)
    dtc.field_table['standart_button'] = AddAnswerForm()
    return base_task_handle(request, task, template='question', render_args=dtc.field_table)