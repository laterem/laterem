<template>
    <NavTree :workTree="workTree" :isEditable="isEditable"></NavTree>
</template>

<script>
import NavTree from './components/NavTree.vue';

export default {
  name: 'NavTreeApp',
  components: {
    NavTree
  },
  data(){
    return{
        workTree: {
            'name': 'mother',
            'type': 'category',
            'id': 'mother',
            'children': [
                {
                    "name": "Misc.",
                    "type": "category",
                    "id": 1,
                    "children": [
                        {
                            "name": "Misc2.",
                            "type": "category",
                            "id": 2,
                            "children": [
                                {
                                    "name": "\u0420\u0430\u0431\u043e\u0442\u0430!",
                                    "type": "work",
                                    "id": 1,
                                    "stats": {
                                        "OK": 0.6,
                                        "PS": 0.0,
                                        "ST": 0.0,
                                        "WA": 0.0,
                                        "NA": 0.4
                                    }
                                }
                            ]
                        }
                    ]
                },
            ],
        },
        isEditable: false,
    };
  },
};
</script>
