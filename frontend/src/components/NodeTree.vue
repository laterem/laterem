<template>
<span class="caret caret-down">
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
<ul :id="categoryUlId" class="nested active">
    <!-- Category render -->
    <li v-for="child in childrenCategories" :key="child">
        <NodeTree
            :node="child"
        ></NodeTree>
    </li>
    <!-- Work render -->
    <li v-for="child in childrenWorks" :key="child">
        <span style="border: none;">
            <a :href="'/works/' + child.id + '/'">{{ child.name }}</a>
        </span>
        <!-- Progress line -->
    </li>
</ul>

</template>

<script>
import NodeTree from './NodeTree.vue'

export default {
    name: 'NodeTree',
    components: {
        NodeTree,
    },
    props: {
        node: Object,
        isEditable: Boolean,
    },
    computed: {
        childrenCategories() {
            let _childrenCategories = [];
            let node = JSON.parse(JSON.stringify(this.node, null, 4))[0];
            for ( let i = 0; i < node.children.length; i ++ ) {
                if ( node.children[i].type == 'category' ) {
                    _childrenCategories.push(node.children[i]);
                }
            }
            return _childrenCategories.length ? _childrenCategories : undefined
        },
        childrenWorks() {
            let _childrenWorks = [];
            let node = JSON.parse(JSON.stringify(this.node, null, 4))[0];
            for ( let i = 0; i < node.children.length; i ++ ) {
                if ( node.children[i].type == 'work' ) {
                    _childrenWorks.push(node.children[i]);
                }
            }
            return _childrenWorks.length ? _childrenWorks : undefined
        },
        nodeName() {
            return JSON.parse(JSON.stringify(this.node, null, 4))[0].name
        },
        categoryIdName() {
            return 'input-' + JSON.parse(JSON.stringify(this.node, null, 4))[0].id
        },
        categoryUlId() {
            return 'category-id-' + JSON.parse(JSON.stringify(this.node, null, 4))[0].id
        },
    },
};
</script>
  