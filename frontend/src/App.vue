<template>
  <aside id="menu"></aside>
  <aside id="content">
    <router-view />
  </aside>
</template>

<style scoped>
aside#menu,
aside#content {
  position: absolute;
  top: 65px;
  bottom: 10px;

  overflow: scroll;
}

aside#menu {
  left: 10px;

  width: calc(20% - 20px);

  padding: 10px;
  border-radius: 20px;

  background: var(--content-background-color);
  box-shadow: 4px 4px 4px var(--content-shadow-color);

  overflow-x: scroll;
}
#menu li {
  margin: 5px 0px 5px 0px;
}
#menu a {
  display: block;

  margin: 5px 0px 0px 0px;

  padding: 2px;
  padding-bottom: 0px;
  margin: 1px;

  font-size: 0.9em;
  text-decoration: none;
  color: var(--body-font-color);
}

#menu a:hover {
  background-color: var(--content-hover-color);
}

#menu .title {
  font-size: large;
}

aside#content {
  left: calc(20% + 20px);

  width: calc(80% - 30px);

  border-radius: 20px;
  box-shadow: 4px 4px 4px var(--content-shadow-color);
  background: var(--content-background-color);
}

div#content {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;

  padding: 10px;
}
</style>
