<template>
  <div id="all-groups-table-header">
    <div style="grid-column: 1">
      <span style="font-size: larger">Все группы</span>
    </div>
    <div style="grid-column: 3">
      <button type="submit" name="new-group" class="button-icon">
        <AddGroupIcon />Добавить &nbsp;
      </button>
    </div>
  </div>
  <div id="all-groups-table">
    <!-- Here goes iteration for groups in all groups, needs Django API -->
    <!-- {% for group in allgroup %}
      <div class="all-groups-table-element">
          <a href="{{group.id}}">{{group.name}}</a>
      </div>
      {% endfor %} -->
  </div>
</template>

<script>
import AddGroupIcon from "@/assets/icons/add-group-icon.vue";

export default {
  components: {
    AddGroupIcon,
  },
};
</script>
