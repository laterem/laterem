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
      <img :src="iconFolder + 'book-plus.svg'" width="1.5em" />
    </button>
  </h1>
  <ul v-if="workTree.id == 'mother'" class="wtree">
    <!-- Here must go list of childs -->
    <li>
      <NodeTree
        :node="JSON.parse(JSON.stringify(workTree.children, null, 4))[0]"
        :isEditable="isEditable"
      ></NodeTree>
    </li>
  </ul>
</template>

<script>
import NodeTree from "./NodeTree.vue";

export default {
  name: "NavTree",
  components: {
    NodeTree,
  },
  props: {
    workTree: Object,
    isEditable: Boolean,
  },
  data() {
    return {
      iconFolder: "/static/icons/",
    };
  },
};
</script>

<style>
ul, #myUL {
  list-style-type: none;
}

#myUL {
  margin: 0;
  padding: 0;
}

#myUL a {
  text-decoration: none;
  color: var(--body-font-color);
}

ul.wtree, .wtree ul {
  margin-left: var(--ident);
}

.wtree {
  padding: 0;
  --radius: 10px;
}

.wtree * {
  padding: 0;
}

.wtree a {
  text-decoration: none;
  color: var(--body-font-color);
}

.wtree li {
  list-style-type: none;
  margin: 10px 0 10px 10px;
  position: relative;
}

.wtree li:before {
  content: "";
  position: absolute;
  top: -10px;
  left: var(--left);
  border-left: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  border-radius: 0 var(--radius);
  width: var(--ident);
  height: 1.75em;
}

.wtree li:after {
  position: absolute;
  content: "";
  top: 0;
  left: var(--left);
  border-left: 1px solid var(--border);
  width: var(--ident);
  height: 100%;
}

.wtree li:last-child:after {
  display: none;
}

.wtree span {
  display: flex;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 10px;
  color: var(--body-font-color);
  text-decoration: none;
  /* height: 1em; */
}

.wtree span input {
  min-width: -moz-available;
  min-width: -webkit-fill-available;
  min-width: -ms-available;

  max-width: max-content;
}

.wtree span button {
  position: relative;
  width: 40px;
  justify-content: center;
  align-content: center;
  height: 2em;
  padding: 0.5em;
  right: 170px;
  margin-left: 2.5px;
}

.wtree li span:hover, .wtree li span:focus {
  background: var(--content-hover-color); 
  color: var(--body-font-color); 
  border: 1px solid var(--border-hover);
  border-radius: var(--radius);
}
.wtree li span:hover + ul li span, .wtree li span:focus + ul li span {
  background: var(--content-hover-color); 
  color: var(--body-font-color); 
  border: 1px solid var(--border-hover);
  border-radius: var(--radius);
}

.wtree li span:hover ul li:before, .wtree li span:focus ul li:before,
.wtree li span:hover ul li:after, .wtree li span:focus ul li:after {
  border-color: var(--border-hover);
}

.caret {
  cursor: pointer;
  -webkit-user-select: none; /* Safari 3.1+ */
  -moz-user-select: none; /* Firefox 2+ */
  -ms-user-select: none; /* IE 10+ */
  user-select: none;
}

.caret::before {
  content: url("data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8' standalone='no'%3F%3E%3C!-- Created with Inkscape (http://www.inkscape.org/) --%3E%3Csvg width='15px' height='15px' viewBox='0 0 5 5' version='1.1' id='svg5' inkscape:version='1.2.1 (9c6d41e410, 2022-07-14)' sodipodi:docname='caret-icon.svg' xmlns:inkscape='http://www.inkscape.org/namespaces/inkscape' xmlns:sodipodi='http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd' xmlns='http://www.w3.org/2000/svg' xmlns:svg='http://www.w3.org/2000/svg'%3E%3Csodipodi:namedview id='namedview7' pagecolor='%23505050' bordercolor='%23eeeeee' borderopacity='1' inkscape:showpageshadow='0' inkscape:pageopacity='0' inkscape:pagecheckerboard='true' inkscape:deskcolor='%23505050' inkscape:document-units='mm' showgrid='false' inkscape:zoom='17.678304' inkscape:cx='6.8728311' inkscape:cy='14.537593' inkscape:window-width='1920' inkscape:window-height='1057' inkscape:window-x='-8' inkscape:window-y='-8' inkscape:window-maximized='1' inkscape:current-layer='layer1' /%3E%3Cdefs id='defs2'%3E%3Cinkscape:path-effect effect='fillet_chamfer' id='path-effect223' is_visible='true' lpeversion='1' nodesatellites_param='F,0,0,1,0,0.52916667,0,1 @ F,0,0,1,0,0.52916667,0,1 @ F,0,0,1,0,0.52916667,0,1' unit='px' method='auto' mode='F' radius='2' chamfer_steps='1' flexible='false' use_knot_distance='true' apply_no_radius='true' apply_with_radius='true' only_selected='false' hide_knots='false' /%3E%3C/defs%3E%3Cg inkscape:label='Слой 1' inkscape:groupmode='layer' id='layer1'%3E%3Cpath sodipodi:type='star' style='fill:%23ffffff;stroke-width:0.266999;fill-opacity:1' id='path113' inkscape:flatsided='true' sodipodi:sides='3' sodipodi:cx='2.5' sodipodi:cy='2.5' sodipodi:r1='2.5053763' sodipodi:r2='1.2526883' sodipodi:arg1='0' sodipodi:arg2='1.0471976' inkscape:rounded='0' inkscape:randomized='0' d='M 4.5471046,2.7645833 1.7055836,4.4051362 A 0.30551452,0.30551452 30 0 1 1.2473118,4.1405529 l 0,-3.28110579 A 0.30551452,0.30551452 150 0 1 1.7055836,0.59486378 l 2.841521,1.64055292 a 0.30551452,0.30551452 90 0 1 0,0.5291666 z' inkscape:transform-center-x='-0.62634409' inkscape:path-effect='%23path-effect223' /%3E%3C/g%3E%3C/svg%3E");
  display: inline-block;
  margin-right: 10px;
  color: var(--body-font-color);
  height: 15px;
  align-self: center;
}

.caret-down::before {
  transform: rotate(90deg);  
}

.nested {
  display: none;
}
</style>
