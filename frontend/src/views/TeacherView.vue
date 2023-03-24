<template>
  <aside id="menu">
    <RouterLink to="/teacher/users/">Все пользователи</RouterLink>
    <RouterLink to="/teacher/groups/">Группы</RouterLink>
    <RouterLink to="/teacher/works/">Работы</RouterLink>
    <RouterLink to="/teacher/tasks/">Шаблоны задач</RouterLink>
  </aside>
  <aside id="content">
    <RouterView />
  </aside>
</template>
