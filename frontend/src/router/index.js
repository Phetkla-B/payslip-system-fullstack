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