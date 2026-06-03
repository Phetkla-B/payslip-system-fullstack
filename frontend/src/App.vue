<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

// Check current page
const isLoginPage = computed(() => route.path === "/login");

// Read user role from localStorage
const userRole = computed(() => localStorage.getItem("user_role"));

// Logout user
function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user_role");

  router.push("/login");
}
</script>


<template>
  <dev>
    <nav v-if="!isLoginPage" class="navbar">
      <div class="nav-left">
        <strong>Payslip System</strong>

        <router-link v-if="userRole === 'admin'" to="/admin/upload">
          Upload
        </router-link>

        <router-link v-if="userRole === 'admin'" to="/admin/upload-history">
          Upload History
        </router-link>

        <router-link v-if="userRole === 'employee'" to="/payslips">
          My Payslips
        </router-link>
        
      </div>

      <button @click="logout">
        Logout
      </button>
    </nav>

    <router-view />
  </dev>
</template>


<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-item: center;
  padding: 16px 32px;
  background: #1f2937;
  color: white;
}

.nav-left {
  display: flex;
  align-item: center;
  gap: 20px;
}

a {
  color: white;
  text-decoration: none;
}

a.router-link-active {
  text-decoration: underline;
}

button {
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>