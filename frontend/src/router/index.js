import { createRouter, createWebHistory } from 'vue-router';
import LoginView from "../views/LoginView.vue";
import AdminUploadView from "../views/AdminUploadView.vue";
import UploadHistoryView from "../views/UploadHistoryView.vue";
import PayslipListView from "../views/PayslipListView.vue";
import PayslipDetailView from "../views/PayslipDetailView.vue";

const routes = [
    {
        path: "/",
        redirect: "/login",
    },
    {
        path: "/login",
        component: LoginView,
    },
    {
        path: "/admin/upload",
        component: AdminUploadView,
    },
    {
        path: "/admin/upload-history",
        component: UploadHistoryView,
    },
    {
        path: "/payslips",
        component: PayslipListView,
    },
    {
        path: "/payslips/:id",
        component: PayslipDetailView,   
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("user_role");

    // Public page
    if (to.path === "/login") {
        next();
        return;
    }

    // No token, redirect to login
    if (!token) {
        next("/login");
        return;
    }

    // Employee cannot access admin page
    if (to.path.startsWith("/admin") && role !== "admin") {
        next("/payslips");
        return;
    }

    // Admin should not access employee payslip pages
    if (to.path.startsWith("/payslips") && role === "admin") {
        next("/admin/upload");
        return;
    }

    next();
});