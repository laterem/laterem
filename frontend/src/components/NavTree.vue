<template>
<h1 v-if="workTree.id == 'mother'" class="title">
  {{ workTree.name }}
  <button
    v-if="isEditable"
    type="submit"
    name="add-category-mother"
    class="button-icon"
    style="margin-left: 10px; height: min-content"
  >
    <img :src="iconFolder + 'book-plus.svg'" width="1.5em"/>
  </button>
</h1>
<ul v-if="workTree.id == 'mother'" class="wtree">
  <!-- Here must go list of childs -->
  <li>
    <NodeTree :node="workTree.children" :isEditable="isEditable"></NodeTree>
  </li>
</ul>
</template>

<script>
import NodeTree from './NodeTree.vue';

export default {
  name: 'NavTree',
  components: {
    NodeTree,
  },
  props: {
    workTree: Object,
    isEditable: Boolean,
  },
  data() {
    return {
      iconFolder: '/static/icons/',
    };
  },
};
</script>
