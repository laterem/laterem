import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/HomeView.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
  },
  {
    path: "/student",
    name: "student",
    component: () => import("@/views/StudentView.vue"),
  },
  {
    path: "/teacher",
    name: "teacher",
    component: () => import("@/views/TeacherView.vue"),
    children: [
      {
        path: "/teacher/users",
        name: "users",
        component: () => import("@/views/teacherPanel/UsersPanelView.vue"),
      },
      {
        path: "/teacher/groups",
        name: "groups",
        component: () => import("@/views/teacherPanel/GroupsPanelView.vue"),
      },
      {
        path: "/teacher/works",
        name: "works",
        component: () => import("@/views/teacherPanel/WorksPanelView.vue"),
      },
      {
        path: "/teacher/tasks",
        name: "tasks",
        component: () => import("@/views/teacherPanel/TasksPanelView.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
