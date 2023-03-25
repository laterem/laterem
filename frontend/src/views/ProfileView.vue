<template>
  <aside id="menu">Профиль</aside>
  <aside id="content">
    <div style="display: flex; margin-bottom: 10px">
      <div style="width: 100px; height: 100px"><userIcon /></div>
      <div>
        <h1 style="justify-self: center">
          <!--{{user.dbmodel.first_name}} {{user.dbmodel.last_name}}-->
        </h1>
        <h3 style="justify-self: center"><!--{{user.dbmodel.email}}--></h3>
        <RouterLink class="button" to="/logout">Выйти</RouterLink>
      </div>
    </div>
  </aside>
</template>

<script>
import userIcon from "@/assets/icons/user-icon.vue";

export default {
  components: {
    userIcon,
  },
};
</script>
