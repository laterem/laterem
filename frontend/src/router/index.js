import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import StudentView from "../views/StudentView.vue";
import TeacherView from "../views/TeacherView.vue";
import UsersPanelView from "../views/teacherPanel/UsersPanelView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/student",
    name: "student",
    component: StudentView,
  },
  {
    path: "/teacher",
    name: "teacher",
    component: TeacherView,
    children: [
      {
        path: "/teacher/users",
        name: "users",
        component: UsersPanelView,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
