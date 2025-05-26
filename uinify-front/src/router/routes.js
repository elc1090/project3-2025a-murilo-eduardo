const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    redirect: "/login",
    children: [
      {
        path: "login",
        component: () => import("pages/LoginPage.vue"),
        name: "login",
      },
      {
        path: "dashboard",
        component: () => import("pages/DashboardPage.vue"),
        name: "dashboard",
      },
      {
        path: "share",
        component: () => import("pages/ShareComponent.vue"),
        name: "share",
      },
    ],
  },
  {
    path: "/components",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        component: () => import("pages/ComponentsPage.vue"),
        name: "components",
      },
      {
        path: ":id",
        component: () => import("pages/ComponentViewPage.vue"),
        name: "component-view",
        props: true,
      },
      {
        path: ":id/edit",
        component: () => import("pages/ShareComponent.vue"),
        name: "component-edit",
        props: true,
      },
    ],
  },

  {
    path: "/unauthorized",
    component: () => import("pages/ErrorUnauthorized.vue"),
    name: "unauthorized",
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
