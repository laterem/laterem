<template>
  <span
    class="caret"
    :class="{ 'caret-down': isActive }"
    @click="isActive = !isActive"
  >
    <input
      :value="nodeName"
      :name="categoryIdName"
      :id="categoryIdName"
      disabled="true"
    />
    <!-- Here must go buttons
        of category name editing
        v-if="isEditable" -->
  </span>
  <ul :id="categoryUlId" class="nested" :class="{ active: isActive }">
    <!-- Category render -->
    <li v-for="child in childrenCategories" :key="child">
      <NodeTree :node="child"></NodeTree>
    </li>
    <!-- Work render -->
    <li v-for="child in childrenWorks" :key="child">
      <span style="border: none">
        <a :href="'/works/' + child.id + '/'">{{ child.name }}</a>
      </span>
      <!-- Progress line -->
    </li>
  </ul>
</template>

<script>
import NodeTree from "./NodeTree.vue";

export default {
  name: "NodeTree",
  components: {
    NodeTree,
  },
  props: {
    node: Object,
    isEditable: Boolean,
  },
  data() {
    return {
      isActive: false,
    };
  },
  computed: {
    childrenCategories() {
      let _childrenCategories = [];
      for (let i = 0; i < this.node.children.length; i++) {
        if (this.node.children[i].type == "category") {
          _childrenCategories.push(this.node.children[i]);
        }
      }
      return _childrenCategories.length ? _childrenCategories : undefined;
    },
    childrenWorks() {
      let _childrenWorks = [];
      for (let i = 0; i < this.node.children.length; i++) {
        if (this.node.children[i].type == "work") {
          _childrenWorks.push(this.node.children[i]);
        }
      }
      return _childrenWorks.length ? _childrenWorks : undefined;
    },
    nodeName() {
      return this.node.name;
    },
    categoryIdName() {
      return "input-" + this.node.id;
    },
    categoryUlId() {
      return "category-id-" + this.node.id;
    },
  },
};
</script>
