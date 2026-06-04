<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../api/axios.js";

// Router is used to redirect user after login
const router = useRouter();

// Form data
const citizenId = ref("");
const password = ref("");

// UI state
const errorMessage = ref("");
const isLoading = ref(false);

async function handleLogin() {
    errorMessage.value = "";
    isLoading.value = true;

    try {
        // Call backend login API
        const response = await api.post("/auth/login", {
            citizen_id: citizenId.value,
            password: password.value,
        });

        // Reset before login
        localStorage.removeItem("access_token");
        localStorage.removeItem("user_name");
        localStorage.removeItem("user_role");

        // Save token to localStorage
        localStorage.setItem("access_token", response.data.access_token);

        // Get current user profile to check role
        const meResponse = await api.get("/users/me");
        const role = meResponse.data.role;

        // Save user role for navigation menu
        localStorage.setItem("user_role", role);
        localStorage.setItem("user_name", `${meResponse.data.first_name} ${meResponse.data.last_name}`);

        // Redirect by role
        if (role === "admin") {
            window.location.href = "/admin/upload";
        } else {
            window.location.href = ("/payslips");
        }
    } catch (error) {
        console.error("Login failed:", error);

        if (error.response?.status === 401){
            errorMessage.value = "เลขบัตรประชาชนหรือรหัสผ่านไม่ถูกต้อง";
        } else if (!error.response) {
            errorMessage.value = "ไม่สามารถเชื่อมต่อ Server ได้";
        } else {
            errorMessage.value = "เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง";
        }
        
    } finally {
        isLoading.value = false;
    }
}
</script>



<template>
    <div class="login-page">
        <div class="card login-card">
            <h1 class="login-title">Self-Service Payslip</h1>
            <p class="login-subtitle">
                เข้าสู่ระบบเพื่อดูข้อมูลเงินเดือน
            </p>

            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label class="form-label">เลขบัตรประชาชน</label>

                    <input
                        class="form-control"
                        v-model="citizenId"
                        type="text"
                        placeholder="กรอกเลขบัตรประชาชน 13 หลัก"
                    />
                </div>

                <div class="form-group">
                    <label class="form-label">รหัสผ่าน</label>

                    <input
                        class="form-control"
                        v-model="password"
                        type="password"
                        placeholder="กรอกรหัสผ่าน"
                    />
                </div>

                <p v-if="errorMessage" class="alert-error">
                    {{ errorMessage }}
                </p>

                <button 
                    class="btn btn-primary login-button"
                    type="submit" :disabled="isLoading"
                >
                    {{ isLoading ? "กำลังเข้าสู่ระบบ..." : "เข้าสู่ระบบ" }}
                </button>
            </form>
        </div>
    </div>
</template>


<style scoped>
.login-page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 24px;
}

.login-card {
    width: 360px;
    max-width: 380;
}

.login-title {
    margin: 0 0 8px;
    font-size: 26px;
    text-align: center;
}

.login-subtitle {
    margin-bottom: 24px;
    color: #6b7280;
    text-align: center;
}

.login-button {
    width: 100%;
    margin-top: 8px;
}
</style>