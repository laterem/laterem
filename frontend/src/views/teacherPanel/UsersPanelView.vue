<template>
  <div id="user-table-header">
    <div style="grid-column: 1">
      <span style="font-size: larger; margin-left: 5px"
        >Все пользователи сайта</span
      >
    </div>
    <div style="grid-column: 2">
      <button class="button-icon" onclick="disp_dialog($('#add-user')[0])">
        <AddUserIcon /> &nbsp; Добавить &nbsp;
      </button>
    </div>
    <div style="grid-column: 3">
      <button class="button-icon" onclick="disp_dialog($('#import-users')[0])">
        <ImportFromFileIcon /> &nbsp; Импорт &nbsp;
      </button>
    </div>
  </div>

  <div id="user-table">
    <!-- Here goes iteration for users in all users, needs Django API -->
    <!-- {% for user in allusers %}
          <div style="grid-column: 1; border-left: none;" class="user-table-element">
              <input value="{{user.first_name}}" class="edit-user-{{user.id}}" disabled="true" name="user_name"/> <input value="{{user.last_name}}" class="edit-user-{{user.id}}" disabled="true" name="user_lastname"/>
          </div>
          <div style="grid-column: 2;" class="user-table-element">
              <input value="{{user.email}}" class="edit-user-{{user.id}}" disabled="true" name="user_email"/> <input class="edit-user-{{user.id}}" disabled="true" name="user_password"/>
              <button style="visibility: hidden;" name="edit:{{user.email}}"></button>
          </div> 
          <div style="grid-column: 3; padding: 0;" class="user-table-element">
              <form method="post">
                  {% csrf_token %}
                  <button id="edit_button" type="submit" name="edit:{{user.email}}" class="edit-user-{{user.id}}-confirm button-icon" onclick="data_edit(this)" style="display: none;"><div style="width: 1.5em">{% include "icons/pencil-icon.html" %}</div></button>
                  <button id="edit_button" type="button" name="edit:{{user.email}}" class="edit-user-{{user.id}}-undo button-icon" onclick="data_edit(this)" style="display: none;"><div style="width: 1.5em">{% include "icons/undo-icon.html" %}</div></button>
                  <button id="edit_button" type="button" name="edit:{{user.email}}" class="edit-user-{{user.id}}-edit button-icon" onclick="data_edit(this)" style="display: inline-flex;"><div style="width: 1.5em">{% include "icons/pencil-icon.html" %}</div></button>
              </form>
          </div>
          <div style="grid-column: 4; padding: 0; border-left: none;" class="user-table-element">
              <form method="post">
                  {% csrf_token %}
                  <button title="Удалить пользователя" name="delete:{{user.email}}" type="button" class="button-icon" onclick="delete_signal_to_send=this.name; $('#confirm-user-deleting-massage')[0].innerHTML = 'Вы уверены что хотите удалить пользователя ' + this.name.slice(this.name.indexOf(':') + 1) + '?'; $('#confirm-user-deleting-button')[0].name = this.name; disp_dialog($('#delete-user-confirm'))"><div style="width: 1.5em; padding: 0;">{% include "icons/delete-icon.html" %}</div></button>
              </form>
          </div>
      {% endfor %} -->
  </div>
  <!-- Code above includes modals, it needs to be totaly reworked -->
  <!-- <button id="blackout" style="display: none;" onclick="disp_dialog([$('#add-user'), $('#import-users')])"></button>
  {% include "./add_user.html" %}
  {% include "./import_users.html" %}
  <form method="post">
      {% csrf_token %}
      <table id="delete-user-confirm" class="dialog-table" style="display: none;">
          <tr><td colspan="2" id="confirm-user-deleting-massage">Вы уверены что хотите удалить пользователя?</td></tr>
          <tr>
              <td style="display: grid; justify-items: end;"><button id="confirm-user-deleting-button" type="submit" class="wrong">Подтвердить</button></td>
              <td><button type="button" onclick="disp_dialog($('#delete-user-confirm'))">Отменить</button></td>
          </tr>
      </table>
  </form> -->
</template>

<script>
import AddUserIcon from "@/assets/icons/add-user-icon.vue";
import ImportFromFileIcon from "@/assets/icons/import-from-file-icon.vue";

export default {
  components: {
    AddUserIcon,
    ImportFromFileIcon,
  },
};
</script>
