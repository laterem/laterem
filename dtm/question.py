from prototype.de_web.oop_taskengine.forms import AddAnswerForm
from prototype.de_web.oop_taskengine.views import base_task_handle
from prototype.de_web.oop_taskengine.tasks import Task
from dtc.dtc_compiler import DTCCompiler

def prepare_dtc(file):
    with open(file+'.dtc', mode='r') as f:
        txt = f.read()

    dtcc = DTCCompiler()

    dtc = dtcc.compile(txt)
    dtc.execute()
    return dtc.field_table

class do_task(Task):
    def configure(self, dtc) -> None:
        self.correct_answers = dtc['answer']
        self.description = dtc['text']
    
    def render(self) -> str:
        return self.description

    def generate(self) -> None:
        return NotImplemented
    
    def test(self, answer: str) -> int:
        return answer.strip() in self.correct_answers

def task_render(request):
    dtc = prepare_dtc('question')
    task = do_task.configure(dtc=dtc)
    standart_button = AddAnswerForm()
    return base_task_handle(request, task, template='question', render_args={'text': dtc['text'], 'form': standart_button})