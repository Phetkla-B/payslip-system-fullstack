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

        // Reset login
        localStorage.removeItem("access_token");
        localStorage.removeItem("user_role");

        // Save token to localStorage
        localStorage.setItem("access_token", response.data.access_token);

        // Get current user profile to check role
        const meResponse = await api.get("/users/me");
        const role = meResponse.data.role;

        // Save user role for navigation menu
        localStorage.setItem("user_role", role);

        // Redirect by role
        if (role === "admin") {
            window.location.href = "/admin/upload";
        } else {
            window.location.href = ("/payslips");
        }
    } catch (error) {
        console.error("Login failed:", error);
        errorMessage.value = "เลขบัตรประชาชนหรือรหัสผ่านไม่ถูกต้อง";
    } finally {
        isLoading.value = false;
    }
}
</script>



<template>
    <div class="login-page">
        <div class="login-card">
            <h1>Self-Service Payslip</h1>
            <p>เข้าสู่ระบบเพื่อดูข้อมูลเงินเดือน</p>

            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label>เลขบัตรประชาชน</label>
                    <input
                        v-model="citizenId"
                        type="text"
                        placeholder="กรอกเลขบัตรประชาชน 13 หลัก"
                    />
                </div>

                <div class="form-group">
                    <label>รหัสผ่าน</label>
                    <input
                        v-model="password"
                        type="password"
                        placeholder="กรอกรหัสผ่าน"
                    />
                </div>

                <p v-if="errorMessage" class="error-message">
                    {{ errorMessage }}
                </p>

                <button type="submit" :disabled="isLoading">
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
    background-color: #f4f6f8;
}

.login-card {
    width: 360px;
    padding: 32px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

h1 {
    margin-bottom: 8px;
    font-size: 24px;
    color: #333;
}

p {
    margin-bottom: 24px;
    color: #666;
}

.form-group {
    margin-bottom: 16px;
}

label {
    display: block;
    margin-bottom: 6px;
    font-weight: 600;
    color: #555;
}

input {
    width: 100%;
    padding: 10px;
    border: 1px solid #d0d5dd;
    border-radius: 8px;
    font-size: 14px;
}

button {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 8px;
    background-color: #2563eb;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.error-message {
    margin-bottom: 14px;
    color: #dc2626;
    font-weight: 600;
}

</style>