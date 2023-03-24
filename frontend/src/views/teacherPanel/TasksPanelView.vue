<template>
  <div id="task-table-header">
    <span style="grid-column: 1; font-size: larger; margin-left: 5px"
      >Шаблоны задач</span
    >
    <div style="grid-column: 2">
      <button class="button-icon" onclick="disp_dialog($('#add-task'))">
        <BookPlus /> &nbsp; Добавить &nbsp;
      </button>
    </div>
  </div>

  <!-- Displays notifications about invalid ltc syntax, useless with vue -->
  <!-- {% if notification %}
    <div> {{ notification }} </div>
{% endif %} -->

  <div id="task-table">
    <!-- Here goes iteration for tasks in all tasks, needs Django API -->
    <!-- {% for temp in alltasktypes %}
    <div style="border-left: none;" class="task-table-element">
        <a href="{{ temp.id }}/">{{ temp.name }}</a>
    </div>
    <div style="grid-column: 2; padding: 0; border-left: none;" class="task-table-element">
        <form method="post">
            {% csrf_token %}
            <div name="{{ temp.name }}">
                <button title="Удалить шаблон" name="delete:{{temp.id}}" type="button" class="button-icon" onclick="delete_signal_to_send=this.name; $('#confirm-task-deleting-massage')[0].innerHTML = 'Вы уверены что хотите удалить шаблон ' + this.closest('div').attributes.name.value + '?'; $('#confirm-task-deleting-button')[0].name = this.name; disp_dialog($('#delete-task-confirm'))"><div style="width: 1.5em; padding: 0;">{% include "icons/delete-icon.html" %}</div></button>
            </div>
        </form>
    </div>
{% endfor %} -->
  </div>
  <!-- Code above includes modals, it needs to be totaly reworked -->
  <!-- <button id="blackout" style="display: none;" onclick="disp_dialog([$('#delete-task-confirm'), $('#add-task')])"></button>
{% include "./add_task.html" %}
<form method="post">
    {% csrf_token %}
    <table id="delete-task-confirm" class="dialog-table" style="display: none;">
        <tr><td colspan="2" id="confirm-task-deleting-massage">Вы уверены что хотите удалить пользователя?</td></tr>
        <tr>
            <td style="display: grid; justify-items: end;"><button id="confirm-task-deleting-button" type="submit" class="wrong">Подтвердить</button></td>
            <td><button type="button" onclick="disp_dialog($('#delete-task-confirm'))">Отменить</button></td>
        </tr>
    </table>
</form> -->
</template>

<script>
import BookPlus from "@/assets/icons/book-plus.vue";

export default {
  components: {
    BookPlus,
  },
};
</script>
